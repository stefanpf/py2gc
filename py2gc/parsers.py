#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import datetime


def parse_date(date):
    '''
    Take an input in the format DDMM(YYYY), check whether it is a valid date,
    add the current or next calendar year if no YYYY is given, and return
    a string in the format "YYYY-MM-DD".
    '''
    print('Parsing date...')

    current_year = datetime.datetime.now().year

    if len(date) < 4 or len(date) > 8 or not date.isdigit():
        print('Cannot parse date: %s\nDate must be in format DDMM or DDMMYYYY.' % date)
    elif len(date) == 4:
        try:
            date_to_datetime_object = datetime.datetime.strptime(date, '%d%m')
            datestr_current_year = str(current_year) + '-' + datetime.datetime.strftime(date_to_datetime_object, '%m-%d')
            datetime_current_year = datetime.datetime.strptime(datestr_current_year, '%Y-%m-%d')
            if datetime_current_year - datetime.datetime.now() > datetime.timedelta(days=0):
                parsed_date = datestr_current_year
                return parsed_date
            else:
                parsed_date = str(current_year + 1) + datestr_current_year[4:]
                return parsed_date
        except ValueError:
            print('Cannot parse date: %s\nPlease enter a valid date.' % date)
    else:
        try:
            date_to_datetime_object = datetime.datetime.strptime(date, '%d%m%Y')
            parsed_date = datetime.datetime.strftime(date_to_datetime_object, '%Y-%m-%d')
            return parsed_date
        except ValueError:
            print('Cannot parse date: %s\nPlease enter a valid date.' % date)


def parse_location(location):

    print('Parsing location...')
    parsed_location = str(location)
    return parsed_location


def parse_note(note):

    print('Parsing note...')
    parsed_note = str(note)
    return parsed_note


def parse_time(event_time):
    '''
    Take an input in the form HHMM, check whether it is a valid time,
    and return as a string in the format "HH:MM".
    '''

    print('Parsing time...')
    if len(event_time) < 4 or len(event_time) > 4 or not event_time.isdigit():
        print('Cannot parse time: %s\nTime must be in format HHMM.' % event_time)
    else:
        try:
            time_to_datetime_object = datetime.datetime.strptime(event_time, '%H%M')
            parsed_time = datetime.datetime.strftime(time_to_datetime_object, '%H:%M')
            return parsed_time
        except ValueError:
            print('Cannot parse time: %s\nPlease enter a valid time.' % event_time)


def parse_path(path):

    print('Parsing path...')
    parsed_path = str(path)
    if os.path.isdir(path):
        return parsed_path
    else:
        print('''Cannot parse path to credentials. Will try to get credentials
              from default path __auth__.''')
        return None
