#!/usr/bin/env python3
import random

print('Welcome to Guess the Number!')
low,high=1,100
secret=random.randint(low,high)
tries=0
while True:
    try:
        guess=int(input(f'Guess a number between {low} and {high}: '))
    except ValueError:
        print('Please enter a valid integer.')
        continue
    tries+=1
    if guess<secret:
        print('Too low!')
    elif guess>secret:
        print('Too high!')
    else:
        print(f'Correct! You took {tries} guesses.')
        break
