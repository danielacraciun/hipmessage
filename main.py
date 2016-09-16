from local_settings import token, room_name
from messages.plain_message import PlainMessage

instance = PlainMessage(token, room_name)
instance.run()
