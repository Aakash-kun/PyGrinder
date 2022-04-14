from ..config import conf
from ..support_functions import sfd

async def match_emote(msg, bot):

    a = await sfd.get_interactions(msg, bot)
    mydict = {}
    for b in a:
        for c in b:
            mydict[c["label"]] = c['custom_id']
    answer = a[mydict[sfd.get_highest_preference(mydict.keys(), conf.search_locations)]]["custom_id"]

[
    [
        {
        'type': 2,
        'style': 2,
        'label': '🤗',
        'custom_id': '4d82f7c4-c120-4f3f-9f74-0093d9949a5d:🤗',
        'hash': '',
        'disabled': True
    }, {
        'type': 2,
        'style': 2,
        'label': '🤔',
        'custom_id': '4d82f7c4-c120-4f3f-9f74-0093d9949a5d:🤔',
        'hash': '',
        'disabled': True
    }, {
        'type': 2,
        'style': 2,
        'label': '😌',
        'custom_id': '4d82f7c4-c120-4f3f-9f74-0093d9949a5d:😌',
        'hash': '',
        'disabled': True
    }, {
        'type': 2,
        'style': 2,
        'label': '🙂',
        'custom_id': '4d82f7c4-c120-4f3f-9f74-0093d9949a5d:🙂',
        'hash': '',
        'disabled': True
    }, {
        'type': 2,
        'style': 2,
        'label': '😄',
        'custom_id': '4d82f7c4-c120-4f3f-9f74-0093d9949a5d:😄',
        'hash': '',
        'disabled': True
    }
    ],
    [
        {
        'type': 2,
        'style': 2,
        'label': '🙃',
        'custom_id': '4d82f7c4-c120-4f3f-9f74-0093d9949a5d:🙃',
        'hash': '',
        'disabled': True
    }, {
        'type': 2,
        'style': 2,
        'label': '😀',
        'custom_id': '4d82f7c4-c120-4f3f-9f74-0093d9949a5d:😀',
        'hash': '',
        'disabled': True
    }, {
        'type': 2,
        'style': 3,
        'label': '😁',
        'custom_id': '4d82f7c4-c120-4f3f-9f74-0093d9949a5d:😁',
        'hash': '',
        'disabled': True
    }, {
        'type': 2,
        'style': 2,
        'label': '😉',
        'custom_id': '4d82f7c4-c120-4f3f-9f74-0093d9949a5d:😉',
        'hash': '',
        'disabled': True
    }, {
        'type': 2,
        'style': 2,
        'label': '😆',
        'custom_id': '4d82f7c4-c120-4f3f-9f74-0093d9949a5d:😆',
        'hash': '',
        'disabled': True
    }
    ]
]