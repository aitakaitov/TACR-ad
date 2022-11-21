# Datasets

Two datasets are available - dataset with only *p* tags (called plain)
and dataset with only *p* tags but with the tags inside them not unrolled (called html).
Have a look at them, and it should be obvious. 

Both datasets are available at https://drive.google.com/file/d/1ANgesiUxqrx2oa9Ij21o-3rElxJeNERy/view?usp=sharing

The preprocessing steps are in <code>preprocessing.py</code> - some useless tags get removed
and then only the *p* tags are kept.

The training is done with <code>train.py</code>.

There are some 17 700 positive examples and some 64 000 negative examples.

# Trained model

The trained model WandB run: https://wandb.ai/aitakaitov/ads/runs/nqz86mee

The trained model files: https://drive.google.com/file/d/1h043TSe9q9HLYZo60LgnPS9c8wulktyh/view?usp=sharing

Model checkpoints for 1st and 2nd epochs: https://drive.google.com/file/d/1UtP6bPpoFJGtwDTmxfc5S9bqK68-cf5w/view?usp=sharing

Class 0 == not an ad, class 1 == ad

The training examples were truncated to 512 tokens.

# Preprocessing comments

In the HTML files the keyword "reklama" was present in a number of sites, both with ads being the subject of the article and not. Some articles just have ads at the beginning with a paragraph with just the word "Reklama". Since that could be a problem, I'm mentioning it here. It could be worth it to just remove all the occurences of this keyword, but the F1 score turned out alright, and the cleaning and retraining is a matter of a few hours.
