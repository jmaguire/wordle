"""I dont like wordle"""
from timeit import default_timer as timer
import re
import math
import json
from collections import Counter
from wordfreq import zipf_frequency
import multiprocessing
from multiprocessing.pool import ThreadPool
import itertools
import sys


# TRY ROATE
def split(a, n):
    k, m = divmod(len(a), n)
    return (a[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(n))


def common_letters(word, target):
    """Count letters in common"""
    return len(set(word) & set(target))


def eliminated(word, target):
    """Count letters in common"""
    common_letters = len(set(word) & set(target))
    common_positions = sum(
        [1 if word[i] == target[i] else 0 for i in range(5)])
    return common_letters + common_positions


def score_guesses_loop(my_guesses, my_answers):
    my_scores = {}
    for guess in my_guesses:
        score = [eliminated(guess, word)
                 for word in my_answers]
        my_scores[guess] = sum(score)
    return my_scores


def score_guesses(my_guesses, my_answers, my_scores={}):
    if len(my_guesses) == 0:
        return my_scores
    guess = my_guesses[0]
    my_scores[guess] = sum([common_letters(guess, word)
                           for word in my_answers])
    return score_guesses(my_guesses[1:], my_answers, my_scores)


sys.setrecursionlimit(15000)
if __name__ == '__main__':
    sys.setrecursionlimit(15000)
    # Load data
    answers = []
    with open('answer-list.json', 'r', encoding='utf-8') as f:
        answers = json.load(f)
    words_count = len(answers)
    print("Loaded:", words_count, "answers")

    guesses = []
    with open('guess-list.json', 'r', encoding='utf-8') as f:
        guesses = json.load(f)
    print("Loaded:", len(guesses), "guesses")

    # Run constraints

    # Filter characters that don't exist
    bad_charaters = list('')

    # Filter known characters
    good_characters = list('')

    # Filter known good positions
    # r"\w\w\w\w\w"
    good_places = r"\w\w\w\w\w"

    # Filter known bad positions
    # r"\w\w\w\w\w"
    bad_places = r"\w\w\w\w\w"

    # Eliminate bad characters
    if bad_charaters:
        answers = [word for word in answers if all(
            chr not in word for chr in bad_charaters)]

    # Narrow to good characters
    if good_characters:
        answers = [word for word in answers if all(
            chr in word for chr in good_characters)]

    # Narrow to good characters correct placement
    if good_places:
        answers = [
            word for word in answers if re.match(good_places, word)]

    # Eliminate to good characters incorrect placement
    if bad_places:
        answers = [
            word for word in answers if re.match(bad_places, word)]

    # Sort by english frequency
    answers = sorted(answers, key=lambda word: zipf_frequency(
        word, 'en', 'best'), reverse=True)

    words_left_count = len(answers)
    print('Words left:', '{:.2%}'.format(words_left_count/words_count))
    print('Best Guess:', answers[:10])

    # Calculate best word to eliminate choices
    # Remove words with invalid characters so we only eliminate remaining guesses
    if bad_charaters:
        guesses = [word for word in guesses if all(
            chr not in word for chr in bad_charaters)]

    # Get top words
    # Characters that we already know about and do not reduce entropy
    process_count = 8
    parameters = []
    for guess_chunk in split(guesses, process_count):
        print(len(guess_chunk))
        parameters.append((guess_chunk, answers))

    with multiprocessing.Pool(processes=process_count) as pool:
        start = timer()
        results = pool.starmap(score_guesses_loop, parameters)
    scores = {k: v for d in results for k, v in d.items()}

    scores = sorted(scores,
                    key=scores.get,
                    reverse=True)
    end = timer()
    print('Multiprocess', end - start)
    print('Best for elimination:', scores[:3])
