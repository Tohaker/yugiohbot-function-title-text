from text import *
from title import *


def function(event, context):
    source_file = 'resources/cards_api.csv'

    nouns, adjectives = title.parse_existing_titles(source_file)
    card_title = title.create_new_title(nouns, adjectives)

    card_text = text.generate_improved_effect_text('resources/effect_order.csv')

    result = {'title': card_title, 'text': card_text}
    print(result)

    return result


if __name__ == '__main__':
    print(function(None, None))
