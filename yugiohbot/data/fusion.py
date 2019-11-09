import re

import nltk
import pandas as pd


def list_cards_and_summons(file):
    types = pd.read_csv(file)['type'].dropna().values.tolist()
    effects = pd.read_csv(file)['effect'].dropna().values.tolist()

    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

    fusion_cards = []
    fusion_types = []
    summon_desc = []

    for i, effect in enumerate(effects):
        if 'Fusion' not in types[i] or 'Pendulum' in types[i]:  # We don't want anything Pendulum (yet) or Non-Fusion.
            continue

        sentences = tokenizer.tokenize(effect)
        fusion_info = re.split('\n', sentences[0])  # The first sentence contains the Fusion specific information.

        cards = re.findall('"([^"]*)"', fusion_info[0])

        pos = nltk.pos_tag(fusion_info[0].split())
        temp_type = []
        found_type = False

        for word, tag in pos:
            if word.isdigit():
                found_type = True
                continue

            # Add to the list whenever a monster has been completed.
            if found_type and (('NN' not in tag and 'JJ' not in tag) or ('monster' in word.lower())):
                found_type = False
                if temp_type:
                    fusion_types.append(' '.join(temp_type))
                    temp_type.clear()

            if found_type and 'level' not in word.lower():
                temp_type.append(word)

        fusion_cards.extend(cards)

        if len(fusion_info) > 1 and 'summon' in fusion_info[1]:
            summon_desc.append(fusion_info[1])

    fusion_types = list(dict.fromkeys(fusion_types))
    fusion_cards = list(dict.fromkeys(fusion_cards))
    summon_desc = list(dict.fromkeys(summon_desc))
    return fusion_cards, fusion_types, summon_desc


if __name__ == '__main__':
    fc, ft, s = list_cards_and_summons('../resources/cards_api.csv')
    print(ft)
