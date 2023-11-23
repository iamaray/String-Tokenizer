"""
This file contains the functions that will be used to process the text input
and perform word-level tokenization on the text.
"""

import string
import typing_extensions
import numpy as np
from collections import defaultdict
# from utils import *

# List of common English abbreviations and acronyms
abbreviations = np.array([
    "e.g.",
    "i.e.",
    "etc.",
    "Mr.",
    "Mrs.",
    "Dr.",
    "Jr.",
    "Sr.",
    "U.S.",
    "U.K.",
    "a.m.",
    "p.m.",
    "vs.",
    "etc.",
    "etc.",
    "Ave."
    # Add more abbreviations and acronyms as needed
])

"""
A class representing a vocabulary. This class will be used to represent the
vocabulary.

Attributes:
    vocabulary (typing_extensions.List[WordToken]): A list of WordTokens
        representing the vocabulary.

Methods:

    __init__(self, vocabulary: typing_extensions.List[WordToken]): The
        constructor for the Vocabulary class. The constructor will take in a
        list of WordTokens and set the vocabulary attribute to the input.
    __str__(self): The string representation of the Vocabulary class. The
        string representation will be the string representation of the
        vocabulary.
"""


class Vocabulary(list):
    def __init__(self, vocabulary: list):
        try:
            self.vocabulary = vocabulary
        except:
            self.vocabulary = None

    def mergeSubVocabulary(self, subVocabulary):
        """
        This function will merge a subVocabulary into the vocabulary.
        """
        self.vocabulary = list(
            set.union(set(self.vocabulary), set(subVocabulary.vocabulary)))

    def __str__(self):
        return str(self.vocabulary)

    def __eq__(self, other):
        if isinstance(other, Vocabulary):
            return self.vocabulary == other.vocabulary
        else:
            return False

    def __iter__(self):
        return iter(self.vocabulary)

    def __next__(self):
        return next(self.vocabulary)


class UnknownToken(str):
    def __init__(self) -> None:
        self.id = np.random.random()

    def __str__(self) -> str:
        return f"<UNK> - {self.id}"

    def __repr__(self) -> str:
        return "<UNK>"

    def __eq__(self, other) -> bool:
        return other is UnknownToken and self.id == other.id

    def __lt__(self, __value: str) -> bool:
        return super().__lt__(__value)

    def __hash__(self) -> int:
        return super().__hash__()


def removePunctuation(text: str):
    """
    This function will take in the text input and perform the following
    operations:
    1. Remove all punctuation
    3. Split the text into a list of words
    4. Return the list of words

    Types of punctuation to keep:
        apostrophes for words like "don't" and "can't"
        hyphens for words like "mother-in-law"
        periods for words like "Mr." and 'Mrs."
        commas for numbers like "1,000"
        dollar signs for money amounts like "$1,000"
        percent signs for percentages like "1%"
        ampersands for words like "AT&T"
        at signs for email addresses like "user@example"
        forward slashes for dates like "1/1/2020"
        colons for times like "1:00"

        plus signs for phone numbers like "+1-800-555-1234"   
            (phone numbers are something I'm not sure about, as they are fairly
             unique, so we may not want to tokenize them as their own word... or at all)
    """

    naiveWordLst = text.strip().split()
    punctuation = string.punctuation
    wordLst = []

    # TODO: refactor this absolutely terrible code you piece of shit.
    for word in naiveWordLst:
        sharedPunct = set(word).intersection(set(punctuation))
        setMinus = set(word).difference(sharedPunct)
        # we keep the word only if punctuation is *part* of the word
        if word[len(word) - 1] not in punctuation:
            if word in abbreviations or len(setMinus) != 0:
                wordLst += [word]

        else:
            if word in abbreviations:
                wordLst += [word]
            elif word in punctuation:
                continue
            else:
                wordLst += [word[:len(word)-1]]

    return wordLst


def countWordOccurrences(wordList):
    """
    This function will take in the list of words and count the number of
    occurrences of each word in the list. The function will return a dictionary
    where the keys are the words and the values are the number of occurrences
    of each word.
    """
    wordCount = defaultdict(int)

    for word in wordList:
        wordCount[word] += 1

    return wordCount


def createSubVocabulary(wordCountDict: defaultdict, minFrequency: int, overallVocabulary: Vocabulary):
    """
    Save all words whose frequency is at least minCount to a sub vocabulary.
    """
    # Create a list of words whose frequency is at least minCount
    subVocabulary = [
        word for word in wordCountDict.keys() if wordCountDict[word] >= minFrequency]

    subVocabulary += [UnknownToken() for word in wordCountDict.keys()
                      if word not in subVocabulary]

    # Convert the vocabulary to a numpy array
    subVocabulary = Vocabulary(subVocabulary)

    return subVocabulary


exText = "Hello, my name is bob. I can't walk & I cannot read. What is your name? Where don't you work? I work at\
            AT&T. My phone number is (+1)404-483-9833."

wordList = removePunctuation(exText)
wordOccurences = countWordOccurrences(wordList)
subVocab = createSubVocabulary(wordOccurences, 2, Vocabulary(["help"]))
print(subVocab)
print(type(subVocab))

overalVocab = Vocabulary(["Hello", "there", "how", "are", "you"])
overalVocab.mergeSubVocabulary(subVocab)
print(overalVocab)
