from setuptools import setup

tests_require = [
    'pytest',
    'pyfakefs',
    'pytest-mock',
]

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
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=tests_require,
    entry_points={
        'console_scripts': ['count_words_in_directory=word_counter.histogram:main'],
    },
    extras_require={
        'testing': tests_require,
    },
)
