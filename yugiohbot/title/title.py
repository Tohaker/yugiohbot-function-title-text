import csv
import random
import logging

from textblob import TextBlob


def parse_existing_titles(file):
    existing_names = []
    nouns = []
    adjectives = []

    # Read in the card names from a CSV file to a list.
    try:
        with open(file, encoding="utf8") as csvfile:
            read_csv = csv.reader(csvfile)
            for row in read_csv:
                if read_csv.line_num != 1:
                    existing_names.append(row[1])
    except FileNotFoundError as fe:
        logging.debug('File: ' + file + ' could not be found.\n' + str(fe))
        return nouns, adjectives

    # Read each card name into a TextBlob and extract the noun into a list.
    for name in existing_names:
        blob = TextBlob(name)

        for word, pos in blob.tags:
            if pos == 'NNP':
                nouns.append(word)  # Only add words which are Proper Nouns to the list.
            elif pos == 'JJ':
                adjectives.append(word)  # Only add words which are Adjectives to the list.

    nouns = dedup(nouns)
    adjectives = dedup(adjectives)

    return nouns, adjectives


# Removes duplicates from a list while still preserving the order.
def dedup(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]


def create_new_title(nouns, adjectives):
    if len(nouns) == 0:
        return ""
    elif len(nouns) > 0 and len(adjectives) == 0:
        nouns_adjectives_dict = {'nouns': nouns}
    else:
        nouns_adjectives_dict = {'nouns': nouns, 'adjectives': adjectives}

    no_sections = random.randint(1, 2)  # Select how many sections the title will have. Min 1, Max 2.
    title_section = []
    title_section_pos = []

    for i in range(no_sections):
        no_components = random.randint(1, 2)  # Select how many components each section will have. Min 1, Max 2.
        component = []
        component_pos = []

        for j in range(no_components):
            if len(component) < 1:
                random_pos = random.choice(list(nouns_adjectives_dict.keys()))  # Choose either a noun or an adjective
                random_word = random.choice(nouns_adjectives_dict[random_pos])  # Select a random value from the POS

                component.append(random_word)
                component_pos.append(random_pos)

                if random_pos is 'adjectives' and no_components < 2:
                    no_components += 1  # An adjective can't be the only word, so we add an extra one if one is chosen.
            else:
                component.append(random.choice(nouns))  # Get a new random noun

        title_section.append(component)
        title_section_pos.append(component_pos)

    if len(title_section) > 1:
        second_section = title_section_pos[1]
        connecting_list = ['of', 'of the', 'the']

        if second_section[-1] == 'adjectives':
            # If the last word is an adjective, we use 'of'.
            connecting = 'of'
        else:
            # Otherwise just randomise between connecting phrases.
            connecting = random.choice(connecting_list)

        final_title = ""
        i = 0
        for section in title_section:
            if i > 0:
                final_title += connecting + ' '
            for word in section:
                final_title += word + ' '
            i += 1
    else:
        final_title = ""
        for word in title_section[0]:
            final_title += word + ' '

    return final_title
