import os

from backends.base_backend import BaseBackend


class FileBackend(BaseBackend):
    _FILE_PATH = 'last_message_db.info'
    DATE_SAVE_PATTERN = '%Y %m %d %H:%M:%S.%f'

    def __init__(self, room_name=None):
        self._room_name = room_name

    def _get_db_file(self):
        if os.path.isfile(self._FILE_PATH):
            return open(self._FILE_PATH, 'r')

        return None

    def get_last_message_id(self):
        file_h = self._get_db_file()
        if file_h is None:
            return None

        last_id = file_h.readline()
        last_id = last_id.strip('\n')
        file_h.close()

        return last_id or None

    def set_last_message_id(self, id_):
        if self._room_name is not None:
            file_name = '{}_{}'.format(self._room_name, self._FILE_PATH)
        else:
            file_name = self._FILE_PATH

        with open(file_name, 'w') as file_h:
            file_h.write('{}\n'.format(id_))