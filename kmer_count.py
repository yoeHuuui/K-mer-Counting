import sys
import time
import math

class BloomFilter(object):
    def __init__(self, items_count, fp_prob):
        self.fp_prob = fp_prob
        self.size = self.get_size(items_count, fp_prob)
        self.hash_count = self.get_hash_count(self.size, items_count)
        self.bit_array = [0] * self.size
         
    @classmethod
    def get_size(self, n, p):
        m = -(n * math.log(p))/(math.log(2)**2)
        return int(m)
        
    @classmethod
    def get_hash_count(self, m, n):
        k = (m/n) * math.log(2)
        return int(k)

    @classmethod
    def hash_func(self, item, i):
        return (item ** (i+1)) % (10 ** 5)

    def add(self, item):
        for i in range(self.hash_count):
            digest = self.hash_func(item, i)
            self.bit_array[digest] += 1
 
    def check(self, item):
        digests = []
        for i in range(self.hash_count):
            digest = self.hash_func(item, i)
            digests.append(self.bit_array[digest])
        if min(digests) != 0:
            return True
        else:
            return False

class Kmer_processing(object):
    def __init__(self):
        #self.kmer = kmer
        self.trantab = str.maketrans('acgt', 'tgca')

    def canonical(self, kmer):
        kmer_re = kmer.translate(self.trantab)
        kmer_re = kmer_re[::-1]
        if kmer > kmer_re:
            return(kmer_re)
        else:
            return(kmer)
    
    def coding(self, kmer):
        result = 1
        for char in kmer:
            result = (result << 2) | ((ord(char) >> 1) & 3)
        return result
    
    def encoding(self, bits):
        result = ''
        enc = bits
        while enc > 1:
            byte = enc & 3
            if byte == 0:
                result += 'a'
            elif byte == 1:
                result += 'c'
            elif byte == 2:
                result += 't'
            elif byte == 3:
                result += 'g'
            enc = enc >> 2
        return result[::-1]

start = time.time()
file = sys.argv[1]
kmer_len = int(sys.argv[2])
q = int(sys.argv[3])

bloomf = BloomFilter(10 ** 4, 0.001)
kmer_p = Kmer_processing()
kmer_count = dict()

file_object = open(file, 'r')
for line in file_object:
    if not line.startswith(">"):
        line = line.rstrip("\n")
        if kmer_len > len(line):
            print("ERROR!")
        else:
            line = line.lower()
            for i in range(0, (len(line)-kmer_len+1)):
                seq = kmer_p.canonical(line[i:i+kmer_len])
                if 'n' not in seq:
                    index_num = kmer_p.coding(seq)
                    if bloomf.check(index_num) == True:
                        if index_num not in kmer_count:
                            kmer_count[index_num] = 1
                    else:
                        bloomf.add(index_num)
                    if index_num in kmer_count:
                        kmer_count[index_num] += 1
file_object.close()

for k,v in kmer_count.items():
    if v >= q:
        print(v, kmer_p.encoding(k))
end = time.time()
print("Runing Time:{}s".format(end-start))