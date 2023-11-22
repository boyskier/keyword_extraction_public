import os.path
import re
import nltk
from collections import Counter
from nltk.corpus import stopwords, words, names
from nltk.stem import PorterStemmer
stemmer = PorterStemmer()

# Download necessary NLTK data
nltk.download('words')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
nltk.download('names')

male_names = names.words('male.txt')
female_names = names.words('female.txt')

english_words = set(words.words())


# print('polyurea' in english_words)
def generate_ngrams(words_list, n):
    return [' '.join(words_list[num:num + n]) for num in range(len(words_list) - n + 1)]


# Function to validate n-grams
def valid_ngram(ngram, stopwords_set, english_words_set, min_english_words=2):
    words = ngram.split()
    # Conditions for validation
    if any(word in stopwords_set for word in words): return False
    if len(words) != len(set(words)): return False
    if all(len(word) <= 3 for word in words): return False
    if sum(word in english_words_set for word in words) < min_english_words: return False
    return True


# Function to process and filter n-grams
def process_ngrams(words, n, stopwords_set, english_words_set, min_english_words):
    ngrams = generate_ngrams(words, n)
    return [ngram for ngram in ngrams if valid_ngram(ngram, stopwords_set, english_words_set, min_english_words)]


# Function to write frequencies to file
def write_frequencies_to_file(counter, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        for item, count in sorted(counter.items(), key=lambda x: x[1], reverse=True):
            if count >= 2:
                f.write(f"{item}, {count}\n")
            if item =="polyurea":
                print("polyurea found")
                print(count)


def extract_keywords_from_book(input_file_path, output_file_path=None):
    common_english_words = set(stopwords.words('english'))

    for name in male_names + female_names:
        common_english_words.add(name.lower())

    # Read additional common words
    with open('common_english_words.txt', 'r', encoding='utf-8') as file:
        common_english_words.update(file.read().splitlines())

    common_words_stems = set()
    for word in common_english_words:
        stemmed_word = stemmer.stem(word)
        common_words_stems.add(stemmed_word)


    # Read file content
    with open(input_file_path, 'r', encoding='utf-8') as file:
        original_content = file.read()

    words = re.findall(r'\b[a-zA-Z]+\b', original_content.lower())
    filtered_words = [
        word for word in words
        if word not in common_english_words and stemmer.stem(word) not in common_words_stems
    ]
    base_name = os.path.splitext(os.path.basename(input_file_path))[0]

    # Apply n-gram processing
    for n in range(1, 4):  # For 1-gram, 2-gram, and 3-gram
        if n == 1:
            min_english_words = 0
        elif n == 2:
            min_english_words = 1
        else:
            min_english_words = 2

        # min_english_words = 1 if n < 3 else 2  # 1 for bi-grams, 2 for tri-grams
        ngrams = process_ngrams(filtered_words, n, common_english_words, english_words, min_english_words)

        counter = Counter(ngrams)
        unique_ngrams = {ngram for ngram, count in counter.items() if count > 1}

        write_frequencies_to_file(counter, f'{base_name}_{n}_grams.txt')
        print(f'{n}-grams done')
        print(f'unique {n}-grams found: {len(unique_ngrams)}')
        print(f'file saved as {base_name}_{n}_grams.txt')
        print('-----------------------------------')
