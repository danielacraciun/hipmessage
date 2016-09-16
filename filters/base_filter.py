class BaseFilter(object):
    # For a list of fields, check out
    # https://www.hipchat.com/docs/apiv2/method/view_room_history
    mandatory_fields = None
    without_fields = None

    def is_valid(self, message):
        """
        This is the method the method that you should override.
        Returns whether or not the given message passes a certain
        set of conditions
        """
        return True

    def is_ok(self, message):
        """
        This method returns whether or not the message passed this filter
        """
        return (
            self.has_mandatory_fields(message) and
            self.is_without_fields(message) and
            self.is_valid(message)
        )

    def has_mandatory_fields(self, msg):
        if self.mandatory_fields is None:
            return True

        keys = []
        self._get_dict_keys(msg, keys)

        return set(self.mandatory_fields).issubset(set(keys))

    def is_without_fields(self, msg):
        if self.without_fields is None:
            return True

        keys = []
        self._get_dict_keys(msg, keys)

        return not any(map(lambda key: key in keys, self.without_fields))

    def _get_dict_keys(self, dict_, result_keys):
        if isinstance(dict_, dict):
            result_keys += dict_.keys()
            map(lambda value: self._get_dict_keys(value, result_keys),
                dict_.values())