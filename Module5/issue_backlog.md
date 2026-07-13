ok here's my 5 issues for the walking skeleton. this is basically "what does the first working version look like" — not the good version, just the RUNNING version. writing these before i start so i don't just wing it.


Issue 1: load the csv and make sure it's not garbage

gotta read alabama_housing.csv in and actually check it before i trust it.


make sure the number columns are actually numbers and not text
check if anything's missing (some of the early rows looked kinda sparse on stuff like median_days_on_market and price_reduced_count, need to double check)
print the shape and make sure it's 6,902 rows like i already confirmed, spanning 201607 to 202606


done when: data loads without weirdness and i've actually looked at whether anything's missing (even if the answer is "nope, clean")


Issue 2: do the date split (NOT a random split)

this is the important one. train = everything <=202412, test = everything >=202501. no shuffling across that line or i defeat the whole point of doing this the right way.

done when: i get exactly 5,711 train rows and 1,191 test rows. if i don't get those numbers something broke and i need to fix it before moving on, not just shrug


Issue 3: normalize the features + build a dumb baseline

normalize the numeric columns using ONLY the training data's mean/std (learned this the hard way from the housing example — you don't get to peek at test data stats). then build the dumbest possible baseline — either "just guess the average price" or "just guess whatever that county's price was last time" — and get its MAE.

done when: i have an actual baseline MAE number written down somewhere. this is the number i have to beat, not a vibe


Issue 4: actually build the model and get it training

small keras model, 1-2 dense layers, adam + mse + mae like everything else in this course. doesn't need to be good yet, just needs to run start to finish without exploding.

done when: model.fit() runs and finishes and i have an actual trained model, even if it's mid


Issue 5: test it for real and write down what happened

run the trained model on the 202501-202606 test set (the stuff it's never seen). get the MAE. compare it to my baseline from issue 3. put the honest result in reflection.md — did it beat the baseline or not, no fudging it.

done when: i can say a real number and say whether it's actually better than the dumb baseline or not