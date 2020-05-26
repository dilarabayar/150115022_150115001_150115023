#Dilara Bayar 150115022 Sahra Bekli 150115023 İncilay Dikbıyık 150115001
import random
from random import choice

def randomizedmotifsearch(dna,motifsize,motiflength):
    counter = 0  #Hangi iterasyonda motifi bulduğunu göstermek için
    motifs = [None] * motifsize
    best_motifs = [None] * motifsize
    allsubstrings = [None] * motifsize #tüm kmerleri tutmak için
    best_score = 0
    denominator = 0 #paydayı tutmak için
    count = 0 #count arrayi

    #her sıradan random 10mer seçiyor. motife atıyor.
    for i in range(0, len(dna)):
        rndkmer = random.choice(findsubstring(dna[i], motiflength))
        motifs[i] = rndkmer

    #ilk olarak best motif random çıkan motife eşitlenir.
    best_motifs = motifs.copy()

    while True:
        count, denominator = construct_count(motifs) #count oluştur, paydayı bul
        profile_array = profile(count, denominator) #profile oluştur
        #dnada dizin dizin en iyi sonucu veren kmer bulunuyor. motif bu kmer ile değiştiriliyor.
        for i in range(0, len(dna)): #row boyunca ilerler.
            substring = findsubstring(dna[i], motifsize).copy() #dna rowundaki tüm kmerlerin probilitisi hesaplanır.
            element = probability_randomized(substring, profile_array) #
            del motifs[i]  #o sıradaki motif silinir, ve yeni en iyi motif konur.
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

    # ilk olarak best motif random çıkan motife eşitlenir.
    best_motifs = motifs.copy()

    for i in range(0, iteration): #verilen iterasyon sayısı kadar ilerleyecek.
        row = random.randint(0, motifsize-1)  # random bir motif seçilmesi belirleniyor.
        del motifs[row]   #seçilen rowu siliyorum.
        count, denominator = construct_count(motifs) #count array ve payda hesaplanır.
        profile_array = profile(count, denominator) #profil oluşturulur.
        selected_motif = probability_gibbs(findsubstring(dna[row],motiflength), profile_array) #yeni motif seçilir.
        motifs.insert(row, selected_motif) #yeni motif motifs arrayine eklenir.
        if (score(motifs) < score(best_motifs)): #eğer yeni score eskisinden daha düşükse en iyi scoreu değiştir.
            best_motifs = motifs.copy()

    print("Motifs that has best score is: ", score(best_motifs))
    for i in range(0, len(best_motifs[0])):
        print(best_motifs[i])

def score(motifs):
    score = 0
    nucleoid = [0] * 4

    for i in range(0,len(motifs[0])): #column boyunca ilerler.
        for j in range(0,len(motifs)): #row boyunca ilerler.
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
        nucleoid = [0] * 4 #bir sonraki columna geçerken nucleoid araryi resetlenir.
    return score


def construct_count(motifs):
    denominator =  0
    nucleoid = [0]*4
    #bana column length lazım o yüzden len(motifs[0]) alındı.
    count = [[0 for i in range(len(motifs[0]))] for j in range(4)]

    for i in range(0,len(motifs[0])): #column boyunca ilerler.
        for j in range(0,len(motifs)): #row boyunca ilerler.
            if (motifs[j][i] == 'a'):
                nucleoid[0] += 1
            elif (motifs[j][i] == 'c'):
                nucleoid[1] += 1
            elif (motifs[j][i] == 'g'):
                nucleoid[2] += 1
            elif (motifs[j][i] == 't'):
                nucleoid[3] += 1
        denominator = sum(nucleoid) #tüm column toplanarak payda hesaplanır.

        for k in range(0,len(nucleoid)): #counta bulunan sayıyı a-c-g-t sırasıyla ekle
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

    for i in range(0, len(count)): #tüm arrayi paydaya böl.
        profile[i] = [x/denominator for x in count[i]]
    return profile

def probability_gibbs(motif, profile):
    #tüm motiflerin üzerinden tek tek char by char ilerliyor.
    probabilities = []
    init = 1.0

    for i in range(0, len(motif)): #row boyunca ilerler.
        for j in range(0, len(motif[i])): #column boyunca ilerler.
            if (motif[i][j] == 'a'):
                init *= profile[0][j]
            elif (motif[i][j] == 'c'):
                init *= profile[1][j]
            elif (motif[i][j] == 'g'):
                init *= profile[2][j]
            elif (motif[i][j] == 't'):
                init *= profile[3][j]
        probabilities.append(init) #ilgili motifin probilitysi arraye eklenir.
        init = 1.0 #initial değer resetlenir.

    #her motifin seçilme olasılığı farklı ve eğer eşit çıkan olursa ilkini alıyor.
    select = random.choices(motif, probabilities)[0]
    return select

def probability_randomized(dna, profile):
    #tüm dnaki kmerlerin probabilitysi hesaplanacak.
    probabilities = []
    init = 1.0

    for i in range(0, len(dna)): #row boyunca ilerler.
        for j in range(0, len(dna[i])): #column boyunca ilerler.
            if (dna[i][j] == 'a'):
                init *= profile[0][j]
            elif (dna[i][j] == 'c'):
                init *= profile[1][j]
            elif (dna[i][j] == 'g'):
                init *= profile[2][j]
            elif (dna[i][j] == 't'):
                init *= profile[3][j]
        probabilities.append(init)  #ilgili motifin probilitysi arraye eklenir.
        init = 1.0 #initial değer resetlenir.

    #maximum probability olanın indexini döndür. bana o kmerin valuesu lazım.
    index = probabilities.index(max(probabilities))
    #dnada o kmerin kendisi geri döndürülür.
    return dna[index]


def findsubstring(string,size):
    substring = []

    #gönderilen stringdeki size boyutundaki tüm substringler bulunur.
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