#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
from googleapiclient import discovery
from httplib2 import Http
import oauth2client
from oauth2client import file, client, tools


def build_json(date, note, start_time, end_time, location):

    print('Building JSON event object...')

    '''
    This works in Python 3.x but throws an exception in Python 2.7:
    TypeError: Required argument 'tz' (pos 1) not found
    '''
    utc_offset = str(datetime.datetime.now().astimezone().isoformat())[-6:]

    event = {
        'summary': '',
        'location': '',
        'start': {
            'dateTime': '2015-05-28T09:00:00-07:00'
        },
        'end': {
            'dateTime': '2015-05-28T17:00:00-07:00'
        },
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'popup', 'minutes': 30},
            ],
        },
    }

    event['summary'] = note

    if location:
        event['location'] = location
    else:
        del event['location']

    if date and start_time:
        if end_time:
            event['start']['dateTime'] = date + 'T' + start_time + ':00' + utc_offset
            event['end']['dateTime'] = date + 'T' + end_time + ':00' + utc_offset
        else:
            event['start']['dateTime'] = date + 'T' + start_time + ':00' + utc_offset

            end_time = datetime.datetime.strptime(start_time, '%H:%M') + datetime.timedelta(minutes=30)
            end_time = datetime.datetime.strftime(end_time, '%H:%M')
            event['end']['dateTime'] = date + 'T' + end_time + ':00' + utc_offset
    elif date and end_time:
        event['start']['dateTime'] = date + 'T00:00:00' + utc_offset
        event['end']['dateTime'] = date + 'T' + end_time + ':00' + utc_offset
    else:
        event['start']['date'] = date
        del event['start']['dateTime']
        event['end']['date'] = date
        del event['end']['dateTime']

    return event


def call_api(json_arg, credentials_path):

    print('Calling Google Calendar API...')
    try:
        flags = tools.argparser.parse_args(args=[])
    except ImportError:
        flags = None

    '''
    If you want to change the default credentials directory
    just change path = '__auth__/' to the correct path.
    '''
    if credentials_path:
        path = credentials_path
    else:
        path = '__auth__/'

    SCOPES = 'https://www.googleapis.com/auth/calendar'
    store = file.Storage('%sstorage.json' % path)
    creds = store.get()
    if not creds or creds.invalid:
        try:
            flow = client.flow_from_clientsecrets('%sclient_id.json' % path, SCOPES)
        except (FileNotFoundError, oauth2client.clientsecrets.InvalidClientSecretsError):
            print('Cannot find client_id.json or storage.json to obtain credentials.')
            return
        creds = tools.run_flow(flow, store, flags) if flags else tools.run(flow, store)
    google_calendar = discovery.build('calendar', 'v3', http=creds.authorize(Http()))

    api_event = google_calendar.events().insert(calendarId='primary',
                                                sendNotifications=True, body=json_arg).execute()

    if api_event:
        event_summary = api_event['summary']
        try:
            event_date_datetime = datetime.datetime.strptime(api_event['start']['dateTime'][:10], '%Y-%M-%d')
        except KeyError:
            event_date_datetime = datetime.datetime.strptime(api_event['start']['date'], '%Y-%M-%d')
        event_date = datetime.datetime.strftime(event_date_datetime, '%d-%M-%Y')
        print('Success! Event created on %s: %s' % (event_date, event_summary))
    else:
        print('API call failed for some reason.')
