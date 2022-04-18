# Summary

The programe of k-mer counting

## Algorithm Implemented

My algorithm is try to implement the BFCounter. 

1. First, I define a class about Bloomfilter. In this class, the hash function numbers and length of array are determined by the number items of input (k-mer) and false positive probability. I define the items number is 10e4 and probability is 0.001.

2. Second, I define a class about Kmer-processing. The k-mer will be processed into bit coding (in canonical form). Moreover, the encoding function is also define to encode.

3. In the programe, It will read in the sequence and splice into the k-mer, and then the k-mer will be coded. The boolm filter will check that whether the k-mer in the array. If the k-mer in boolm filter, The k-mer will be inserted to the hash table, otherwise, the k-mer will be added to bloom filter. After processing the whole k-mer, scaning the hash table for printing k-mer that is satisfactory.

## How to use it
On Linux or terminal, you just need to run it with three parameter: the path of your input fasta file, the length of k-mer, and the counts of all k-mers in the fasta file that occur at least q times.

`python kmer_count.py input.fa 20 40`

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
