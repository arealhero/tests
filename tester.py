#!/usr/bin/env python3

import sys
import os

import json
import random
import re

test = "philosophy"

with open(f'{test}.json', 'r') as file:
    data = json.load(file)

def print_correct(question):
    choices = question['choices']
    correct = question['correct']
    print(f'----\n {correct}. {choices[correct-1]}')


def print_question(question, number=None, show_correct=False):
    decoded = question['question'].replace('\\n', '\n')
    prefix = f'{number}. ' if number else ''
    print(prefix + decoded)
    choices = question['choices']
    for i in range(len(choices)):
        choice = choices[i]
        print(f' {i+1}. {choice}')

    if show_correct:
        print_correct(question)


def show_random_questions():
    while True:
        shown_questions = 0
        correct_answers = 0

        try:
            questions = data['questions']
            random.shuffle(questions)
            for question in questions:
                print_question(question)
                print('----')
                answer = int(input(' '))
                if answer == question['correct']:
                    print('Yes!')
                    correct_answers += 1
                else:
                    correct = question['correct']
                    print(f'----\n {correct}. {question["choices"][correct-1]}')
                print()
                shown_questions += 1
        except KeyboardInterrupt:
            percents = int(round(correct_answers / shown_questions * 100))
            print(f'\n----- \nResults: {correct_answers}/{shown_questions} ({percents}%)')
            break

        print(f'\n----- \nResults: {correct_answers}/{shown_questions}, press Enter to start again\n')
        input()

def read_questions():
    while True:
        question = input('question: ')

        i = 1
        choices = []
        while i != 5:
            choice = input(f'{i}. ')
            if len(choice) == 0:
                break

            choices.append(choice)
            i += 1

        while True:
            correct = int(input('correct: '))

            obj = {
                'question': question,
                'choices': choices,
                'correct': correct,
            }

            print_correct(obj)

            answer = input()
            if len(answer) == 0:
                break

        data['questions'].append(obj)

        with open(f'{test}.json', 'w') as file:
            json.dump(data, file)

def find_questions():
    while True:
        regex = input('Enter regex: ')
        questions = data['questions']
        for question in questions:
            match = re.search(regex, question['question'])
            if match:
                print_question(question, show_correct=True)
                print('\n')

def print_all_questions():
    questions = data['questions']
    for i in range(len(questions)):
        question = questions[i]
        print_question(question, number=i+1, show_correct=True)
        print('\n')

def main():
    print('1. show random questions')
    print('2. insert new questions')
    print('3. find questions')
    print('4. print all questions')
    choice = int(input('choice: '))

    print()
    if choice == 1:
        show_random_questions()
    elif choice == 2:
        read_questions()
    elif choice == 3:
        find_questions()
    elif choice == 4:
        print_all_questions()
    else:
        print('unknown choice')

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nProgram was interrupted, exiting...')
        try:
            sys.exit(130)
        except SystemExit:
            os._exit(130)
