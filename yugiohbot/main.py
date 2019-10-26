from text import *
from title import *
import google.auth
from google.auth.transport.requests import AuthorizedSession


def function(event, context):
    source_file = 'resources/cards_api.csv'

    nouns, adjectives = title.parse_existing_titles(source_file)
    card_title = title.create_new_title(nouns, adjectives)

    phrases = text.split_descriptions(source_file)
    card_text = text.generate_card_text(phrases)

    result = {'title': card_title, 'text': card_text}
    print(result)

    credentials, project = google.auth.default()
    authed_session = AuthorizedSession(credentials)

    response = authed_session.get("https://yugiohbot-card-generator-t4loex5l4q-ue.a.run.app", params=result)

    return response


if __name__ == '__main__':
    print(function(None, None))
