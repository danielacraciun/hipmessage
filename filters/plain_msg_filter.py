from filters.base_filter import BaseFilter


class PlainMessageFilter(BaseFilter):
    # Get all messages that are not card
    without_fields = ['card']