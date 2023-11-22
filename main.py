from clean_common_english_words import *
from keyword_extraction_code import *
from togpt import *

file_path = '생화학안지인.txt'

# common_english_words.txt를 정리
clean_common_english_words()

# 1,2,3-gram 생성
# extract_keywords_from_book(file_path)
# 하나의 csv로 합침
# convert_to_csv(os.path.splitext(os.path.basename(file_path))[0])

# gpt와 reference를 이용하여 description을 추가
update_with_gpt_descriptions(f'{os.path.splitext(os.path.basename(file_path))[0]}_ngrams.csv',
                             model="gpt-3.5-turbo")  # gpt-3.5-turbo-1106

# 생성된 새로운 csv의 내용을 reference에 추가. not medical term들도 referenece에 추가해야함.
append_to_reference(f'{os.path.splitext(os.path.basename(file_path))[0]}_ngrams.csv', 'REFERENCE.csv')

# not medical term들을 제거
remove_non_medical_terms(f'{os.path.splitext(os.path.basename(file_path))[0]}_ngrams.csv')
