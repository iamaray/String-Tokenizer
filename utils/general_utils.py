"""
A file with general utilities.
"""


class VocabMergeError(Exception):
    """
    An exception raised when a sub-vocabulary cannot be merged into the overall vocabulary.
    """
    def __init__(self, message):
        self.message = message


def read_txt_file(file_path):
    """
    Reads a text file and returns the contents of the file as a string.
    """
    try:
        with open(file_path, 'r') as file:
            file_data = file.read()
        return file_data
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")


class Maybe:
    """
    Represents a container that may or may not hold a value.

    Attributes:
        _value: The value held by the Maybe container.

    Methods:
        bind(func): Applies a function to the value inside the Maybe container and returns a new Maybe container.
        orElse(default): Returns the Maybe container itself if it holds a value, otherwise returns a new Maybe container with the specified default value.
        unwrap(): Returns the value held by the Maybe container.
        __or__(other): Returns a new Maybe container with the value of either the current Maybe container or the other Maybe container.
        __str__(): Returns a string representation of the Maybe container.
        __repr__(): Returns a string representation of the Maybe container.
        __eq__(other): Checks if the Maybe container is equal to another Maybe container.
        __ne__(other): Checks if the Maybe container is not equal to another Maybe container.
        __bool__(): Checks if the Maybe container holds a value.

    Usage:
        maybe_value = Maybe(10)
        maybe_value.bind(lambda x: x + 5)  # Returns Maybe(15)
        maybe_value.orElse(0)  # Returns Maybe(10)
        maybe_value.unwrap()  # Returns 10
        maybe_value | Maybe(20)  # Returns Maybe(10)
        str(maybe_value)  # Returns 'Just 10'
        repr(maybe_value)  # Returns 'Just 10'
        maybe_value == Maybe(10)  # Returns True
        maybe_value != Maybe(20)  # Returns True
        bool(maybe_value)  # Returns True
    """

    def __init__(self, value):
        self._value = value

    def bind(self, func):
        if self._value is None:
            return Maybe(None)
        else:
            return Maybe(func(self._value))

    def orElse(self, default):
        if self._value is None:
            return Maybe(default)
        else:
            return self

    def unwrap(self):
        return self._value

    def __or__(self, other):
        return Maybe(self._value or other._value)

    def __str__(self):
        if self._value is None:
            return 'Nothing'
        else:
            return 'Just {}'.format(self._value)

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        if isinstance(other, Maybe):
            return self._value == other._value
        else:
            return False

    def __ne__(self, other):
        return not (self == other)

    def __bool__(self):
        return self._value is not None
