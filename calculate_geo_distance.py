import os
from time import sleep

import datetime
import requests

# DIR and FILES
HOME_DIR = os.getenv("HOME")
SOURCE_FILE = '/Desktop/geo_location.csv'
OUTPUT_FILE = '/Desktop/geo_location_result.csv'

# CALL PARAMS
FORMAT = 'json'
UNITS = 'metric'
MODE = 'transit'
DEPARTURE_TIME = '1475485200'   # 9:00am
GOOGLE_KEY = 'here_your_google_key'
BASE_URL_4_DISTANCE = 'https://maps.googleapis.com/maps/api/distancematrix'
BASE_URL_4_GEOCODE = 'https://maps.googleapis.com/maps/api/geocode'
BASE_URL_4_TIMEZONE = 'https://maps.googleapis.com/maps/api/timezone'

# OTHER PARAMS
CHAR_SEPARATOR = '@'

def get_csv_in_line(_origin, _destination, _distance, _duration, _abs_tz, _lat_orig, _lng_orig, _lat_dest, _lng_dest):
    return _origin + CHAR_SEPARATOR + \
           _destination + CHAR_SEPARATOR + \
           str(_distance) + CHAR_SEPARATOR + \
           str(_duration) + CHAR_SEPARATOR + \
           str(_abs_tz) + CHAR_SEPARATOR + \
           str(_lat_orig) + CHAR_SEPARATOR + \
           str(_lng_orig) + CHAR_SEPARATOR + \
           str(_lat_dest) + CHAR_SEPARATOR + str(_lng_dest)

f_in = open(HOME_DIR + SOURCE_FILE, 'r')
f_out = open(HOME_DIR + OUTPUT_FILE, 'w')

cnt = 1

for line in f_in:
    origin = line.split(CHAR_SEPARATOR)[0]
    destination = line.split(CHAR_SEPARATOR)[1].replace('\r\n', '')
    call = BASE_URL_4_DISTANCE+'/'+FORMAT+'?units='+UNITS+'&origins='+origin+'&destinations='+destination+'&key='+GOOGLE_KEY
    r = requests.get(call)
    data = r.json()

    distance = duration = ''

    if len(data['rows']) > 0 and len(data['rows'][0]['elements']) > 0:
        if 'distance' in data['rows'][0]['elements'][0].keys():
            distance = data['rows'][0]['elements'][0]['distance']['value']
        if 'duration' in data['rows'][0]['elements'][0].keys():
            duration = data['rows'][0]['elements'][0]['duration']['value']

    call = BASE_URL_4_GEOCODE+'/'+FORMAT+'?address='+origin+'&key='+GOOGLE_KEY
    r = requests.get(call)
    data = r.json()

    lat_orig = 0
    lng_orig = 0
    if len(data['results']) > 0:
        lat_orig = data['results'][0]['geometry']['location']['lat']
        lng_orig = data['results'][0]['geometry']['location']['lng']

    call = BASE_URL_4_GEOCODE + '/' + FORMAT + '?address=' + destination + '&key=' + GOOGLE_KEY
    r = requests.get(call)
    data = r.json()

    lat_dest = 0
    lng_dest = 0
    if len(data['results']) > 0:
        lat_dest = data['results'][0]['geometry']['location']['lat']
        lng_dest = data['results'][0]['geometry']['location']['lng']

    call = BASE_URL_4_TIMEZONE + '/' + FORMAT + '?location=' + str(lat_dest) + ',' + str(lng_dest) + '&timestamp=' + \
           datetime.date.today().strftime("%s") + '&key=' + GOOGLE_KEY
    r = requests.get(call)
    data = r.json()

    timezone_dst = data.get('rawOffset', 0)

    call = BASE_URL_4_TIMEZONE + '/' + FORMAT + '?location=' + str(lat_orig) + ',' + str(lng_orig) + '&timestamp=' + \
           datetime.date.today().strftime("%s") + '&key=' + GOOGLE_KEY
    r = requests.get(call)
    data = r.json()

    timezone_orig = data.get('rawOffset', 0)

    abs_timezone = abs(timezone_orig - timezone_dst)

    res = get_csv_in_line(origin, destination, distance, duration, abs_timezone, lat_orig, lng_orig, lat_dest, lng_dest)

    print str(cnt) + ': ' + res
    f_out.write(res + '\n')

    # sleep(0.05)

    cnt += 1
    
    # if cnt == 20:
    #     break
