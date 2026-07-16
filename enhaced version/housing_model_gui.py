"""
Simple GUI runner for the Alabama housing model.

What it does:
- Runs my_housing_model (1).py with the current Python interpreter.
- Streams training output into a text panel.
- Loads and previews training_history.png after the run.
"""

from __future__ import annotations

import os
import queue
import re
import subprocess
import sys
import threading
import tkinter as tk
from tkinter import ttk


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_MODULE_FILE = os.path.join(BASE_DIR, "housing_model", "pipeline.py")
TRAINING_PLOT_PATH = os.path.join(BASE_DIR, "training_history.png")
TREND_PLOT_PATH = os.path.join(BASE_DIR, "actual_vs_predicted_prices.png")
LOCATIONS_PLOT_PATH = os.path.join(BASE_DIR, "best_price_locations.png")
UTILITIES_PLOT_PATH = os.path.join(BASE_DIR, "estimated_utilities_by_county.png")


class HousingModelGUI:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Alabama Home Price Explorer")
        self.root.geometry("1180x780")

        self.output_queue: queue.Queue[str] = queue.Queue()
        self.process: subprocess.Popen[str] | None = None
        self.training_plot_image: tk.PhotoImage | None = None
        self.trend_plot_image: tk.PhotoImage | None = None
        self.locations_plot_image: tk.PhotoImage | None = None
        self.utilities_plot_image: tk.PhotoImage | None = None

        self.status_var = tk.StringVar(value="Ready")
        self.mae_var = tk.StringVar(value="Test MAE: not run yet")

        self._configure_style()
        self._build_ui()
        self._poll_output_queue()

    def _create_scrollable_plot_tab(self, parent: ttk.Frame, placeholder_text: str) -> tuple[tk.Canvas, ttk.Label]:
        container = ttk.Frame(parent)
        container.pack(fill="both", expand=True)

        canvas = tk.Canvas(container, background="#ffffff", highlightthickness=0)
        v_scroll = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        h_scroll = ttk.Scrollbar(container, orient="horizontal", command=canvas.xview)

        canvas.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)

        v_scroll.pack(side="right", fill="y")
        h_scroll.pack(side="bottom", fill="x")
        canvas.pack(side="left", fill="both", expand=True)

        inner = ttk.Frame(canvas)
        canvas.create_window((0, 0), window=inner, anchor="nw")

        label = ttk.Label(inner, text=placeholder_text, justify="center")
        label.pack(padx=10, pady=10)

        def update_scrollregion(_event: tk.Event) -> None:
            canvas.configure(scrollregion=canvas.bbox("all"))

        inner.bind("<Configure>", update_scrollregion)
        canvas.bind(
            "<MouseWheel>",
            lambda event: canvas.yview_scroll(int(-1 * (event.delta / 120)), "units"),
        )

        return canvas, label

    def _configure_style(self) -> None:
        style = ttk.Style()
        style.theme_use("clam")

        self.root.configure(bg="#eaf6ff")
        style.configure("App.TFrame", background="#eaf6ff")

        style.configure(
            "Card.TLabelframe",
            background="#ffffff",
            borderwidth=2,
            relief="solid",
            bordercolor="#9dd3ff",
        )
        style.configure(
            "Card.TLabelframe.Label",
            font=("Segoe UI", 11, "bold"),
            foreground="#0f4c81",
            background="#ffffff",
        )

        style.configure(
            "Title.TLabel",
            background="#eaf6ff",
            font=("Segoe UI", 22, "bold"),
            foreground="#0f4c81",
        )
        style.configure(
            "Help.TLabel",
            background="#eaf6ff",
            font=("Segoe UI", 11),
            foreground="#145374",
        )
        style.configure(
            "Metrics.TLabel",
            background="#eaf6ff",
            font=("Segoe UI", 12, "bold"),
            foreground="#0f4c81",
        )

        style.configure(
            "Primary.TButton",
            font=("Segoe UI", 11, "bold"),
            padding=(12, 9),
            background="#2ec4b6",
            foreground="#062c30",
            borderwidth=0,
        )
        style.map(
            "Primary.TButton",
            background=[("active", "#20b3a7"), ("disabled", "#bfece7")],
            foreground=[("disabled", "#6e8a8f")],
        )

        style.configure(
            "Secondary.TButton",
            font=("Segoe UI", 10, "bold"),
            padding=(9, 7),
            background="#ffde7d",
            foreground="#5a4300",
            borderwidth=0,
        )
        style.map(
            "Secondary.TButton",
            background=[("active", "#ffd05a"), ("disabled", "#f7edc9")],
            foreground=[("disabled", "#8c8464")],
        )

        style.configure("TNotebook", background="#d7efff", borderwidth=0)
        style.configure(
            "TNotebook.Tab",
            font=("Segoe UI", 10, "bold"),
            padding=(12, 7),
            background="#9dd3ff",
            foreground="#0f4c81",
        )
        style.map(
            "TNotebook.Tab",
            background=[("selected", "#4eb3ff"), ("active", "#7ec6ff")],
            foreground=[("selected", "#ffffff")],
        )

    def _build_ui(self) -> None:
        header = ttk.Frame(self.root, style="App.TFrame", padding=(14, 10, 14, 6))
        header.pack(fill="x")

        ttk.Label(header, text="Alabama Home Price Explorer", style="Title.TLabel").pack(anchor="w")
        ttk.Label(
            header,
            text=(
                "1) Click Start Model.  2) Wait for Done.  3) Click tabs to explore charts for 2025-2026."
            ),
            style="Help.TLabel",
        ).pack(anchor="w", pady=(4, 0))

        badge_strip = tk.Frame(header, bg="#eaf6ff")
        badge_strip.pack(anchor="w", pady=(6, 0))
        tk.Label(
            badge_strip,
            text="Easy Mode",
            bg="#ffd166",
            fg="#5a4300",
            font=("Segoe UI", 10, "bold"),
            padx=8,
            pady=3,
        ).pack(side="left")
        tk.Label(
            badge_strip,
            text="  Live Charts  ",
            bg="#80ed99",
            fg="#185b31",
            font=("Segoe UI", 10, "bold"),
            padx=8,
            pady=3,
        ).pack(side="left", padx=(8, 0))
        tk.Label(
            badge_strip,
            text="  2025-2026 Data  ",
            bg="#90e0ef",
            fg="#004e64",
            font=("Segoe UI", 10, "bold"),
            padx=8,
            pady=3,
        ).pack(side="left", padx=(8, 0))

        top = ttk.Frame(self.root, style="App.TFrame", padding=(14, 4, 14, 8))
        top.pack(fill="x")

        self.run_button = ttk.Button(top, text="Start Model", command=self.run_model, style="Primary.TButton")
        self.run_button.pack(side="left")

        self.stop_button = ttk.Button(
            top,
            text="Stop",
            command=self.stop_model,
            state="disabled",
            style="Secondary.TButton",
        )
        self.stop_button.pack(side="left", padx=(8, 0))

        self.training_plot_button = ttk.Button(
            top,
            text="Reload Epoch Plot",
            command=self.load_training_plot,
            style="Secondary.TButton",
        )
        self.training_plot_button.pack(side="left", padx=(8, 0))

        self.trend_plot_button = ttk.Button(
            top,
            text="Reload Actual vs Predicted",
            command=self.load_trend_plot,
            style="Secondary.TButton",
        )
        self.trend_plot_button.pack(side="left", padx=(8, 0))

        self.locations_plot_button = ttk.Button(
            top,
            text="Reload County Locations",
            command=self.load_locations_plot,
            style="Secondary.TButton",
        )
        self.locations_plot_button.pack(side="left", padx=(8, 0))

        self.utilities_plot_button = ttk.Button(
            top,
            text="Reload Utilities Chart",
            command=self.load_utilities_plot,
            style="Secondary.TButton",
        )
        self.utilities_plot_button.pack(side="left", padx=(8, 0))

        ttk.Label(top, textvariable=self.status_var, style="Metrics.TLabel").pack(side="right")

        metrics = ttk.Frame(self.root, style="App.TFrame", padding=(14, 0, 14, 8))
        metrics.pack(fill="x")
        ttk.Label(metrics, textvariable=self.mae_var, style="Metrics.TLabel").pack(anchor="w")

        main = ttk.PanedWindow(self.root, orient="horizontal")
        main.pack(fill="both", expand=True, padx=14, pady=(0, 14))

        output_frame = ttk.LabelFrame(main, text="What the model is doing", padding=10, style="Card.TLabelframe")
        self.output_text = tk.Text(
            output_frame,
            wrap="word",
            height=30,
            font=("Consolas", 10),
            background="#fffdf5",
            foreground="#3d2c00",
            insertbackground="#3d2c00",
            highlightthickness=1,
            highlightbackground="#ffe8a3",
        )
        output_scroll = ttk.Scrollbar(output_frame, orient="vertical", command=self.output_text.yview)
        self.output_text.configure(yscrollcommand=output_scroll.set)
        self.output_text.pack(side="left", fill="both", expand=True)
        output_scroll.pack(side="right", fill="y")

        plot_frame = ttk.LabelFrame(main, text="Charts", padding=10, style="Card.TLabelframe")
        self.plot_tabs = ttk.Notebook(plot_frame)
        self.plot_tabs.pack(fill="both", expand=True)

        epoch_tab = ttk.Frame(self.plot_tabs)
        trend_tab = ttk.Frame(self.plot_tabs)
        locations_tab = ttk.Frame(self.plot_tabs)
        utilities_tab = ttk.Frame(self.plot_tabs)

        self.plot_tabs.add(epoch_tab, text="Epoch Plots")
        self.plot_tabs.add(trend_tab, text="Actual Data + Prediction")
        self.plot_tabs.add(locations_tab, text="County Locations")
        self.plot_tabs.add(utilities_tab, text="Utilities (Estimate)")

        self.training_plot_canvas, self.training_plot_label = self._create_scrollable_plot_tab(
            epoch_tab,
            "Epoch loss/MAE chart not ready yet. Click Start Model first.",
        )

        self.trend_plot_canvas, self.trend_plot_label = self._create_scrollable_plot_tab(
            trend_tab,
            "Actual-vs-predicted chart not ready yet. Click Start Model first.",
        )

        self.locations_plot_canvas, self.locations_plot_label = self._create_scrollable_plot_tab(
            locations_tab,
            "County best-price chart not ready yet. Click Start Model first.",
        )

        self.utilities_plot_canvas, self.utilities_plot_label = self._create_scrollable_plot_tab(
            utilities_tab,
            "Estimated utilities chart not ready yet. Click Start Model first.",
        )

        main.add(output_frame, weight=3)
        main.add(plot_frame, weight=2)

    def append_output(self, text: str) -> None:
        self.output_text.insert("end", text)
        self.output_text.see("end")

    def run_model(self) -> None:
        if not os.path.exists(MODEL_MODULE_FILE):
            self.append_output(f"Error: module file not found: {MODEL_MODULE_FILE}\n")
            self.status_var.set("Script missing")
            return

        self.output_text.delete("1.0", "end")
        self.mae_var.set("Test MAE: running...")
        self.status_var.set("Running model...")
        self.run_button.configure(state="disabled")
        self.stop_button.configure(state="normal")

        thread = threading.Thread(target=self._run_model_worker, daemon=True)
        thread.start()

    def _run_model_worker(self) -> None:
        cmd = [sys.executable, "-m", "housing_model.pipeline"]
        try:
            self.process = subprocess.Popen(
                cmd,
                cwd=BASE_DIR,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
            )

            assert self.process.stdout is not None
            lines: list[str] = []
            for line in self.process.stdout:
                lines.append(line)
                self.output_queue.put(line)

            return_code = self.process.wait()
            full_output = "".join(lines)
            mae_match = re.search(r"Test MAE:\s*([0-9.]+)", full_output)
            if mae_match:
                mae = mae_match.group(1)
                self.output_queue.put(f"\nParsed Test MAE: {mae} (x $100,000)\n")
                self.output_queue.put("__MAE__" + mae)

            if return_code == 0:
                self.output_queue.put("\nRun finished successfully.\n")
                self.output_queue.put("__DONE_OK__")
            else:
                self.output_queue.put(f"\nRun failed with exit code {return_code}.\n")
                self.output_queue.put("__DONE_FAIL__")
        except Exception as exc:
            self.output_queue.put(f"\nUnexpected error: {exc}\n")
            self.output_queue.put("__DONE_FAIL__")
        finally:
            self.process = None

    def stop_model(self) -> None:
        if self.process and self.process.poll() is None:
            self.process.terminate()
            self.append_output("\nStop requested.\n")
            self.status_var.set("Stopping...")

    def _poll_output_queue(self) -> None:
        try:
            while True:
                item = self.output_queue.get_nowait()

                if item.startswith("__MAE__"):
                    value = item.replace("__MAE__", "", 1)
                    self.mae_var.set(f"Test MAE: {value} (x $100,000)")
                    continue

                if item == "__DONE_OK__":
                    self.status_var.set("Done!")
                    self.run_button.configure(state="normal")
                    self.stop_button.configure(state="disabled")
                    self.load_training_plot()
                    self.load_trend_plot()
                    self.load_locations_plot()
                    self.load_utilities_plot()
                    continue

                if item == "__DONE_FAIL__":
                    self.status_var.set("Run failed")
                    self.run_button.configure(state="normal")
                    self.stop_button.configure(state="disabled")
                    continue

                self.append_output(item)
        except queue.Empty:
            pass

        self.root.after(100, self._poll_output_queue)

    def load_plot(self, path: str, label: ttk.Label, canvas: tk.Canvas, image_slot: str) -> None:
        if not os.path.exists(path):
            label.configure(
                text="Plot not found yet. Run the model first.",
                image="",
            )
            label.update_idletasks()
            canvas.configure(scrollregion=canvas.bbox("all"))
            canvas.xview_moveto(0)
            canvas.yview_moveto(0)
            return

        try:
            image_obj = tk.PhotoImage(file=path)
            setattr(self, image_slot, image_obj)
            label.configure(image=image_obj, text="")
            label.update_idletasks()
            canvas.configure(scrollregion=canvas.bbox("all"))
            canvas.xview_moveto(0)
            canvas.yview_moveto(0)
        except Exception as exc:
            label.configure(
                image="",
                text=(
                    "Could not preview PNG in Tk on this system.\n"
                    f"File exists at: {path}\n"
                    f"Error: {exc}"
                ),
            )
            label.update_idletasks()
            canvas.configure(scrollregion=canvas.bbox("all"))
            canvas.xview_moveto(0)
            canvas.yview_moveto(0)

    def load_training_plot(self) -> None:
        self.load_plot(
            TRAINING_PLOT_PATH,
            self.training_plot_label,
            self.training_plot_canvas,
            "training_plot_image",
        )

    def load_trend_plot(self) -> None:
        self.load_plot(
            TREND_PLOT_PATH,
            self.trend_plot_label,
            self.trend_plot_canvas,
            "trend_plot_image",
        )

    def load_locations_plot(self) -> None:
        self.load_plot(
            LOCATIONS_PLOT_PATH,
            self.locations_plot_label,
            self.locations_plot_canvas,
            "locations_plot_image",
        )

    def load_utilities_plot(self) -> None:
        self.load_plot(
            UTILITIES_PLOT_PATH,
            self.utilities_plot_label,
            self.utilities_plot_canvas,
            "utilities_plot_image",
        )


def main() -> None:
    root = tk.Tk()
    app = HousingModelGUI(root)
    app.load_training_plot()
    app.load_trend_plot()
    app.load_locations_plot()
    app.load_utilities_plot()
    root.mainloop()


if __name__ == "__main__":
    main()
