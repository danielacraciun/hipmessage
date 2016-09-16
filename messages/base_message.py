import datetime

from hypchat import HypChat


class BaseMessage(object):
    """
    Class that gets all messages from a given room, filters them through
    the classes from filter_classes and returns them when get_newest_messages
    is called.
    """

    # A class that has implemented two methods
    #   - set_last_message_id(self._room_name, )
    #   - get_last_message_id()
    message_backend_class = None

    # Iterable of filter classes.
    # All messages will be passed through the is_ok method of this
    # classes and will include them only if the return Value is True
    filter_classes = None

    def __init__(self, token, room_name, max_results=500):
        self._token = token
        self._room_name = room_name
        self._hipchat_client = HypChat(token)
        self._room = self._hipchat_client.get_room(self.get_room_id(room_name))
        self._message_backend = self.message_backend_class(self._room_name)
        self._max_results = max_results

    def get_room_id(self, room_name):
        rooms = self._hipchat_client.rooms()
        filtered_rooms = filter(
            lambda room: room['name'] == self._room_name, rooms['items'])
        if not filtered_rooms:
            raise ValueError('No room with name {}'.format(self._room_name))

        return list(filtered_rooms)[0]['id']

    def is_message_valid(self, message):
        if self.filter_classes:
            return all(
                map(lambda cls: cls().is_ok(message), self.filter_classes))
        return True

    def process_complete_history(self):
        date = datetime.datetime.utcnow()
        newest_id = None

        while True:
            messages_count = 0
            messages = self._room.history(
                maxResults=self._max_results, date=date)
            for message in messages['items']:
                messages_count += 1
                if self.is_message_valid(message) is False:
                    continue

                self.process_message(message)
                newest_id = newest_id or message['id']

            date = message['date']

            if messages_count < 1000:
                return newest_id

    def get_newest_messages(self):
        last_message_id = self._message_backend.get_last_message_id()

        params = {}
        if last_message_id is not None:
            params = {'not_before': last_message_id}
        else:
            newest_id = self.process_complete_history()
            self._message_backend.set_last_message_id(newest_id)
            return

        last_message = None
        # The messages come in the order oldest to newest
        for msg in self._room.latest(**params)['items']:
            if self.is_message_valid(msg):
                self.process_message(msg)
                last_message = msg

        if last_message is not None:
            self._message_backend.set_last_message_id(last_message['id'])

    def process_message(self, msg):
        """
        This is the method you override in your derived class.
        Method that takes as only argument a message and processes it.
        """

    def run(self):
        self.get_newest_messages()
