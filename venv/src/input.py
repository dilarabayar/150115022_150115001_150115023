import random
from random import choice

def main():
    nucleoids = ["a", "c", "g", "t"]
    pattern = "aaaaaggggg"
    string = ""
    pos = []

    for loop in range(0,10):

        for j in range(0,4):

            if (j == 0):
                position = random.randint(0,9)
                pos.append(position)
            else:
                position = choice([i for i in range(0,9) if i not in pos])
                pos.append(position)

            for k in range(0,len(pattern)):
                if (k == position):
                    char = random.choice(nucleoids)
                    while pattern[position] == char:
                        char = random.choice(nucleoids)
                    pattern = pattern[:position]+char+pattern[position+1:]
                    break
        print("yeni pattern: ", pattern)
        pos.clear()
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
        pattern = "aaaaaggggg"


if __name__ == "__main__":
    main()