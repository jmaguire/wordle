import re
from wordfreq import zipf_frequency

words = []

with open('words_dictionary.txt', 'r') as file:
    words = file.readlines()
    words = [word.rstrip() for word in words]
    words = [word for word in words if len(word) == 5]

# Filter characters that don't exist
bad_charaters = list('reinmaokf')

# Filter known characters
known_charaters = list('sl')

# Filter known good positions
regex_good = r"\wlush"

# ## Filter known bad positions
regex_bad = r"[^sl]\w[^s]\w[^ls]"

if bad_charaters:
    filtered_words = [word for word in words if all(
        chr not in word for chr in bad_charaters)]

if known_charaters:
    filtered_words = [word for word in filtered_words if all(
        chr in word for chr in known_charaters)]

if regex_good:
    filtered_words = [
        word for word in filtered_words if re.match(regex_good, word)]

if regex_bad:
    filtered_words = [
        word for word in filtered_words if re.match(regex_bad, word)]

# Sort by english frequency
filtered_words = sorted(filtered_words, key=lambda word: zipf_frequency(
    word, 'en', 'large'), reverse=True)

print(filtered_words)
