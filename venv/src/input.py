import random
from random import choice

def main():
    nucleoids = ["a", "c", "g", "t"]
    pattern = "aaaaaggggg"
    string = ""
    pos = []

    for loop in range(0,10): #10 kere dnaya yeni pattern satır satır eklemesi yapılacak.

        #bu kısım patternda random 4 yeri değiştirebilemk için.
        for j in range(0,4):

            if (j == 0): #en başta random bir yer seçilir.
                position = random.randint(0,9)
                pos.append(position) #hangi pozisyon değiştirildi tutulur.
            else: #hiç bir zaman aynı yeri değiştirmesin diye.
                position = choice([i for i in range(0,9) if i not in pos])
                pos.append(position)

            #patternda random seçilen pozisyona gidilip oradaki karakter değiştirilir.
            for k in range(0,len(pattern)):
                if (k == position):
                    char = random.choice(nucleoids)
                    while pattern[position] == char:
                        char = random.choice(nucleoids)
                    pattern = pattern[:position]+char+pattern[position+1:]
                    break

        pos.clear() #tüm posizyonlar silindi.
        position = random.randint(0,480) #bu pozizyon dnada random yer seçebilmek için.
        for j in range(0,490): #490 boyutunda random dna oluşturdu.
            if(j == position): #dnada patternın ekleneceği random yere glince dnaya eklendi.
                string = string + pattern
                j = j + 10 #boyutu kadar 10 atlandı.
            char = random.choice(nucleoids)
            string = string + char

        #texte yazdırıldı.
        with open('input.txt', 'a') as file:
            file.write(string + '\n')

        string = "" #string resetlendi.
        pattern = "aaaaaggggg" #pattern kendi resetlendi.


if __name__ == "__main__":
    main()