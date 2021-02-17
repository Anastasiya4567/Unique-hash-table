# Chaplianskaya, Czyżkowski
# W14 W21
import sys
import codecs
import datetime

import generator
import hash_table
import arrow


def print_statistics(time_delta, enum_time, words_counter, errors_counter):
    print(f"Enumerate time: {int(enum_time * 1000)} ms")
    create_time = time_delta.total_seconds()
    print(f"Creating time: {int(create_time * 1000)} ms")
    print(f"Errors number: {errors_counter}")
    print(f'Number of words: {words_counter}')


def main():
    errors_counter = 0
    arg_k = 10
    arg_n = 10
    if sys.argv[1] == "help":
        print("Please refer to the readme.txt file in this directory.")
    elif len(sys.argv) >= 4:
        arg_k = arg_k if int(sys.argv[1]) == 0 else int(sys.argv[1])
        arg_n = arg_n if int(sys.argv[2]) == 0 else int(sys.argv[2])
        # read from file
        if sys.argv[3] == "file":
            if len(sys.argv) == 4:
                print("Error! No file name given")
            else:
                words_counter = 0
                words = hash_table.HashTable(arg_k, arg_n)
                try:
                    start_time = arrow.utcnow()
                    with codecs.open(sys.argv[4], "r", encoding='utf-8') as words_file:
                        for line in words_file:
                            line = line[:-1]
                            if line[-1] == '\r':
                                line = line[:-1]
                            if len(line[:-1]) == 0:
                                continue
                            for word in line[:-1].split(" "):
                                try:
                                    words_counter += 1
                                    words.insert_value(word)
                                except Exception: # not enough space to insert the word
                                    errors_counter += 1
                    finish_time = arrow.utcnow()
                    enum_time = words.enumerate_time()
                    print_statistics(start_time, finish_time, enum_time, words_counter, errors_counter)
                except Exception as exception:
                    print(exception)
        # standard input
        elif sys.argv[3] == "input":
            line = str()
            words_in_line = list()
            while True:
                start_time = arrow.utcnow()
                while len(words_in_line) == 0:
                    line = sys.stdin.readline()[:-1]
                    if line[-1] == '\r':
                        line = line[:-1]
                    words_in_line = line.split(" ")
                number_of_words = int(words_in_line[0])
                if number_of_words == 0:
                    break
                words = hash_table.HashTable(arg_k, arg_n)
                words_in_line = words_in_line[1:]
                for i in range(number_of_words):
                    while len(words_in_line) == 0:
                        line = sys.stdin.readline()[:-1]
                        words_in_line = line.split(" ")
                        try:
                            words.insert_value(words_in_line[0])
                        except Exception:
                            errors_counter += 1
                    words_in_line = words_in_line[1:]
                end_time = arrow.utcnow()
                enum_time = words.enumerate_time()
                print_statistics(end_time-start_time, enum_time, number_of_words, errors_counter)
            sys.exit()
        # generate
        elif sys.argv[3] == "gen":
            if len(sys.argv) == 4:
                print("No number of words to generate given")
            else:
                generated_words = generator.generate(int(sys.argv[4]))
                enum_time = 0
                time_delta = datetime.timedelta()
                words = hash_table.HashTable(arg_k, arg_n)
                start_time = arrow.utcnow()
                for word in generated_words:
                    try:
                        words.insert_value(word)
                    except Exception:
                        errors_counter += 1
                end_time = arrow.utcnow()
                enum_time += words.enumerate_time()
                time_delta += end_time - start_time
                print_statistics(time_delta, enum_time, int(sys.argv[4]), errors_counter)
        else:
            print("Incorrect arguments")
            print("Please refer to the readme.txt file in this directory.")
    else:
        print("Incorrect arguments")
        print("Please refer to the readme.txt file in this directory.")


if __name__ == '__main__':
    main()
