import os.path
import pickle

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


class Sheets:
	# If modifying these scopes, delete the file token.pickle.
	

	# The ID and range of a sample spreadsheet.
	# SPREADSHEET_ID = '13_6S-dBLfNY0eKRULjIliKjr-sLfuv4iS5mX-0e78pA'
	# RANGE = 'A1:C'
	# creds = None
	# service = None
	def __init__(self,SPREADSHEET_ID,RANGE):
		self.SPREADSHEET_ID=SPREADSHEET_ID
		self.RANGE=RANGE
		self.SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
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
		return values
	
	
	def get_first(self):
		return self.get_all()[1]


# def main():
# 	service = build('sheets', 'v4', credentials=creds)

# 	# Call the Sheets API
	


if __name__ == '__main__':
	s = Sheets('13_6S-dBLfNY0eKRULjIliKjr-sLfuv4iS5mX-0e78pA','A1:C')
	s.credentials()
	s.build_service()
	# s.print_range()
	print(s.get_first())

	# main()
