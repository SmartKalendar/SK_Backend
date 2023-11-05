from flask import Flask, request, jsonify
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import json
import datetime
import os.path

app = Flask(__name__)

SCOPES = ['https://www.googleapis.com/auth/calendar']

@app.route('/create_event', methods=['POST'])
def test():
    gpt_result = request.get_json()
    # print(gpt_result)
    gpt_result = json.loads(gpt_result, strict=False)
    print(gpt_result)
    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)

        event = gpt_result

        event = service.events().insert(calendarId='primary', body=event).execute()
        print('Event created: %s' % (event.get('htmlLink')))
        return "Event created"


    except HttpError as error:
        print('An error occurred: %s' % error)
        return "An error occurred"



if __name__ == '__main__':
    app.run(port=3000)
