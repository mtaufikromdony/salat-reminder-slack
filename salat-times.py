import os
import re
import json
import requests
import urllib.request
from datetime import datetime, timedelta, date, time
from urllib.request import urlopen

cityname = 'Jakarta'
countryname = 'Indonesia'
color = '#36a64f'
url = f'http://api.aladhan.com/v1/timingsByAddress?address={cityname},{countryname}&method=11&tune=2,2,0,4,2,4,0,2,0'
username = 'Haji Toped'
emojicon = ':kaaba:'
webhookurl = 'https://hooks.slack.com/services/xxxx/xxxxx'
print(url)

req_url = urllib.request.urlopen(url)
req_url = requests.get(url)
parsejson = req_url.json()
#print(parsejson)

with open('jadwalsalat.json', 'w') as json_file:
  json.dump(parsejson, json_file)
    
times = parsejson["data"]["timings"]
print(times)

hijriday = parsejson["data"]["date"]["hijri"]["day"]
hijriweekday = parsejson["data"]["date"]["hijri"]["weekday"]["en"]
hijrimonth = parsejson["data"]["date"]["hijri"]["month"]["en"]
hijriyear = parsejson["data"]["date"]["hijri"]["year"]
date = parsejson["data"]["date"]["readable"]

print(hijriday, hijrimonth, hijriyear)

advminutes = 10
start_message = f'*{date}* ({hijriweekday} - {hijriday} {hijrimonth}, {hijriyear}) \n\n'
pre_message = f'Hai <!channel> , mengingatkan waktu Salat & Imsakiyah untuk *{cityname}* dan sekitar nya :mosque:\n'

def convert_prayer_name(name: str) -> str:

    if name == 'Fajr':
        name = 'Subuh'
    elif name == 'Dhuhr':
        name = 'Dhuhur'
    elif name == 'Asr':
        name = 'Asar'
    elif name == 'Isha':
        name = 'Isya'
    else:
        name = name.title()

    return name
    pass


def reminder_prayertime(name: str, time: str):
    time_sched = substract_10_mins(name, time)
    today = datetime.today()
    today_date = datetime(today.year, today.month, today.day,
                          time_sched.hour, time_sched.minute)
    name = convert_prayer_name(name)
    slack_sender(name, today_date)
    pass

def fetch_prayertimes():
    os.system('for i in `atq | awk \'{print $1}\'`;do atrm $i;done')

    #getdata = json.load(open('jadwalsalat.json'))
    #jtopy=json.dumps(getdata) #json.dumps take a dictionary as input and returns a string as output.
    #dictjson=json.loads(jtopy) # json.loads take a string as input and returns a dictionary as output.
    
    for key, val in parsejson["data"]["timings"].items():
        if not (key == 'timings' or key == 'Sunset' or key== 'Midnight' or key== 'Sunrise'):
            reminder_prayertime(key, val)

    global start_message
    payloaddict = {
        'username': username,
        'color': color,
        'pretext': pre_message,
        'text': start_message,
        'icon_emoji': emojicon
    }
    json_dump = json.dumps(payloaddict)

    os.system(f'curl -X POST {webhookurl} -d \'{json_dump}\'')

    pass

def substract_10_mins(name: str, time_str: str) -> time:
    datetime_obj = datetime.strptime(time_str, '%H:%M')

    name = convert_prayer_name(name)
    time_prayer = datetime_obj.strftime('%H:%M')

    global start_message
    start_message += f'{name} {time_prayer}\n'

    datetime_obj -= timedelta(minutes=advminutes)
    #print(time_prayer)

    return datetime_obj

def slack_sender(name: str, time: datetime):
    time_str = time.strftime('%H:%M')
    time += timedelta(minutes=advminutes)
    time = time.strftime('%H:%M')

    if name == "Imsak":
       message = f'\n\n *{name} : {time}*'
       pre_message_10mins = f'*{advminutes} menit* menuju waktu *{name}* :mosque:'
    else:
       message = f'\n\n *{name} : {time}*'
       pre_message_10mins = f'*{advminutes} menit* menuju waktu Salat *{name}* :mosque:'

    payloaddict = {
        'username': username,
        'color': color,
        'pretext': pre_message_10mins,
        'text': message,
        'icon_emoji': emojicon
    }
    json_dump = json.dumps(payloaddict)

    command = f'curl -X POST {webhookurl} -d \'{json_dump}\''
    f = open(f'{name}.sh', 'w+')
    f.write(command)
    f.close()
    os.system(f'chmod +x {name}.sh')

    print(time_str)
    os.system(f'at -f {name}.sh {time_str}')

    pass

fetch_prayertimes()