import json
from collections import Counter
from os.path import dirname, join

from pyfakefs.fake_filesystem import FakeFilesystem, FakeOsModule

from word_counter.count import enumerate_files, count_words_in_text, \
    count_files_in_directory


def test_file_enumeration(mocker):
    # creating fake filesystem.
    fake_fs = FakeFilesystem()

    file_list = [
        '/home/archive.zip',
        '/home/text1.txt',
        '/home/text2.txt',
        '/home/not_text.bin',
        '/home/books/book1.txt',
        '/home/books/book2.txt',
        '/home/books/not_text2.bin',
        '/home/books/archive2.zip'

    ]

    # creating files in fake filesystem.

    files_checklist = list()
    for path in file_list:
        fake_fs.create_file(path)
        if path.endswith('.txt') or path.endswith('.zip'):
            files_checklist.append(path)
    # creating and mocking needed fake modules.
    os_module = FakeOsModule(fake_fs)

    # mocking needed modules and functions.
    to_patch = {
        'join': fake_fs.joinpaths,
        'isdir': fake_fs.isdir,
        'os': os_module
    }

    for name, f in to_patch.items():
        mocker.patch('word_counter.count.{}'.format(name), f)

    paths = list(enumerate_files('/'))
    assert Counter(paths) == Counter(files_checklist)


def test_word_count(generate_text):
    text = 'hello world'

    assert count_words_in_text(text) == Counter({'hello': 1, 'world': 1})

    # empty string
    assert count_words_in_text('') == Counter({})

    # zero words text
    assert count_words_in_text(' i 1 f3 . "/;') == Counter({})

    text = "' `s yea' 'don't -yeah no- ice-cream i I O Open  it's a goody-1y day olly's " \
           "free2play a A o i ice can't, won't I'm D R P g6l f1'3p"

    result = count_words_in_text(text)
    assert result == Counter({
        'yea': 1, "don't": 1, 'yeah': 1, 'no': 1, 'ice': 2, 'cream': 1,
        'I': 1, "O": 1, 'open': 1, "it's": 1, 'a': 3, 'goody': 1, 'day': 1,
        "olly's": 1, "can't": 1, "won't": 1, "i'm": 1
    })

    random_text1, counter1 = generate_text(100, 1000)
    random_text2, counter2 = generate_text(100, 1000)

    result1 = count_words_in_text(random_text1)
    result2 = count_words_in_text(random_text2)

    assert result1 == counter1
    assert result2 == counter2


def test_count_directory():
    """
    Apply word counting to test samples and check with pre-counted counter.
    """
    samples_path = join(dirname(__file__), 'samples')
    with open(join(samples_path, 'check_list.txt'), 'r') as file:
        check_counter = Counter(json.load(file))
    counter = count_files_in_directory(join(samples_path, 'folder'))

    assert counter == check_counter
