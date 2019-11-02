from text import *
from title import *


def function(event, context):
    source_file = 'resources/cards_api.csv'

    nouns, adjectives = title.parse_existing_titles(source_file)
    card_title = title.create_new_title(nouns, adjectives).strip()

    card_effect = text.generate_improved_effect_text('resources/effect_order.csv').format(
        card_title)  # Add the card title wherever there is a placeholder

    card_flavour = text.generate_flavour_text('resources/flavour_list.csv')

    result = {'title': card_title, 'effect': card_effect, 'flavour': card_flavour}
    print(result)

    return result


if __name__ == '__main__':
    print(function(None, None))
