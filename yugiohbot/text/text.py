import random

import nltk.data
import pandas as pd

from data import fusion


def generate_card_text(phrases):
    if len(phrases) == 0:
        return ""

    sample_range = 5 if len(phrases) >= 5 else len(phrases)
    rand = random.sample(range(len(phrases)), random.randint(1, sample_range))
    text = []
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    prohibited = [',', ':', ';', '-']

    for selection in rand:
        p = phrases[selection]
        r = random.randint(0, len(p) - 1)

        sel = p[r]
        text.append(sel)  # Get a random phrase from the random text selection

    lastchar = text[-1][-1:]
    if lastchar in prohibited:
        lastletter = lastchar
        new_selection = ''

        while lastletter in prohibited:
            selection = phrases[random.randint(0, len(phrases))]
            new_r = random.randint(0, len(selection) - 1)
            new_selection = selection[new_r]
            lastletter = new_selection[-1:]  # Here we make sure the final phrase ends with a period

        text.append(new_selection)

    seperator = ' '
    result = seperator.join(text)
    sentences = tokenizer.tokenize(result)
    sentences = [sent.capitalize() for sent in sentences]  # Capitalize each sentence.
    result = seperator.join(sentences)

    return result


def generate_improved_effect_text(file):
    start = pd.read_csv(file)['start'].dropna().values.tolist()
    comma = pd.read_csv(file)['comma'].dropna().values.tolist()
    semicolon = pd.read_csv(file)['semicolon'].dropna().values.tolist()
    colon = pd.read_csv(file)['colon'].dropna().values.tolist()
    end = pd.read_csv(file)['end'].dropna().values.tolist()

    switcher = {
        ',': comma,
        ';': semicolon,
        ':': colon
    }

    no_sentences = random.randint(1, 3)  # 3 sentences maximum
    sentences = []
    separator = ' '

    for s in range(no_sentences):
        phrases = [random.choice(start)]
        sentence_length = random.randint(1, 5)  # 1 minimum. We always have a start. 1 indicates only an end.
        progress = 1

        punctuation = phrases[0][-1:]  # Get the last character from the starting phrase.
        while punctuation != '.' and sentence_length > 1 and progress < sentence_length - 1:
            comes_from = switcher.get(punctuation)
            phrases.append(random.choice(comes_from))
            punctuation = phrases[-1][-1:]
            progress += 1  # Show our progress through the sentence.

        phrases.append(random.choice(end))
        result = separator.join(phrases)

        sentences.append(result)

    effect = separator.join(sentences)
    return effect


def generate_flavour_text(file):
    flavour = pd.read_csv(file)['flavour text'].dropna().values.tolist()

    separator = ' '
    sentences = []
    no_sentences = random.randint(1, 3)  # 3 sentences maximum

    for s in range(no_sentences):
        sentences.append(random.choice(flavour))

    return separator.join(sentences)


def generate_fusion_text(file):
    fc, ft, s = fusion.list_cards_and_summons(file)
    all_fusions = [*fc, *ft]

    no_fusions = random.randint(1, 3)

    has_summon = random.random() < 0.5
    has_level = random.random() < 0.5
    or_higher = random.random() < 0.5

    fusion_list = []
    for i in range(no_fusions):
        f = random.choice(all_fusions)
        prefix = ''
        if f in ft:
            prefix = str(random.randint(1, 7))
            if has_level:
                prefix += ' Level ' + str(random.randint(1, 5))
                if or_higher:
                    prefix += ' or higher'

        fusion_list.append(prefix + ' ' + f.strip())

    fusion_text = ' + '.join(fusion_list)
    if has_summon:
        fusion_text += random.choice(s)

    return fusion_text


if __name__ == '__main__':
    print(generate_fusion_text('../resources/cards_api.csv'))
