import os
import re
from os.path import isdir, join
from collections import Counter
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
    counter = Counter()
    with ZipFile(path, 'r') as file:
        for child in file.filelist:
            if child.is_dir():
                continue

            if child.filename.endswith('.zip'):
                text = BytesIO(file.read(child.filename))
                counter.update(count_words_in_zip(text))
            elif child.filename.endswith('.txt'):
                text = file.read(child.filename)
                counter.update(
                    count_words_in_text(text.decode())
                )

    return counter

