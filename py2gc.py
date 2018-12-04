#! python3
# -*- coding: utf-8 -*-
# A small command line utility to add events to a Google Calendar.

import argparse
from parsers import parse_date, parse_location, parse_note, parse_time
from api_call import build_json, call_api


def parse_arguments():
    p = argparse.ArgumentParser(description='''A script to add events
                                            to a Google calendar.''')
    p.add_argument('-d', '--date', help='Date of the event.', required=True)
    p.add_argument('-n', '--note', help='Description of the event.', required=True)
    p.add_argument('-s', '--start_time', help='Start time of the event.')
    p.add_argument('-e', '--end_time', help='End time of the event.')
    p.add_argument('-l', '--location', help='Location of the event.')
    return p.parse_args()


if __name__ == "__main__":

    args = parse_arguments()

    date = parse_date(args.date)
    note = parse_note(args.note)

    if args.start_time:
        start_time = parse_time(args.start_time)
    else:
        start_time = None

    if args.end_time:
        end_time = parse_time(args.end_time)
    else:
        end_time = None

    if args.location:
        location = parse_location(args.location)
    else:
        location = None

    json_event = build_json(date, note, start_time, end_time, location)

    call_api(json_event)
