#!/usr/bin/env python3
import datetime
import json
import sys
import threading
import time
import traceback

import pusher

from Config import Settings

from sheet import Sheets
from Announcement import Announcement

sheet: Sheets = Sheets(Settings.SHEET, Settings.SHEET_RANGE)
# Should consider catching exceptions here
sheet.credentials()
sheet.build_service()

posts: [Announcement] = sheet.get_past()
print('Preloaded posts:', posts, file=sys.stderr)

# run code in background
def background():
    global posts
    global sheet
    while True:
        print('loading announcements... ', end='')
        try:
            announcements = sheet.get_current_active(
                datetime.timedelta(minutes=5)
            )
            if len(announcements) > 0:
                announcement = announcements.pop(0)
                text = str(json.dumps(announcement.__dict__, default=str))
                send_announcement(text)
                sheet.set_active(announcement, False)

                posts = sheet.get_past()
                print()
                print('Updated posts:', posts, file=sys.stderr)
            else:
                print("no announcements")

            time.sleep(3)
        except:
            traceback.print_last(file=sys.stderr)
            time.sleep(5)

def send_announcement(message):
    print('Announcing: ' + str(message))
    channels_client = pusher.Pusher(
        app_id=Settings.PUSHER_APP_ID,
        key=Settings.PUSHER_KEY,
        secret=Settings.PUSHER_SECRET,
        cluster=Settings.PUSHER_CLUSTER,
        ssl=True
    )

    channels_client.trigger(Settings.PUSHER_CHANNEL, 'new', message)
