# Announcements for HackTheMidlands

## Running

Installation of dependencies:

    $ pip install -r requirements.txt

You'll need to enable access to your google account by going to:

[https://developers.google.com/docs/api/quickstart/python](https://developers.google.com/docs/api/quickstart/python)

And also enable the Google docs API for your application.

And then specify which google sheet to use by setting the following environment keys:

* SHEET (ID of your google doc sheet)
* SHEET_RANGE (range for the query)

And also specify the folowing:

* SHEETS_TOKEN_PATH - path to the token after you login to google sheets
* SHEETS_CREDENTIALS - path to your `credentials.json`

And also register a pusher account and set your credentials in the following environmental keys:

* PUSHER_APP_ID
* PUSHER_KEY
* PUSHER_SECRET
* PUSHER_CLUSTER
* PUSHER_CHANNEL

Running:

    $ python app.py

Running in development mode:

    $ python app.py --debug

