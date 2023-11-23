"""
The actual word-level tokenization is performed here.
"""

from .word_utils import *
from utils.general_utils import *


def word_level_tokenize(text: str, overallVocab: Vocabulary):
    """
    Tokenizes the input text into a list of WordTokens.

    Args:
        text (str): The text to tokenize.
        vocabulary (Vocabulary): the overall vocabulary.

    Returns:
        A list of WordTokens representing the tokens in the input text.
    """

    try:
        overallVocab.mergeSubVocabulary(
            Maybe(text)
            .bind(removePunctuation)
            .bind(countWordOccurrences)
            .bind(createSubVocabulary))
    except:
        raise VocabMergeError(
            "Could not merge sub-vocabulary into overall vocabulary.")
