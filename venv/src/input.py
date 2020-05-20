import random
from random import choice

def main():
    nucleoids = ["a", "c", "g", "t"]
    pattern = "aaaaaggggg"
    string = ""
    pos = []

    for loop in range(0,10):

        position = random.randint(0,480)
        for j in range(0,490):
            if(j == position):
                string = string + pattern
                j = j + 10
            char = random.choice(nucleoids)
            string = string + char

        with open('input.txt', 'a') as file:
            file.write(string + '\n')

        string = ""


if __name__ == "__main__":
    main()