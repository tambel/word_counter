from distutils.core import setup

setup(
    name='word-counter',
    version='1.0',
    description='Application counts words from all .txt files in given directory(including zip archives).',
    author='Arthur Kamalov',
    url='https://github.com/tambel/word_counter',
    packages=['word_counter'],
    install_requires=[
        'matplotlib',
    ],
    entry_points={
        'console_scripts': ['count_words_in_directory=word_counter.histogram:main'],
    }
)
