"""I dont like wordle"""

import re
import math
import json
from collections import Counter
from wordfreq import zipf_frequency

# # counts single occurences of common characters
# def count_common_characters(word):
#     unique_chrs = ''.join(set(word))
#     return sum([letter_score[chr] for chr in unique_chrs])

# TRY ROATE


def count_eliminated_guesses(word, words_to_target, bad_chars=''):
    """Count how many target words contain characters from the given word"""
    word = word.translate({ord(c): None for c in bad_chars})
    unique_chrs = ''.join(set(word))
    return sum([1 for word in words_to_target if any(
        chr in word for chr in unique_chrs)])


def common_letters(word, target):
    """Count letters in common"""
    in_common = Counter(word) & Counter(target)
    return math.sqrt(sum(in_common.values()))


def count_eliminated_guesses2(word, words_to_target, bad_chars=''):
    """Count how many letters a word has incommon with the corpus"""
    word = word.translate({ord(c): None for c in bad_chars})
    return sum([common_letters(word, target) for target in words_to_target])


# Load data
words = []
with open('answer-list.json', 'r', encoding='utf-8') as f:
    words = json.load(f)
words_count = len(words)
print("Loaded:", words_count, "answers")

elimination_words = []
with open('guess-list.json', 'r', encoding='utf-8') as f:
    elimination_words = json.load(f)
print("Loaded:", len(elimination_words), "guesses")

# Run constraints

# Filter characters that don't exist
bad_charaters = list('')

# Filter known characters
known_charaters = list('')

# Filter known good positions
# r"\w\w\w\w\w"
regex_good = r"\w\w\w\w\w"

# Filter known bad positions
# r"\w\w\w\w\w"
regex_bad = r"\w\w\w\w\w"

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
    word, 'en', 'best'), reverse=True)

words_left_count = len(filtered_words)
print('Words left:', '{:.2%}'.format(words_left_count/words_count))
print('Best Guess:', filtered_words[:10])

# Calculate best word to eliminate choices
# Remove words with invalid characters so we only eliminate remaining guesses
if bad_charaters:
    elimination_words = [word for word in elimination_words if all(
        chr not in word for chr in bad_charaters)]

# # Update letter frequency to discount words with seen characters
# for (key, value) in letter_score.items():
#     if key in known_charaters:
#         letter_score[key] = -1
#
# elimination_words = sorted(elimination_words,
#                            key=lambda word: count_common_characters(word),
#                            reverse=True)
# print('Best for elimination:', elimination_words[:10])

# Sorts by how many remaining words can be eliminated
chars_to_remove = ''.join(known_charaters + bad_charaters)

# Get top words
elimination_words = sorted(elimination_words, key=lambda word: zipf_frequency(
    word, 'en', 'large'), reverse=True)

elimination_words = sorted(elimination_words,
                           key=lambda word: count_eliminated_guesses2(
                               word, filtered_words, chars_to_remove),
                           reverse=True)
print('Best for elimination:', elimination_words[:10])
