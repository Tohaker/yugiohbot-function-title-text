import json
import re

import nltk
import pandas as pd
import requests


def import_from_api():
    # Get the data for all cards from the API.
    response = requests.get('https://db.ygoprodeck.com/api/v5/cardinfo.php')

    # Create a new Dataframe and Array to store the card names in.
    output = pd.DataFrame(columns=['card', 'type', 'effect', 'flavour'])
    card_names = []
    card_types = []
    card_effect = []
    is_flavour = []

    if response.status_code == 200:
        j = json.loads(response.content.decode('utf-8'))

        # The way this API structures its data means we have access the 1st element which contains all the cards.
        for card in j:
            name = card['name']  # Get the name from each card. It is a 'dict' object.
            type = card['type']
            description = card['desc']

            if type == 'Normal Monster':
                is_flavour.append(True)
            else:
                is_flavour.append(False)

            card_names.append(name)
            card_types.append(type)
            card_effect.append(description)

        output['card'] = card_names
        output['type'] = card_types
        output['effect'] = card_effect
        output['flavour'] = is_flavour
        output.to_csv('cards_api.csv', index=False)  # Output to a CSV.
    else:
        return None


def label_effects():
    file = 'cards_api.csv'
    cards = pd.read_csv(file)['card'].dropna().values.tolist()
    effects = pd.read_csv(file)['effect'].dropna().values.tolist()
    is_flavour = pd.read_csv(file)['flavour'].dropna().values.tolist()

    sentence_start = []
    comma = []
    semicolon = []
    colon = []
    sentence_end = []

    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

    for card, effect in enumerate(effects):

        # We don't want to use flavour text in effects.
        if is_flavour[card]:
            continue

        new_effect = effect.replace('max. ', 'max ')
        sentences = tokenizer.tokenize(new_effect)

        for sentence in sentences:
            phrases = extract_phrases(sentence, cards[card])

            previous_phrase = ''

            for i, phrase in enumerate(phrases):
                # First we get the start of the sentence.
                # This forms a list of all the things we can start a sentence with.
                if i == 0:
                    sentence_start.append(phrase)
                    previous_phrase = phrase
                    continue

                if i == len(phrases) - 1:
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


def label_flavour_text():
    file = 'cards_api.csv'
    effects = pd.read_csv(file)['effect'].dropna().values.tolist()
    is_flavour = pd.read_csv(file)['flavour'].dropna().values.tolist()

    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    all_flavours = []

    for i, effect in enumerate(effects):
        if is_flavour[i]:
            sentences = tokenizer.tokenize(effect)
            all_flavours.extend(sentences)

    output = pd.DataFrame({'flavour text': all_flavours})
    output.to_csv('flavour_list.csv', index=False)


def extract_phrases(sentence, card):
    names = re.findall('"([^"]*)"', sentence)
    for name in names:
        if name == card:
            sentence = sentence.replace(name, '{}')

    new_sentence = sentence.replace(',', ',,').replace(';', ';;').replace(':', '::')
    phrases = re.split(', |; |: ', new_sentence)
    return phrases


if __name__ == '__main__':
    label_flavour_text()
