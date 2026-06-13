Questions I asked My Study Buddy

Q: How is "Hot/Cold" related to gradient descent?

3:00 PM
A: Per the corrected answer key (Module2_Quiz.md, Q8): D) Both use "warmer or colder" feedback to choose the next step.

The non-technical reading lays out the connection directly. In the Hot/Cold game, you take a step, someone tells you "warmer" or "colder," and you keep stepping toward warmer — that's the only feedback you need.

Gradient descent works the same way:

A "step" = a small nudge to the network's dials (weights/biases)
"Warmer or colder" = whether that nudge made the loss (wrongness) better or worse — this is the gradient
You repeat: nudge, check warmer/colder, nudge again toward warmer
Two extra details from the reading map onto this too:

Step size ("learning rate") — too big and you overshoot the warm spot; too small and you crawl.
Local minimum — a "pretty warm" spot you can get stuck in that isn't the warmest spot in the room.
And backpropagation is just the trick that computes "warmer/colder" for all 13,000 dials simultaneously, instead of one at a time.

Want to try the physical Hot/Cold exercise from Section 4 of the reading, or move to Q9/Q10 (the "confident and wrong" items)?







Q: Why, when teaching to recognize "Image A or B", do we need three states that we train the model to recognize?

3:02 PM
A: Per the answer key (Module2_Quiz.md, Q9): C) With only two choices, the model must force any input into A or B.

The full reasoning given: "With only two classes the model can't say "neither," so out-of-place inputs get a confident wrong label. A third "background" class gives it an honest "none of these.""

This connects directly to the Teachable Machine activity in the non-technical reading — Section 5 specifically has you add a third class with only 3-4 blurry examples and watch the model get confused,
 then show it something untrained (your face, a coffee mug) and watch it still confidently pick "Thumbs Up" or "Thumbs Down" because those are the only answers it has.

That sets up Q10 nicely — want to tackle that one next? It's the "confidently labels a random object" question, and it ties back to the digit-recognition noise test from Part 1 of the Neural Networks summary.





Q: What skills and workflows do I personally (the student running this prompt) need to develop, in order to work with Python notebooks?

3:04 PM
That one isn't directly answered in your uploaded materials as a personal skill list — but the Bonus question (Module2_Quiz.md) gives the baseline starting point:

Bonus answer: B) Running the cells in order and reading what each one prints.

The answer key calls this "notebook literacy" — that's the foundational workflow.

Beyond that single line, I don't have material in your uploads that lays out a fuller personal skills roadmap for notebooks specifically. The closest related content is Chapter2.md, 
which walks through the actual MNIST notebook code (loading data, building the model, compiling, training with .fit(), 
evaluating with .predict()) — so working through that chapter cell-by-cell, in order, watching what each step prints 
(shapes, loss, accuracy), would be the practical application of "notebook literacy."

If you want, I can walk you through Chapter2.md's code in the order it would appear in a notebook, 
and we can talk through what to expect printed at each cell — that would be a concrete way to build the skill rather than just naming it. Want to do that?