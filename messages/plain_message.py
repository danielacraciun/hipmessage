from backends.file_backend import FileBackend
from filters.plain_msg_filter import PlainMessageFilter
from messages.base_message import BaseMessage


class PlainMessage(BaseMessage):
    message_backend_class = FileBackend
    filter_classes = (PlainMessageFilter,)

    def process_message(self, msg):
        print(msg['from']['name'])
