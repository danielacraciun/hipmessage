from local_settings import token, room_name
from hipmessage import BaseFilter, HipMessage, FileBackend
import json


class PlainMessageFilter(BaseFilter):
    # Get all messages that are not card
    without_fields = ['card']


class CardMessageFilter(BaseFilter):
    # Get all messages that have a card
    mandatory_fields = ['card']

    def is_valid(self, message):
        # Get only those that represent a link
        # This needs to be fixed; cards come as string
        card = json.loads(message['card'])
        return card['style'] == 'link'


class CardMessage(HipMessage):
    message_backend_class = FileBackend
    filter_classes = (CardMessageFilter,)

    def process_message(self, msg):
        card = json.loads(msg['card'])
        print('Description: {} | Link: {}'.format(
            card['description'].encode('utf8'), card['url'].encode('utf8')))


class PlainMessage(HipMessage):
    message_backend_class = FileBackend
    filter_classes = (PlainMessageFilter,)

    def process_message(self, msg):
        msg = json.loads(msg['card'])
        print(msg)


instance = CardMessage(token, room_name)
instance.run()
