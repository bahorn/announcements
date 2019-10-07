from datetime import datetime


class Announcement:

    def __init__(self, time_id: datetime, time: datetime, title: str, body: str):
        self.time_id = time_id
        if time is None:
            self.time = datetime.now()
        else:
            self.time = time
        self.title = title
        self.body = body

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __hash__(self):
        return hash(self.time_id)
