## بِسْمِ اللهِ الرَّحْمٰنِ الرَّحِيْمِ

# salat-reminder-slack

Salat Prayer Times bot for Slack integration and use API from http://api.aladhan.com

## Requirements

* Python 3
* Git
* Slack Incoming Webhook registration on your workspace at https://my.slack.com/services/new/incoming-webhook


## Setup

- Clone this repo.
```
git clone https://github.com/mtaufikromdony/salat-reminder-slack.git
```
- Edit the parameter, example:
```
cityname = 'Jakarta'
countryname = 'Indonesia'
color = '#36a64f'
url = f'http://api.aladhan.com/v1/timingsByAddress?address={cityname},{countryname}&method=11&tune=2,2,0,4,2,4,0,2,0'
username = 'Haji Toped'
emojicon = ':kaaba:'
webhookurl = 'https://hooks.slack.com/services/xxxx/xxxxx'
```
- Install at for schedule command and start the service
```
yum -y install at

sudo service atd start
systemctl enable atd
```
- Install python requests library
```
pip3 install requests
```
- Start the app with this command. NOTE that you need to have python3 installed.
```
$ python3 salat-times.py
```
- check at command job schedule
```
atq

220     Wed Apr 22 04:37:00 2020 a root
221     Wed Apr 22 11:55:00 2020 a root
223     Tue Apr 21 17:53:00 2020 a root
224     Tue Apr 21 19:02:00 2020 a root
225     Wed Apr 22 04:27:00 2020 a root
``` 
- Setup a cron job to automate it
```
30 0 * * * cd /path/prayertimes/ && python3 /path/prayertimes.py >> prayertimes.log 2>&1
```
- Delete at command job schedule (if needed)
```
rm -rf /var/spool/at/*
```

Here's how it will look like in your channel: ![Slack BOT Integration](screenshot.png)

Tested using Centos 7
