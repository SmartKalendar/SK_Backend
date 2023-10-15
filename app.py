﻿from __future__ import print_function

import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/calendar']

def main():
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

        event = {
            'summary': 'AI 설계 및 실습',
            'location': '동아대학교',
            'description': 'AI 설계 및 실습 발표 준비',
            'start': {
                'dateTime': '2023-10-16T15:00:00+09:00',
                'timeZone': 'Asia/Seoul',
            },
            'end': {
                'dateTime': '2023-10-16T18:00:00+09:00',
                'timeZone': 'Asia/Seoul',
            },
            'recurrence': [
                'RRULE:FREQ=DAILY;COUNT=1'
            ],
            # 'attendees': [
            #     {'email': 'cpprhtn@naver.com'},
            # ],
            # 'reminders': {
            #     'useDefault': False,
            #     'overrides': [
            #     {'method': 'email', 'minutes': 24 * 60},
            #     {'method': 'popup', 'minutes': 10},
            #     ],
            # },
        }

        event = service.events().insert(calendarId='primary', body=event).execute()
        print('Event created: %s' % (event.get('htmlLink')))


    except HttpError as error:
        print('An error occurred: %s' % error)


if __name__ == '__main__':
    main()