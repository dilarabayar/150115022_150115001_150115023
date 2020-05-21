#Dilara Bayar 150115022 Sahra Bekli 150115023 İncilay Dikbıyık 150115001
import random
from random import choice

def randomizedmotifsearch(dna,motifsize,motiflength):
    counter = 0
    motifs = [None] * motifsize
    best_motifs = [None] * motifsize
    allsubstrings = [None] * motifsize
    best_score = 0
    denominator = 0
    count = 0

    #her sıradan random 10mer seçiyor. motife atıyor.
    for i in range(0, len(dna)):
        rndkmer = random.choice(findsubstring(dna[i], motiflength))
        motifs[i] = rndkmer

    best_motifs = motifs.copy()

    while True:
        count, denominator = construct_count(motifs)
        profile_array = profile(count, denominator)
        #dnada dizin dizin en iyi sonucu veren kmer bulunuyor. motif bu kmer ile değiştiriliyor.
        for i in range(0, len(dna)):
            substring = findsubstring(dna[i], 10).copy()
            element = probability_randomized(substring, profile_array)
            del motifs[i]
            motifs.insert(i, element)

        #eğer sonuç ilkinden daha iyiyse devam
        if (score(motifs) < score(best_motifs)):
            best_motifs = motifs.copy()
            counter = counter + 1
        #sonuç ilkinden kötüyse bitir.
        else:
            print("Best score found in ", counter, ". iteration and score is ", score(best_motifs))
            for i in range(0, len(best_motifs)):
                print(best_motifs[i])
            return


def gibbsampler(dna,motifsize,motiflength,iteration):
    motifs = [None] * motifsize
    best_motifs = [None] * motifsize
    current_score = 0
    best_score = 0
    denominator = 0
    count = 0

    for i in range(0, len(dna)):
        rndkmer = random.choice(findsubstring(dna[i],motiflength))
        motifs[i] = rndkmer

    best_motifs = motifs.copy()

    for i in range(0, iteration):
        row = random.randint(0, motifsize-1)  # random bir motif seçilmesi belirleniyor.
        del motifs[row]   #seçilen rowu siliyorum.
        count, denominator = construct_count(motifs)
        profile_array = profile(count, denominator)
        selected_motif = probability_gibbs(findsubstring(dna[row],motiflength), profile_array)
        motifs.insert(row, selected_motif)
        if (score(motifs) < score(best_motifs)):
            best_motifs = motifs.copy()

    print("Motifs that has best score is: ", score(best_motifs))
    for i in range(0, len(best_motifs[0])):
        print(best_motifs[i])

def score(motifs):
    score = 0
    nucleoid = [0] * 4

    for i in range(0,len(motifs[0])):
        for j in range(0,len(motifs)):
            if (motifs[j][i] == 'a'):
                nucleoid[0] += 1
            elif (motifs[j][i] == 'c'):
                nucleoid[1] += 1
            elif (motifs[j][i] == 'g'):
                nucleoid[2] += 1
            elif (motifs[j][i] == 't'):
                nucleoid[3] += 1
        #score columndaki tüm nucleoid sayıları toplamından maximum olan nükleoidin çıkarılmasıyla bulunur.
        score = score + (sum(nucleoid) - max(nucleoid))
        nucleoid = [0] * 4
    return score


def construct_count(motifs):
    denominator =  0
    nucleoid = [0]*4
    #bana column length lazım o yüzden len(motifs[0]) alındı.
    count = [[0 for i in range(len(motifs[0]))] for j in range(4)]

    for i in range(0,len(motifs[0])):
        for j in range(0,len(motifs)):
            if (motifs[j][i] == 'a'):
                nucleoid[0] += 1
            elif (motifs[j][i] == 'c'):
                nucleoid[1] += 1
            elif (motifs[j][i] == 'g'):
                nucleoid[2] += 1
            elif (motifs[j][i] == 't'):
                nucleoid[3] += 1
        denominator = sum(nucleoid)

        for k in range(0,len(nucleoid)):
            count[k][i] = nucleoid[k]
        nucleoid = [0]*4

    #eğer count 2d arraying herhangi bir değer sıfırsa tüm değerlere 1 eklesin.
    if any(0 in sublist for sublist in count):
        for i in range(0,len(count)):
            count[i] = [x + 1 for x in count[i]]
        denominator = denominator + 4 #her değere 1 ekleyince payda da acgt boyutundan dolayı 4 artmış oluyor.
    return count, denominator

def profile(count, denominator):
    profile = [[0 for i in range(len(count[0]))] for j in range(4)]

    for i in range(0, len(count)):
        profile[i] = [x/denominator for x in count[i]]
    return profile

def probability_gibbs(motif, profile):
    probabilities = []
    init = 1.0

    for i in range(0, len(motif)):
        for j in range(0, len(motif[i])):
            if (motif[i][j] == 'a'):
                init *= profile[0][j]
            elif (motif[i][j] == 'c'):
                init *= profile[1][j]
            elif (motif[i][j] == 'g'):
                init *= profile[2][j]
            elif (motif[i][j] == 't'):
                init *= profile[3][j]
        probabilities.append(init)
        init = 1.0

    select = random.choices(motif, probabilities)[0]
    return select

def probability_randomized(dna, profile):
    probabilities = []
    init = 1.0

    for i in range(0, len(dna)):
        for j in range(0, len(dna[i])):
            if (dna[i][j] == 'a'):
                init *= profile[0][j]
            elif (dna[i][j] == 'c'):
                init *= profile[1][j]
            elif (dna[i][j] == 'g'):
                init *= profile[2][j]
            elif (dna[i][j] == 't'):
                init *= profile[3][j]
        probabilities.append(init)
        init = 1.0
    #maximum probability olanın indexini döndür. bana o kmerin valuesu lazım.
    index = probabilities.index(max(probabilities))
    return dna[index]


def findsubstring(string,size):
    substring = []

    for i in range(0, len(string)):
        pattern = string[i:i + size]
        if len(pattern) != size:
            break
        substring.append(pattern)

    return substring

def main():
    dna = []

    f = open("input.txt", "r")
    for line in f:
        dna.append(line.rstrip('\n'))

    print("Gibbs Algorithm results: ")
    gibbsampler(dna,10,10,1000)
    print("\n")
    print("Randomized Motif Search Algorithm  results: ")
    randomizedmotifsearch(dna,10,10)

if __name__ == "__main__":
    main()