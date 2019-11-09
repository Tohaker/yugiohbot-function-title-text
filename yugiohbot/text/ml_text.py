import re

import nltk

from data import model


def generate_card_description(type):
    accepted = ['fusion', 'monster', 'spell', 'trap']

    if any(t in type for t in accepted):
        desc = model.generate_single(type, 0.5)
        formatted = desc[0]

        formatted = re.sub(r"([\"'])(?:(?=(\\?))\2.)*?\1", remove_whitespace, formatted)
        tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
        sentences = [sent.capitalize() for sent in tokenizer.tokenize(formatted)]
        formatted = ' '.join(sentences)
        return formatted

    else:
        print('No ML model for type {}.'.format(type))
        return None


def remove_whitespace(matchobj):
    return matchobj.group(0).replace('\" ', '\"').replace(' \"', '\"')


if __name__ == '__main__':
    generate_card_description('fusion')
