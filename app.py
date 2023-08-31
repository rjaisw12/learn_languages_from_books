import os
from utils import (
    extract_text_from_pdf,
    split_text_into_sentences,
    choose_random_sentence,
    remove_random_word_from_sentence,
    translate_sentence,
    get_character_options,
)
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)

ALLOWED_ORIGINS = ["https://www.raphaeljaiswal.com", "http://localhost:3000"]


CORS(app, origins=ALLOWED_ORIGINS)


@app.route("/get-chinese-quiz", methods=["GET"])
def get_chinese_quiz():
    pdf_path = "hp_chinois.pdf"
    start_page = 11
    end_page = 12

    text = extract_text_from_pdf(pdf_path, start_page, end_page)
    sentences = split_text_into_sentences(text)
    chosen_sentence = choose_random_sentence(sentences)
    words_to_remove, sentence_with_missing_word = remove_random_word_from_sentence(
        chosen_sentence
    )
    translated_sentence = translate_sentence(chosen_sentence)
    character_options = get_character_options(sentences, words_to_remove)

    response = {
        "sentenceWithMissingWord": sentence_with_missing_word,
        "translatedSentence": translated_sentence,
        "characterOptions": character_options,
        "words_to_guess": words_to_remove,
    }

    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True)
