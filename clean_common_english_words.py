# make a code to read common_english_words.txt and remove duplicates and make all into lower case.


def clean_common_english_words():
    # Open the file for reading
    with open('common_english_words.txt', 'r') as file:
        # Read the words from the file and split them into a list
        words = file.read().split()

    # Convert all words to lowercase and remove duplicates
    unique_words = list(set(word.lower() for word in words))

    # Sort the unique words alphabetically (optional)
    unique_words.sort()

    # Create a new file to store the unique lowercase words
    with open('common_english_words.txt', 'w') as output_file:
        # Write the unique words to the new file
        for word in unique_words:
            output_file.write(word + '\n')

    print("cleaned common_english_words.txt")

if __name__ == '__main__':
    clean_common_english_words()