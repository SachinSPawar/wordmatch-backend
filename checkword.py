import string
import random
from random import seed
from random import randint

vowels="aeiou"
consonants="abcdefghijklmnopqrstuvwxyz"

def checkword(word,characters):

    word= word.upper()
    characters=characters.upper()
    letters = {}   

    for c in word:
        letters[c]=1

    for c in characters:
        if c in letters:
            del letters[c]

    if not letters:
        return checkIfEnglishWord(word)
    else:
        return False

def checkIfEnglishWord(word):
    f = open('words.txt', 'r')
    x = f.readlines()
    f.close()

    x = map(lambda s: s.strip(), x)

    if word.upper() in x:
        return True
    else:
        return False

def getRandomLetters(numberOfCharacters):
    global vowels
    global consonants
    characters=""

    for _ in range(numberOfCharacters/3):
        value = randint(0, len(vowels)-1)
        characters = characters+vowels[value]
    
    for _ in range(2*numberOfCharacters/3):
        value = randint(0, len(consonants)-1)
        characters = characters+consonants[value]
    print "characters : "+characters
    return characters

def calculateScore(words,chars):
    if words:
        return len(words)
    else:
        return 0