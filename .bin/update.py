#!/usr/bin/python3

import json
import os
import sys
from collections import OrderedDict

def inject(dest, destkey, src, srckey, is_dialogue=False):
    if srckey in src:
        if is_dialogue:
            dest[destkey] = srckey + ': ' + src[srckey]
        else:
            dest[destkey] = src[srckey]

def main():
    with open('.bin/data.json', 'r') as f:
        data = json.load(f)

    changes = []
    for mermaid, season in data['mermaid'].items():
        when = OrderedDict({
            'Language': 'en',
            'Season': season,
        })

        changes.append(OrderedDict({
            'Action': 'Load',
            'Target': 'Characters/Mariner',
            'FromFile': f'assets/{mermaid}.png',
            'When': when,
        }))

        entries = OrderedDict()
        inject(entries, 'Beach_Mariner_Player_Male', data['noun']['male'], mermaid)
        inject(entries, 'Beach_Mariner_Player_Female', data['noun']['female'], mermaid)
        inject(entries, 'Beach_Mariner_PlayerMarried', data['override']['married'], mermaid, is_dialogue=True)
        inject(entries, 'Beach_Mariner_PlayerHasItem', data['override']['has_item'], mermaid, is_dialogue=True)
        inject(entries, 'Beach_Mariner_PlayerNotUpgradedHouse', data['override']['not_upgraded_house'], mermaid, is_dialogue=True)
        inject(entries, 'Beach_Mariner_PlayerBuyItem_Question', data['dialogue']['question'], mermaid, is_dialogue=True)
        inject(entries, 'Beach_Mariner_PlayerBuyItem_AnswerYes', data['dialogue']['answer_yes'], mermaid)
        inject(entries, 'Beach_Mariner_PlayerBuyItem_AnswerNo', data['dialogue']['answer_no'], mermaid)
        inject(entries, 'Beach_Mariner_PlayerNoRelationship', data['override']['no_relationship'], mermaid, is_dialogue=True)
        if entries:
            changes.append(OrderedDict({
                'Action': 'EditData',
                'Target': 'Strings/Locations',
                'Entries': entries,
                'When': when,
            }))

    content = OrderedDict({
        'Format': '1.19.0',
        'Changes': changes,
    })

    with open('content.json.new', 'w') as f:
        json.dump(content, f, indent=2)

    os.replace('content.json.new', 'content.json')

    return 0


if __name__ == '__main__':
    sys.exit(main())
