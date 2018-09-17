import os
import re
from os.path import isdir, join
from collections import Counter, OrderedDict
from zipfile import ZipFile
from io import BytesIO


def count_words_in_text(text):
    """
    Search words with regex and count with Counter.
    """
    return Counter(
        # find all words with length bigger than 2.
        word.lower() for word in re.findall('\\w{2,}', text)
    )


def enumerate_files(path: str):
    """
        Generator. Search text files and zip archives recursively
        """
    for child_name in os.listdir(path):
        full_path = join(path, child_name)
        if isdir(full_path):
            for sub_file_path in enumerate_files(full_path):
                yield sub_file_path
            continue
        if child_name.endswith('.txt') or child_name.endswith('.zip'):
            yield full_path


def count_words_in_zip(path):
    """
    Read all .txt files from zip-file and count words.
    If nested file found, read it recursively.
    """
    counter = Counter()
    with ZipFile(path, 'r') as file:
        for child in file.filelist:
            if child.filename.endswith('/'):
                continue

            if child.filename.endswith('.zip'):
                # we need to read nested zip file data and
                # open it as bytes stream
                nested_zip_data = file.read(child.filename)
                nested_zip_stream = BytesIO(nested_zip_data)
                counter.update(count_words_in_zip(nested_zip_stream))
            elif child.filename.endswith('.txt'):
                text = file.read(child.filename)
                counter.update(
                    count_words_in_text(text.decode())
                )

    return counter


def count_files_in_directory(path):
    counter = Counter()
    for file_path in enumerate_files(path):
        if file_path.endswith('.txt'):
            with open(file_path, 'r') as file:
                text = file.read()
                counter.update(
                    count_words_in_text(text)
                )
            continue
        counter.update(
            count_words_in_zip(file_path)
        )
    return OrderedDict(counter.most_common())
