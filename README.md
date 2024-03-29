# py2gc
[![Downloads](https://pepy.tech/badge/py2gc)](https://pepy.tech/project/py2gc)

A small command line utility to add events to a Google Calendar.

Project Description: https://blog.stefanpfeuffer.com/post/3/py2gc

It will:

* Take arguments from the command line.
* Parse these arguments to usable strings.
* Create a JSON object for an API call.
* Call the Google Calendar API to add the event to the calendar.

Example:

    $ ./py2gc -d 0712 -s 1900 -n "Dinner with friends"
    Parsing date...
    Parsing note...
    Parsing time...
    Building JSON event object...
    Calling Google Calendar API...
    Success! Event created on 07-12-2018: Dinner with friends

## Installation

1. Install the script via PIP or manually

Install this script via PIP with either

    pip install py2gc

or

    pip install https://github.com/stefanpf/py2gc/archive/master.zip

Or manually download this repo and install Python modules with:

    pip install -r requirements.txt

Version note: this script doesn't work on Python 2.X. If you have different Pythons installed on your system, you will want to install this using `pip3` to make sure that it will be installed under your Python 3.X.

2. Go to the Google Developer API console, add the Calendar API to your dashboard and create OAuth credentials for a local application. Download the JSON file that contains the client id and client secret and place it in "`$home/.py2gc/`" (or choose a different location and edit `call_api()` in `api_call.py` accordingly). Alternatively you can pass the path to the credentials with the `-p` argument (see below.)

3. On the first run, the authenticator will open a browser window and ask the user to log in with their Google account to authenticate the API use. That Google account's primary calendar will be used unless a specific Calendar ID is passed via the `-i --calendarid` argument.

## Usage

The arguments are:

    py2gc
    -d --date       # Date of the event either as DDMM or DDMMYYYY. REQUIRED.
    -n --note       # Description of the event. REQUIRED.
    -s --starttime  # Start time of the event, as HHMM in 24hr format.
    -e --endtime    # End time of the event, as HHMM in 24hr format.
    -l --location   # Location of the event.
    -i --calendarid # Google Calendar ID. Default is primary.
    -p --path       # Path to your Google Calendar API credentials.
    -h --help       # Help.

### -d --date (REQUIRED)

Expects the event date in the format DDMM or DDMMYYYY.

If no year is given, it will assume the current calendar year if the given date is in the future and the next calendar year if the date is in the past. Put differently: if no year is given, the event will be placed on the first future occurence of the date.

Example:

    (If today is the 04 April 2018)
    -d 1004 will produce 10 April 2018
    -d 0302 will produce 3 February 2019
    -d 03022018 will produce 3 February 2018

### -n --note (REQUIRED)

Expects an event description/summary.

Example:

    -n "dinner at sam's"

### -s --starttime (OPTIONAL)

Expects the event start time in the format HHMM.

Example:

    -s 1315

Note: If no start time is supplied, the event will be treated as "all-day".

### -e --endtime (OPTIONAL)

Expects the event end time in the format HHMM.

Example:

    -e 0745

Note: If a start time is supplied but no end time, the event will be treated as 30 minute duration. If an end time is supplied but no start time, the event will be treated as beginning at 00:00 hours on the date supplied and ending at the supplied end time.

### -l --location (OPTIONAL)

Expects an event location.

Example:

    -l 'library'

### -i --calendarid (OPTIONAL)

Expects a Google Calendar ID.

Example:

    -i S0MeTypeofString@group.calendar.google.com

Use this argument to write the event to a specific calendar. If no Calendar ID is given, the script will default to `'primary'`.

### -p --path (OPTIONAL)

Expects a file path.

Example:

    -p /usr/test/path/to/credentials

Note: by default, the script will expect to find the Google API credentials (client_id.json and, after the first run, storage.json) in a folder called `$home/.py2gc/`. If you want to store your credentials elsewhere, you can either pass the correct path via this argument or change the variable `path = '$home/.py2gc/'` in the `call_api()` function.

### Usage Examples

    py2gc -d 0308 -n "pycon europe"

This will create an all-day event on the next 3 August with a description of "pycon europe".

    py2gc -d 24122018 -n 'christmas dinner at home' -s 1700

This will create an event on 24 December 2018, starting at 17:00 hrs with a default duration of 30 minutes and a description of "christmas dinner at home".

    py2gc -d 24122018 -n "christmas dinner at home" -s 1700 -e 2200

This will create an event on 24 December 2018, starting at 17:00 hrs and ending at 22:00 hrs and with a description of "christmas dinner at home"

    py2gc -d 2412 -n "christmas dinner" -s 1700 -e 2200 -l "home"

This will create an event on the next 24 December, starting at 17:00 hrs and ending at 22:00 hrs, with a description of "christmas dinner" and a location of "home".

### Output Example

    $ ./py2gc.py -d 0712 -s 1900 -n "Dinner with friends"
        Parsing date...
        Parsing note...
        Parsing time...
        Building JSON event object...
        Calling Google Calendar API...
        Success! Event created on 07-12-2018: Dinner with friends

## Planned Features

* Support multi-day events.
* Fix treatment of 29 February when calendar year is not supplied.
