# Datasets

Two datasets are available - dataset with only *p* tags (called plain)
and dataset with only *p* tags but with the tags inside them not unrolled (called html).
Have a look at them, and it should be obvious. 

Both datasets are available at https://drive.google.com/file/d/1ANgesiUxqrx2oa9Ij21o-3rElxJeNERy/view?usp=sharing

The preprocessing steps are in <code>preprocessing.py</code> - some useless tags get removed
and then only the *p* tags are kept.

The training is done with <code>train.py</code>.