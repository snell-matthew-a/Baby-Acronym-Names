This script generates a list of potential 'Backronym' baby names from a list of family members, movie stars, etc. that you want to include.  It returns every name that can be formed by taking 1 letter from each of the source names.

Baby Names are accessed from Data.gov and use the baby names submitted to the Social Security Administration, accessed [here](https://catalog.data.gov/dataset/baby-names-from-social-security-card-applications-national-data).

I've combined each of the `yob1880.txt`, `yob1881.txt` etc. files into tally_names.csv and added up the total occurrences for each name, so it doesn't need to read through names multiple times.  Besides that, most of the commits are just fiddling around with python and updating it to use pandas in a more useful way.
