import json

from backends.file_backend import FileBackend
from filters.card_msg_filter import CardMessageFilter
from messages.base_message import BaseMessage


class CardMessage(BaseMessage):
    message_backend_class = FileBackend
    filter_classes = (CardMessageFilter,)

    def process_message(self, msg):
        card = json.loads(msg['card'])
        print('Description: {} | Link: {}'.format(
            card['description'].encode('utf8'), card['url'].encode('utf8')))