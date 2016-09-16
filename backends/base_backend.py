class BaseBackend(object):
    """
    Class that exposes two methods, get_last_message_id and
    set_last_message_id.self._room_name,  This ID is used to get the latest messages
    from a room, without getting the ones that were already processed
    """

    def get_last_message_id(self):
        """
        This returns the id of the last message that was saved or None
        if no message was saved so far
        """
        raise NotImplementedError(
            "You need to implement this in your derived class")

    def set_last_message_id(self, message_id):
        """
        Saves the id of the las message that was saved
        """
        raise NotImplementedError(
            "You need to implement this in your derived class")
