from datetime import datetime


class Announcement:

    def __init__(self, uid: int, created_at: datetime, time: datetime, title: str, body: str, active: bool):
        self.uid = uid
        self.time_id = created_at
        if time is None:
            self.time = datetime.now()
        else:
            self.time = time
        self.title = title
        self.body = body
        self.active = active

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __hash__(self):
        return hash(self.time_id)

    def __lt__(self, other):
        return self.time < other.time

    def __gt__(self, other):
        return self.time > other.time

    def __cmp__(self, other):
        return self.time < other.time