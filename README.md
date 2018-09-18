# Word Counter App

#### It is a python program that counts words in all ```.txt``` files in given directory including ```.txt``` files in ```zip``` archives.
#### NOTE: project counts all words including single letter words and words with apostrophes, also it discards words with digits.


<p align="center">
  <img src="https://raw.githubusercontent.com/tambel/word_counter/master/screenshot.jpg">
</p>


## How to install
1. Clone the project:
```shell
git clone https://github.com/tambel/word_counter.git
cd word_counter
```

2. Install it with command:
```shell
pip install .
```

## How to run
```shell
count_words_in_directory <path_to_folder>
```
For example you can use it on testing samples:
```shell
count_words_in_directory <project root folder>/test/samples/folder
```

## Run tests

Switch to project root folder and run command:
```shell
python setup.py test
```
