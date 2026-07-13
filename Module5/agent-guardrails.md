agent-guardrails.md

ok so this is basically the rules for my AI partner so it doesn't go rogue on my Alabama housing project. writing this before I actually start coding bc that's the whole point lol

what it CAN do without asking me


explain stuff / help me understand errors
write small chunks of code (like one function at a time), not whole files out of nowhere
suggest fixes when something breaks
help me debug why my train/test split isn't matching the numbers I already confirmed (5,711 / 1,191 — if it doesn't match that, something's wrong)
point out if I'm about to do something dumb like normalize using the test set stats (no)


what it has to ASK me first before doing


changing my train/test split logic. i already locked in the date cutoff (<=202412 train, >=202501 test) and confirmed the row counts myself. if the AI thinks that split is wrong it needs to tell me WHY, not just change it
adding new features / dropping columns i didn't mention
messing with the model architecture in a big way (like going from 1-2 dense layers to something way more complicated). small tweaks fine, full rewrite = ask first
touching charter.md, issue_backlog.md, or reflection.md content without me reviewing it — those are MY decisions written down, not something to auto-edit


stuff it should NEVER do


just merge stuff or act like it has repo access it doesn't
make up accuracy numbers or pretend a model ran when it didn't
tell me my baseline is "good enough" — that's my call based on the charter, not something to auto-approve
change the definition of "good enough" from the charter without me saying so out loud first


how i'm checking its work (since i'm solo)

no partner to review my PRs so i'm doing self-review, in writing, in the PR description. basic rule: if the AI wrote or suggested something, I have to be able to explain WHY it works in my own words before I merge it. if I can't explain it, I don't merge it yet — i ask more questions first.

One Change Rule applies here too. one thing at a time, see what happens, THEN change the next thing. no "let's fix five things at once and hope."

thats it. keep it on task, keep it honest, don't let it just do whatever.