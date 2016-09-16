import json

from filters.base_filter import BaseFilter


class CardMessageFilter(BaseFilter):
    # Get all messages that have a card
    mandatory_fields = ['card']

    def is_valid(self, message):
        # Get only those that represent a link
        # This needs to be fixed; cards come as string
        card = json.loads(message['card'])
        return card['style'] == 'link'
