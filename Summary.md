# Summary

The programe of k-mer counting

## Algorithm Implemented

My algorithm is try to implement the BFCounter. 

1. First, I define a class about Bloomfilter. In this class, the hash function numbers and length of array are determined by the number items of input (k-mer) and false positive probability. I define the items number is 10e4 and probability is 0.001.

2. Second, I define a class about Kmer-processing. The k-mer will be processed into bit coding (in canonical form). Moreover, the encoding function is also define to encode.

3. In the programe, It will read in the sequence and splice into the k-mer, and then the k-mer will be coded. The boolm filter will check that whether the k-mer in the array. If the k-mer in boolm filter, The k-mer will be inserted to the hash table, otherwise, the k-mer will be added to bloom filter. After processing the whole k-mer, scaning the hash table for printing k-mer that is satisfactory.

## Analysis the complexity

### Time complexity

> In there, the time is deterimed by the number of k-mers. So the complexity is __O(n)__, where n is the numer of k-mers.

### Space complexity

> In there, the space is deterimed by the hash table. The space is lineal with the key of hash table. So the complexity is __O(n)__.

### Reflection

1. __I try to build up the bitarray, but I failed to do it. So, the memory is very cost. The array items in my programe is byte, not bit!__

2. __The boolm filter just a filtered function. I had design the counting function, but the result is not right. If the counting function can implemente, the space complexity will decrese more.__

3. Many websides gave me a lot help
   
>  <https://github.com/SUqianwei/k-mer-count-kit/blob/master/improved1.py>
> 
>  <https://github.com/deprekate/2bitSeq/blob/main/seq2bit.py>
> 
>  <https://blog.csdn.net/lhh08hasee/article/details/80032193>
> 
>  <https://www.geeksforgeeks.org/counting-bloom-filters-introduction-and-implementation/>
> 
>  <https://bmcbioinformatics.biomedcentral.com/articles/10.1186/1471-2105-12-333>

### Code

```
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

```