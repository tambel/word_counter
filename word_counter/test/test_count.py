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
    assert paths == files_checklist


def test_word_count(generate_text):
    random_text1, counter1 = generate_text(100, 1000)
    random_text2, counter2 = generate_text(100, 1000)

    result1 = count_words_in_text(random_text1)
    result2 = count_words_in_text(random_text2)

    assert result1 == counter1
    assert result2 == counter2

