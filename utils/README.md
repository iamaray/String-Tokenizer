# Word-Level Tokenization

A very simple word-level tokenizer that accepts text data and generates word-level tokens. The word tokens are then
saved to a 'sub-vocabulary' with the top-$K$ most common words (the less common words are identified with OOV tokens). This sub-vocabulary is then merged into an overall vocabulary.

## Processing Text Input

An incoming string of $n$ words is stripped of any punctuation and converted into a $1 \times n$ array,
where each entry is a single word token. For example, consider the following: $$ \text{"Hi, how are you?"} $$ becomes $$ \text{["Hi", "how", "are", "you"]}. $$

## Structuring Output

The tokenizer maps each word to its use frequency. The output is then another $1 \times n$ array with
the top-$K$ most frequently occurring words, replacing the rare words with the remaining words
replaced with unknown tokens.
