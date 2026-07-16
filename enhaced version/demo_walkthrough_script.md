Demo Walkthrough Script

1) The goal
My project predicts Alabama home prices using housing feature data, then visualizes the results so people can compare trends by time and county. In plain language: I built a tool that helps estimate prices and quickly show where the model is doing well or struggling.

2) The data
I used the Alabama housing dataset in my project folder (alabama_housing (1).csv). The data includes monthly records, county names, and home-related features such as square footage, with median listing price as the prediction target.

3) The approach
I trained a neural network regression model using Keras with a JAX backend. The model is a simple dense network: one hidden layer and one output layer.

I split data chronologically:
- Training data: rows through 2024-12
- Test data: rows from 2025-01 and later

I normalized feature values, trained for 20 epochs, and evaluated with MAE.

4) How I improved it
My first version was one large script that trained a model and produced one chart.

I improved it by:
- Refactoring into modules (data, modeling, plotting, pipeline, config)
- Adding cleaner data structures for passing data between steps
- Expanding from 1 chart to 4 charts:
  - training history
  - actual vs predicted trend
  - major county comparison
  - estimated utilities by county
- Building a full GUI with start/stop controls, live logs, MAE display, tabbed charts, and reload buttons

What worked:
- Usability and clarity improved a lot. It is much easier to run and explain during a demo.

What did not improve as expected:
- Test MAE changed from about 0.597 to about 0.631 in one run, so model error was slightly worse even though analysis and presentation improved.

5) Live demo plan (what I will do in class)
Step 1: Open the GUI app and explain the buttons and chart tabs.
Step 2: Click Start Model.
Step 3: Show live training logs and point out the final Test MAE value.
Step 4: Open each chart tab and briefly explain what it shows.
Step 5: Highlight one example county trend and what the model got right or wrong.

If something breaks live:
I will explain the expected behavior, show whichever generated plots are available, and describe what the output means.

Short AI partnership statement
I used AI to help refactor the original script into modules, improve code organization, and design the GUI workflow. I verified the output by running the pipeline, checking logs, validating generated plots, and comparing MAE behavior across versions.

Critical thinking and ethics statement
This model has limits. It is trained on one dataset and may not generalize to future market shifts. It can also reflect biases in the source data (for example, uneven county representation). With more time, I would test additional features, try regularization and hyperparameter tuning, and evaluate fairness across county groups.

One-minute spoken version
My project predicts Alabama home prices and presents results in a dashboard-style GUI so the predictions are easier to interpret. I used an Alabama housing CSV with monthly and county-level records, and I trained a Keras neural network regression model with a chronological train-test split. Over time, I moved from a single script to a modular project and expanded from one chart to four charts, plus a GUI with live logs and chart tabs. One thing that improved a lot was usability and interpretability. One thing that did not improve in one run was MAE, which moved from about 0.597 to 0.631, so I can honestly say accuracy still needs tuning. In the demo, I will show that the model gets the overall direction of monthly price movement mostly right and produces reasonable averages for several major counties, but it misses on sharper price jumps and dips and sometimes overestimates or underestimates specific counties.

Pre-demo self-check
- I can explain the goal in one sentence without jargon.
- I can name the dataset and target variable from memory.
- I can describe the model and split in plain language.
- I have one clear improvement example (modularization + GUI + extra plots).
- I have run the full demo flow at least once before class.

Sources
- Realtor Data: https://www.realtor.com/research/data/
- Zillow Research Data: https://www.zillow.com/research/data/
- Redfin Data Center Downloads: https://www.redfin.com/news/data-center/downloads/
- FRED/FHFA House Price Index (Alabama county example): https://fred.stlouisfed.org/series/ATNHPIUS01001A
