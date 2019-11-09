import random

import requests

from text import *
from title import *


def function(event, context):
    source_file = 'resources/cards_api.csv'

    nouns, adjectives = title.parse_existing_titles(source_file)
    card_title = title.create_new_title(nouns, adjectives).strip()

    template = ['Normal', 'Effect', 'Ritual', 'Synchro', 'DarkSynchro', 'Xyz', 'Spell', 'Trap', 'Fusion']
    card_template = random.choice(template)

    ml_selector = {
        'Normal': 'flavour',
        'Effect': 'monster',
        'Ritual': 'monster',
        'Synchro': 'monster',
        'DarkSynchro': 'monster',
        'Xyz': 'monster',
        'Spell': 'spell',
        'Trap': 'trap',
        'Fusion': 'fusion'
    }

    if ml_selector.get(card_template) == 'flavour':
        card_effect = text.generate_flavour_text('resources/flavour_list.csv')
    else:
        card_effect = ml_text.generate_card_description(ml_selector.get(card_template))

    result = {'title': card_title, 'effect': card_effect, 'template': card_template}
    print(result)

    receiving_service_url = "https://yugiohbot-card-generator-t4loex5l4q-ue.a.run.app"

    # Set up metadata server request
    # See https://cloud.google.com/compute/docs/instances/verifying-instance-identity#request_signature
    metadata_server_token_url = 'http://metadata/computeMetadata/v1/instance/service-accounts/default/identity?audience='

    token_request_url = metadata_server_token_url + receiving_service_url
    token_request_headers = {'Metadata-Flavor': 'Google'}

    # Fetch the token
    token_response = requests.get(token_request_url, headers=token_request_headers)
    jwt = token_response.content.decode("utf-8")

    # Provide the token in the request to the receiving service
    receiving_service_headers = {'Authorization': 'bearer {}'.format(jwt)}
    service_response = requests.get(receiving_service_url, headers=receiving_service_headers, params=result)

    print(service_response.content)
    return service_response.content


if __name__ == '__main__':
    print(function(None, None))
