import pandas as pd


def sanitise_monster_effects(source, output):
    effects = pd.read_csv(source)['effect'].dropna().values.tolist()
    card_types = pd.read_csv(source)['type'].dropna().values.tolist()

    accept = ['Monster']
    ignore = ['Normal', 'Pendulum', 'Fusion']

    with open(output, 'w', encoding="utf-8") as f:
        for i, item in enumerate(effects):
            if is_correct_card(card_types[i], accept=accept, ignore=ignore):
                f.write("%s\n" % item.strip().replace('\n', ' ').replace('\r', ' '))


def sanitise_normal_monster_effects(source, output):
    effects = pd.read_csv(source)['effect'].dropna().values.tolist()
    card_types = pd.read_csv(source)['type'].dropna().values.tolist()

    accept = ['Normal Monster']
    ignore = ['Pendulum', 'Fusion']

    with open(output, 'w', encoding="utf-8") as f:
        for i, item in enumerate(effects):
            if is_correct_card(card_types[i], accept=accept, ignore=ignore):
                f.write("%s\n" % item.strip().replace('\n', ' ').replace('\r', ' '))


def sanitise_fusion_effects(source, output):
    effects = pd.read_csv(source)['effect'].dropna().values.tolist()
    card_types = pd.read_csv(source)['type'].dropna().values.tolist()

    accept = ['Fusion Monster']
    ignore = ['Normal', 'Pendulum']

    with open(output, 'w', encoding="utf-8") as f:
        for i, item in enumerate(effects):
            if is_correct_card(card_types[i], accept=accept, ignore=ignore):
                f.write("%s\n" % item.strip().replace('\n', ' ').replace('\r', ' '))


def sanitise_trap_effects(source, output):
    effects = pd.read_csv(source)['effect'].dropna().values.tolist()
    card_types = pd.read_csv(source)['type'].dropna().values.tolist()

    accept = ['Trap']
    ignore = []

    with open(output, 'w', encoding="utf-8") as f:
        for i, item in enumerate(effects):
            if is_correct_card(card_types[i], accept=accept, ignore=ignore):
                f.write("%s\n" % item.strip().replace('\n', ' ').replace('\r', ' '))


def sanitise_spell_effects(source, output):
    effects = pd.read_csv(source)['effect'].dropna().values.tolist()
    card_types = pd.read_csv(source)['type'].dropna().values.tolist()

    accept = ['Spell']
    ignore = []

    with open(output, 'w', encoding="utf-8") as f:
        for i, item in enumerate(effects):
            if is_correct_card(card_types[i], accept=accept, ignore=ignore):
                f.write("%s\n" % item.strip().replace('\n', ' ').replace('\r', ' '))


def is_correct_card(card_type, accept, ignore):
    b1 = any(t in card_type for t in accept)
    b2 = any(t not in card_type for t in ignore) if len(ignore) is not 0 else True
    return b1 and b2


if __name__ == '__main__':
    source = '../resources/cards_api.csv'
    sanitise_fusion_effects(source, '../resources/fusion.txt')
