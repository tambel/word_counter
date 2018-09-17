from random import choice, randint
from string import ascii_lowercase
from collections import Counter, namedtuple

from pytest import fixture

_TextInfo = namedtuple('FileInfo', ['text', 'counter'])


@fixture(scope='session')
def generate_text():
    def generate(dict_size, word_count) -> namedtuple:
        # generate random words.
        words = [
            ''.join([choice(ascii_lowercase) for _ in range(randint(2, 10))])
            for _ in range(dict_size)
        ]

        # generate text with this words.
        counter = Counter()
        text = list()
        for _ in range(word_count):
            word = choice(words)
            counter[word] += 1
            text.append(word)

        return _TextInfo(' '.join(text), counter)

    return generate
