import json
import re

import nltk
import pandas as pd
import requests


def import_from_api():
    # Get the data for all cards from the API.
    response = requests.get('https://db.ygoprodeck.com/api/v5/cardinfo.php')

    # Create a new Dataframe and Array to store the card names in.
    output = pd.DataFrame(columns=['card', 'effect'])
    card_names = []
    card_effect = []

    if response.status_code == 200:
        j = json.loads(response.content.decode('utf-8'))

        # The way this API structures its data means we have access the 1st element which contains all the cards.
        for card in j:
            name = card['name']  # Get the name from each card. It is a 'dict' object.
            description = card['desc']
            print(name)
            print(description)
            card_names.append(name)
            card_effect.append(description)

        output['card'] = card_names
        output['effect'] = card_effect
        output.to_csv('cards_api.csv', index=False)  # Output to a CSV.
    else:
        return None


def label_effects():
    effects = pd.read_csv('cards_api.csv')['effect'].dropna().values.tolist()
    columns = ['start', 'comma', 'semicolon', 'colon', 'hyphen', 'end']

    sentence_start = []
    comma = []
    semicolon = []
    colon = []
    sentence_end = []

    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

    for effect in effects:
        sentences = tokenizer.tokenize(effect)

        for sentence in sentences:
            new_sentence = sentence.replace(',', ',,').replace(';', ';;').replace(':', '::')

            if new_sentence.count('"') > 0:
                new_sentence = new_sentence

            phrases = re.split(', |; |: ', new_sentence)

            previous_phrase = ''

            for i, phrase in enumerate(phrases):
                # First we get the start of the sentence.
                # This forms a list of all the things we can start a sentence with.
                if i == 0:
                    sentence_start.append(phrase)
                    previous_phrase = phrase
                    continue

                if i == len(phrase):
                    sentence_end.append(phrase)
                    continue

                punctuation = previous_phrase[-1:]

                switcher = {
                    ',': comma,
                    ';': semicolon,
                    ':': colon,
                }

                comes_after = switcher.get(punctuation, sentence_start)  # Might have to change the default comes_after
                comes_after.append(phrase)  # Wording is confusing, but this means
                # "This phrase comes_after the punctuation of the previous phrase.
                previous_phrase = phrase

    st = pd.DataFrame({'start': sentence_start})
    cm = pd.DataFrame({'comma': comma})
    sc = pd.DataFrame({'semicolon': semicolon})
    cl = pd.DataFrame({'colon': colon})
    ed = pd.DataFrame({'end': sentence_end})

    output = pd.concat([st, cm, sc, cl, ed], axis=1)
    output.to_csv('effect_order.csv', index=False)


def find_proper_nouns(sentence):
    if sentence.count('"') == 0:
        return None

    nouns = []
    word = ''
    inside_noun = False

    for letter in sentence:
        if letter == '"':
            inside_noun = not inside_noun

        if inside_noun:
            word += letter
        else:
            if word:
                nouns.append(word)
