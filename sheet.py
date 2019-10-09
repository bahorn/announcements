import datetime
import os.path
import pickle
from pprint import pprint

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from Announcement import Announcement


class Sheets:
    def __init__(self, SPREADSHEET_ID, RANGE):
        self.SPREADSHEET_ID = SPREADSHEET_ID
        self.RANGE = RANGE
        self.SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        self.creds = None
        self.service = None

    def credentials(self):
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        self.creds = creds

    def build_service(self):
        self.service = build('sheets', 'v4', credentials=self.creds)

    def print_range(self):
        sheet = self.service.spreadsheets()
        result = sheet.values().get(spreadsheetId=self.SPREADSHEET_ID, range=self.RANGE).execute()
        values = result.get('values', [])

        if not values:
            print('No data found.')
        else:
            for row in values:
                print(row)

    def get_all(self):
        sheet = self.service.spreadsheets()
        result = sheet.values().get(spreadsheetId=self.SPREADSHEET_ID, range=self.RANGE).execute()
        values = result.get('values', [])

        return self.parse_all(values[1:])

    def get_active(self):
        return list(filter(lambda x: x.active is True, self.get_all()))

    def get_current_active(self, delta: datetime.timedelta):
        now = datetime.datetime.now()
        print("Between ({}) and ({})".format(str(now - delta), str(now + delta)))
        for a in self.get_active():
            print(a.time)
        return list(filter(lambda x: now - delta <= x.time <= now + delta, self.get_active()))

    @staticmethod
    def parse_all(values):
        new_values = []
        for value in values:
            time = datetime.datetime.strptime(value[2], "%d/%m/%Y %H:%M:%S")
            new_values.append(
                Announcement(uid=value[0], created_at=value[1], time=time, title=value[3], body=value[4],
                             active=(value[5] == 'TRUE')))
        return new_values

    def get_first(self):
        return self.get_all()[1]

    def set_active(self, announcement: Announcement, active: bool):
        sheet = self.service.spreadsheets().values()
        range_name = "F" + str(int(announcement.uid) + 1)
        value = str(active).upper()
        body = {
            'values': [[value]],
        }
        pprint(body)
        sheet.update(
            spreadsheetId=self.SPREADSHEET_ID, range=range_name,
            valueInputOption='RAW', body=body).execute()

