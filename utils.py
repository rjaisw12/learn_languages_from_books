import fitz  # PyMuPDF
import re
import random
import os
from google.cloud import translate_v2 as translate

#os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "service_account_file.json"

def translate_sentence(sentence):
    translate_client = translate.Client()
    result = translate_client.translate(sentence, source_language="zh-CN", target_language="fr")
    return result['translatedText']


def extract_text_from_pdf(pdf_path, start_page=0, end_page=None):
    doc = fitz.open(pdf_path)
    text = ""
    for page in range(start_page, end_page if end_page is not None else len(doc)):
        text += doc[page].get_text()
    return text

def split_text_into_sentences(text):
    sentences = re.split(r'[。！？\n \n]', text)  # Utilise '\n \n' comme séparateur
    sentences = [sentence.replace('\n', ' ') for sentence in sentences]  # Retire les sauts de ligne dans chaque phrase
    sentences = [sentence for sentence in sentences if len(sentence) > 5]  # Filtrer les phrases très courtes
    return sentences

def choose_random_sentence(sentences):
    return random.choice(sentences)

def remove_random_word_from_sentence(sentence):
    words = list(sentence)  # Divise la phrase en caractères
    if len(words) > 2:
        words_to_remove = random.sample(words, 2)  # Retirer 2 mots au hasard
        for word in words_to_remove:
            sentence = sentence.replace(word, "__", 1)
    return words_to_remove, sentence

def get_random_characters(sentences, num_chars):
    all_characters = [list(sentence) for sentence in sentences]
    all_characters = [char for sublist in all_characters for char in sublist]  # Flatten the list
    return random.sample(all_characters, num_chars)

def get_character_options(sentences, correct_characters, num_options=8):
    random_characters = get_random_characters(sentences, num_options - len(correct_characters))
    character_options = correct_characters + random_characters
    random.shuffle(character_options)  # Shuffle the options
    return character_options

pdf_path = 'hp_chinois.pdf'
start_page = 11
end_page = 12

text = extract_text_from_pdf(pdf_path, start_page, end_page)
sentences = split_text_into_sentences(text)
chosen_sentence = choose_random_sentence(sentences)
words_to_remove, sentence_with_missing_word = remove_random_word_from_sentence(chosen_sentence)
translated_sentence = translate_sentence(chosen_sentence)
character_options = get_character_options(sentences, words_to_remove)

print("Phrase avec des mots masqués : ", sentence_with_missing_word)
print("Traduction en français : ", translated_sentence)
print("Options de caractères : ", character_options)
