#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
from googleapiclient import discovery
from httplib2 import Http
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


def call_api(json_arg):

    print('Calling Google Calendar API...')
    try:
        flags = tools.argparser.parse_args(args=[])
    except ImportError:
        flags = None

    '''
    You might want to change the location of your
    storage.json and client_id.json files in this block.
    '''
    SCOPES = 'https://www.googleapis.com/auth/calendar'
    store = file.Storage('__auth__/storage.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('__auth__/client_id.json', SCOPES)
        creds = tools.run_flow(flow, store, flags) if flags else tools.run(flow, store)
    google_calendar = discovery.build('calendar', 'v3', http=creds.authorize(Http()))

    api_event = google_calendar.events().insert(calendarId='primary',
                                                sendNotifications=True, body=json_arg).execute()

    if api_event:
        event_summary = api_event['summary']
        event_date_datetime = datetime.datetime.strptime(api_event['start']['dateTime'][:10], '%Y-%M-%d')
        event_date = datetime.datetime.strftime(event_date_datetime, '%d-%M-%Y')
        print('Success! Event created on %s: %s' % (event_date, event_summary))