#!/usr/bin/env python3

# from os import system
from datetime import datetime
from psutil import sensors_battery
# from socket import gethostname, gethostbyname
from subprocess import check_output
from sys import stdout
from time import sleep
from math import floor
from re import search

def write(data):
    stdout.write(data + '\n')
    stdout.flush()

def nice_bat(percent):
    eigth = int(round(percent * 8 / 100))
    mapping = ['□□□□','◧□□□','■□□□','■◧□□','■■□□','■■◧□','■■■□','■■■◧','■■■■']
    if eigth <= 2:
        return '<span foreground="red">' + mapping[eigth] + '</span>'
    if eigth <= 8 and eigth >= 0:
        return mapping[eigth]
    return '◪◩◪◩'

def nice_vol(percent):
    fourth = int(round(percent * 4 / 100))
    mapping = ['□□','◧□','■□','■◧','■■']
    if fourth <= 8 and fourth >= 0:
        return mapping[fourth]
    return '◪◩'

def refresh():
    # light = system("light -G")
    # ip = gethostbyname(gethostname())
    try:
        ssid = check_output("iwgetid -r", shell=True).strip().decode("utf-8")
        ssid = 'Connected: ' + ssid if ssid else 'No Internet'
    except Exception:
        ssid = 'No Internet'
    try:
        v = search(r"\[(\d{1,3})%\].*\[on\]", check_output(['amixer','get','Master']).decode('utf-8'))
        if v:
            volume = v.group(1).rjust(2, '0').rjust(3)
            nvol = nice_vol(int(volume))
        else:
            volume = ' M '
            nvol = '◫◫'
    except Exception:
        volume = ' --'
        nvol = '◪◩'
    ssid = ssid.ljust(20)
    bat_sens = sensors_battery()
    if bat_sens:
        bat_percent = int(bat_sens.percent)
        bat_symbol = nice_bat(bat_percent)
        # bat_status = ("ϟ" if bat_sens.power_plugged else ' ')
        bat_status = ("+" if bat_sens.power_plugged else ' ')
        if bat_sens.secsleft and bat_sens.secsleft >= 0:
            bat_time = (str(floor(bat_sens.secsleft / 3600)).rjust(2)
                    + ':'
                    + str(floor(bat_sens.secsleft % 3600 / 300) * 5).rjust(2, '0') + ' left')
        elif bat_sens.power_plugged:
            bat_time = 'Charging  '
        else:
            bat_time = ' ' * 10
    else:
        bat_percent = '--'
        bat_symbol = '◪◩◪◩'
        bat_status = ' '
        bat_time = ' ' * 10
    date = datetime.now().strftime('%Y-%m-%d %a %H:%M:%S')
    write(f"{nvol} {volume}% │ {ssid} │ {bat_symbol}{bat_status} {str(bat_percent).rjust(2, '0').rjust(3)}% {bat_time} │ {date}")

while True:
    refresh()
    sleep(.5)
