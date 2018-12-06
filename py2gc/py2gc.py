#!/usr/bin/env python
# -*- coding: utf-8 -*-
# A small command line utility to add events to a Google Calendar.

import argparse
from parsers import parse_date, parse_location, parse_note, parse_time, parse_path
from api_call import build_json, call_api


def parse_arguments():
    p = argparse.ArgumentParser(description='''A script to add events
                                            to a Google calendar.''')
    p.add_argument('-d', '--date', help='''Date of the event, either as DDMM
                   or DDMMYYYY.''', required=True)
    p.add_argument('-n', '--note', help='Description of the event.',
                   required=True)
    p.add_argument('-s', '--starttime', help='''Start time of the event,
                    as HHMM in 24hr format.''')
    p.add_argument('-e', '--endtime', help='''End time of the event,
                    as HHMM in 24hr format.''')
    p.add_argument('-l', '--location', help='Location of the event.')
    p.add_argument('-i', '--calendarid', help='Google CalendarID. Default is primary.')
    p.add_argument('-p', '--path', help='''Path to your Google Calendar API
                    credentials.''')
    return p.parse_args()


if __name__ == "__main__":

    args = parse_arguments()

    date = parse_date(args.date)
    note = parse_note(args.note)

    if args.starttime:
        start_time = parse_time(args.starttime)
    else:
        start_time = None

    if args.endtime:
        end_time = parse_time(args.endtime)
    else:
        end_time = None

    if args.location:
        location = parse_location(args.location)
    else:
        location = None

    if args.path:
        credentials_path = parse_path(args.path)
    else:
        credentials_path = None

    if args.calendarid:
        calendar_id = args.calendarid
    else:
        calendar_id = None

    if date and note:
        json_event = build_json(date, note, start_time, end_time, location)
        call_api(json_event, credentials_path, calendar_id)
    else:
        print('Please enter a valid date and note.')
