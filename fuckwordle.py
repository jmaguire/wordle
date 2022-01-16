"""I dont like wordle"""

import re
import json
from wordfreq import zipf_frequency

#letter_score = {'e': 138.8, 't': 103.1, 'a': 89.3, 'o': 84.9, 'i': 84.1, 'n': 80.3, 's': 72.3, 'r': 69.8, 'h': 56.1, 'l': 45.2, 'd': 42.4, 'c': 37.1,
#                'u': 30.3, 'm': 27.9, 'f': 26.7, 'p': 23.8, 'g': 20.8, 'w': 18.7, 'y': 18.4, 'b': 16.4, 'v': 11.7, 'k': 6, 'x': 2.6, 'j': 1.8, 'q': 1.3, 'z': 1}

letter_score = {'e': 138.8, 't': 103.1, 'a': 89.3, 'o': 84.9, 'i': 84.1, 'n': 80.3, 's': 72.3, 'r': 69.8, 'h': 56.1, 'l': 45.2, 'd': 42.4, 'c': 37.1,
                'u': 30.3, 'm': 27.9, 'f': 26.7, 'p': 23.8, 'g': 20.8, 'w': 18.7, 'y': 18.4, 'b': 16.4, 'v': 11.7, 'k': 6, 'x': 2.6, 'j': 1.8, 'q': 1.3, 'z': 1}
# counts single occurences of common characters


def count_common_characters(word):
    unique_chrs = ''.join(set(word))
    return sum([letter_score[chr] for chr in unique_chrs])


def count_eliminated_guesses(word, words_to_target):
    unique_chrs = ''.join(set(word))
    return sum([1 for word in words_to_target if any(
        chr in word for chr in unique_chrs)])


words = []
with open('words.json', 'r') as f:
    words = json.load(f)

# common_words = []
# with open('commonwords.json', 'r') as f:
#     common_words = json.load(f)

# Filter characters that don't exist
bad_charaters = list('loesri')

# Filter known characters
known_charaters = list('tan')

# Filter known good positions
regex_good = r"t\w\w\w\w"

# Filter known bad positions
regex_bad = r"[^a]\w[^a]\w[^n]"

# Start search for most likely word
filtered_words = words

# Eliminate bad characters
if bad_charaters:
    filtered_words = [word for word in filtered_words if all(
        chr not in word for chr in bad_charaters)]

# Narrow to good characters
if known_charaters:
    filtered_words = [word for word in filtered_words if all(
        chr in word for chr in known_charaters)]

# Narrow to good characters correct placement
if regex_good:
    filtered_words = [
        word for word in filtered_words if re.match(regex_good, word)]

# Eliminate to good characters incorrect placement
if regex_bad:
    filtered_words = [
        word for word in filtered_words if re.match(regex_bad, word)]

# Sort by english frequency
filtered_words = sorted(filtered_words, key=lambda word: zipf_frequency(
    word, 'en', 'large'), reverse=True)

print('Most Common:', filtered_words[:10])

# Calculate best word to eliminate choices
elimination_words = words
if bad_charaters:
    elimination_words = [word for word in elimination_words if all(
        chr not in word for chr in bad_charaters)]

# Update letter frequency to discount words with seen characters
for (key, value) in letter_score.items():
    if key in known_charaters:
        letter_score[key] = -1

elimination_words = sorted(elimination_words,
                           key=lambda word: count_common_characters(word),
                           reverse=True)
print('Best for elimination:', elimination_words[:10])

# Sorts by how many remaining words can be eliminated
elimination_words = sorted(elimination_words,
                           key=lambda word: count_eliminated_guesses(
                               word, filtered_words),
                           reverse=True)
print('Best for elimination2:', elimination_words[:10])
