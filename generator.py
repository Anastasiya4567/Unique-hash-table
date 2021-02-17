# Chaplianskaya, Czyżkowski
# W14 W21

import requests
import re
import random
import time


initialized = False
first_letters_distribution = None
next_letters = None


def create_next_letters(letter, next_letter, next_letters):
    if letter in next_letters:
        if next_letter in next_letters[letter]:
            next_letters[letter][next_letter] += 1
        else:
            next_letters[letter][next_letter] = 1
    else:
        next_letters[letter] = dict()
        next_letters[letter][next_letter] = 1


def lazy_init():
    global first_letters_distribution, next_letters, initialized
    url = "https://wolnelektury.pl/media/book/txt/pan-tadeusz.txt"
    res = requests.get(url)

    polish_text_words = list()
    text_letters = list()
    first_letters = dict()

    text = res.text.lower()
    text = (re.sub('[^a-ząęóżźćśłń]+', ' ', text))
    for word in text.split():
        for letter in word:
            if letter not in text_letters:
                text_letters.append(letter)
        polish_text_words.append(word)
    for word in polish_text_words:
        if word[0] in first_letters:
            first_letters[word[0]] += 1
        else:
            first_letters[word[0]] = 1

    for letter in first_letters:
        first_letters[letter] /= len(polish_text_words)

    first_letters_distribution = list()
    for letter in first_letters:
        first_letters_distribution.append((letter, first_letters[letter]))
    for index in range(len(first_letters_distribution)):
        if index != 0:
            first_letters_distribution[index] = (first_letters_distribution[index][0],
                                                 first_letters_distribution[index][1] +
                                                 first_letters_distribution[index - 1][1])
        if index == len(first_letters_distribution) - 1:
            first_letters_distribution[index] = (first_letters_distribution[index][0], 1)

    next_letters = dict()
    empty = ' '

    for word in polish_text_words:
        for index in range(len(word)):
            if index < len(word) - 1:
                create_next_letters(word[index], word[index + 1], next_letters)
            else:
                create_next_letters(word[index], empty, next_letters)
    for letter in next_letters:
        letter_count = text.count(letter)
        probabilities = list()
        for index in next_letters[letter]:
            next_letters[letter][index] /= letter_count
            probabilities.append((index, next_letters[letter][index]))
        for index in range(len(probabilities)):
            if index != 0:
                letter_ = probabilities[index][0]
                value = probabilities[index][1]
                probabilities[index] = (letter_, value + probabilities[index - 1][1])
            if index == len(probabilities) - 1:
                probabilities[index] = (probabilities[index][0], 1)
        next_letters[letter] = probabilities
    random.seed()
    initialized = True


def generate(number_of_words):
    global first_letters_distribution, next_letters, initialized
    if not initialized:
        lazy_init()
    gen_words = list()
    for i in range(number_of_words):
        word = ""
        random_number = random.random()
        for tup in first_letters_distribution:
            if tup[1] >= random_number:
                word += tup[0]
                break
        word_finished = False
        while not word_finished:
            random_number = random.random()
            for tup in next_letters[word[len(word)-1]]:
                if tup[1] >= random_number:
                    if tup[0] == ' ':
                        word_finished = True
                        break
                    word += tup[0]
                    break
        gen_words.append(word)
    return gen_words
