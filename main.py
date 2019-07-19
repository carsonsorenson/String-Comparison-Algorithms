import random
import time

# generate a binary string size 10000000 based off of a probability
def random_binary_string(p):
    size_of_string = 10000000
    s = ''
    state = '0'
    for i in range(size_of_string):
        if random.uniform(0, 1) > p:
            if state == '0':
                state = '1'
            else:
                state = '0'
        s += state
    return s


# naive algorithm
def naive_algorithm(text, pattern):
    first_index_match = []
    m = len(pattern)
    n = len(text)
    for i in range(0, n - m + 1):
        status = 1
        for j in range(m):
            if text[i + j] != pattern[j]:
                status = 0
                break
        if j == m - 1 and status != 0:
            first_index_match.append(i)
    return first_index_match


# KMP algorithm with computing the longest prefix
def kmp_algorithm(text, pattern):
    first_index_match = []
    m = len(pattern)
    n = len(text)
    longest_prefix = [0] * m
    compute_longest_prefix(pattern, m, longest_prefix)
    j = 0
    i = 0
    while i < n:
        if pattern[j] == text[i]:
            j += 1
            i += 1
        if j == m:
            first_index_match.append(i-j)
            j = longest_prefix[j-1]
        elif i < n and pattern[j] != text[i]:
            if j != 0:
                j = longest_prefix[j-1]
            else:
                i += 1
    return first_index_match


def compute_longest_prefix(pattern, m, longest_prefix):
    l = 0
    i = 1
    while i < m:
        if pattern[i] == pattern[l]:
            l += 1
            longest_prefix[i] = l
            i += 1
        else:
            if l != 0:
                l = longest_prefix[l-1]
            else:
                longest_prefix[i] = 0
                i += 1


# BM Algorithm using the bad character heuristic
NUMBER_OF_CHARS = 2**16


def bad_character_heuristic(string, size):
    bad_char = [-1]*NUMBER_OF_CHARS
    for i in range(size):
        bad_char[ord(string[i])] = i
    return bad_char


def boyer_moore_algorithm(text, pattern):
    first_index_match = []
    m = len(pattern)
    n = len(text)
    bad_char = bad_character_heuristic(pattern, m)
    s = 0
    while s <= (n-m):
        j = m - 1
        while j >= 0 and pattern[j] == text[s+j]:
            j -= 1
        if j < 0:
            first_index_match.append(s)
            s += (m - bad_char[ord(text[s+m])] if s + m < n else 1)
        else:
            s += max(1, j - bad_char[ord(text[s+j])])
    return first_index_match


def empirical_studies():
    '''
    All of the raw data can be found in the './data' folder in .csv files.
    comment out the line that keeps track of the matches to run the empirical studies.
    '''

    # dna empirical study
    text = ''
    with open('input/dna.txt', 'r') as i:
        for line in i:
            text += line.strip('\n')
    run_empirical_study('data/dna.csv', text)

    # Shakespeare's work
    text = ''
    with open('input/Shakespeare.txt', 'r') as i:
        for line in i:
            text += line.replace('\n', ' ')
    run_empirical_study('data/Shakespeare.csv', text)

    # binary string 0.5 probability empirical study
    text = random_binary_string(0.5)
    run_empirical_study('data/0.5_binary.csv', text)

    # binary string 0.999 probability empirical study
    text = random_binary_string(0.999)
    run_empirical_study('data/0.999_binary.csv', text)

def run_empirical_study(output_file, text):
    with open(output_file, 'w') as o:
        o.write('n,Naive Algorithm,Kmp Algorithm,Boyer Moore Algorithm\n')
        n = 2
        while n < len(text):
            if n > 2 ** 16:
                break
            o.write(str(n) + ',')

            pattern = text[len(text) - n: len(text)]
            start = time.time()
            naive_algorithm(text, pattern)
            end = time.time()
            o.write(str(end - start) + ',')

            start = time.time()
            kmp_algorithm(text, pattern)
            end = time.time()
            o.write(str(end - start) + ',')

            start = time.time()
            boyer_moore_algorithm(text, pattern)
            end = time.time()
            o.write(str(end - start) + '\n')
            print(n)
            n *= 2
    print('Done with', output_file)


# This sets up the string and substring and then calls trace() which prints out the results of the 3 algorithms
def test_cases():
    o = open('trace.txt', 'w')

    # Test Case #0
    text = "TEST TEST TST TESTT TESSST TTEST KSDJFKLSJTESTKSJFKS TEST"
    pattern= "TEST"
    trace(text, pattern, o)

    # Test Case #1
    text = "AABAACAADAABAABABBBBAAABAABABAAAABAABBABABBBABBA"
    pattern = "AABA"
    trace(text, pattern, o)

    # Test Case #2
    text = '1000111011000110001000111000110110110100001001000011101011111010111100101110110101010100111000011001'
    pattern = '0001'
    trace(text, pattern, o)


def trace(text, pattern, o):
    o.write('The first indices where the substring \"' + pattern + '\" was found in the string \"' + text + '\"\n\n')

    o.write('Naive Algorithm:')
    first_positions = naive_algorithm(text, pattern)
    for i in first_positions:
        o.write(' ' + str(i))

    o.write('\nKMP Algorithm:  ')
    first_positions = kmp_algorithm(text, pattern)
    for i in first_positions:
        o.write(' ' + str(i))

    o.write('\nBM Algorithm:   ')
    first_positions = kmp_algorithm(text, pattern)
    for i in first_positions:
        o.write(' ' + str(i))
    o.write('\n\n')

def main():
    test_cases()
    #empirical_studies()


if __name__ == '__main__':
    main()
