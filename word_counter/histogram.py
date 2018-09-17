import argparse
import matplotlib
import logging
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

from word_counter.count import count_files_in_directory


def view_histogram(data):
    labels, values = zip(*data.items())
    matplotlib.rcParams['toolbar'] = 'None'  # disabling toolbar
    # creating figure.
    fig, ax = plt.subplots(1, 1)
    fig.set_size_inches(12, 8)
    plt.subplots_adjust(bottom=0.2)
    fig.canvas.set_window_title('Word count.')

    step_size = 10
    current = 0
    size = len(data)

    # update figure.
    def update():
        ax.clear()
        sub_label = labels[current: current + step_size]
        sub_values = values[current: current + step_size]
        indices = [i for i in range(10)]

        ax.bar(indices, sub_values)

        ax.set_xticks(indices)
        ax.set_xticklabels(sub_label)
        showed_size = current + step_size
        if showed_size >= size:
            showed_size = current + (size - current)
        ax.set_title("{}-{} of {}".format(current, showed_size, size))
        plt.draw()

    def to_next_page(_):
        nonlocal current
        if current + step_size >= size:
            return
        current += step_size
        update()

    def to_prev_page(_):
        nonlocal current
        if current == 0:
            return
        current -= step_size
        update()

    # buttons to navigate through histogram.
    next_button = Button(plt.axes([0.81, 0.05, 0.1, 0.075]), 'Next')
    next_button.on_clicked(to_next_page)
    previous_file = Button(plt.axes([0.7, 0.05, 0.1, 0.075]), 'Previous')
    previous_file.on_clicked(to_prev_page)

    update()
    plt.show()


def main():
    """
    Entry point for console command - count_words_in_directory
    """
    logging.basicConfig(format='%(levelname)s: %(message)s')
    parser = argparse.ArgumentParser()
    parser.add_argument('path')
    args = parser.parse_args()
    counter = count_files_in_directory(args.path)
    view_histogram(counter)
