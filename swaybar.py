#!/usr/bin/env python3

# from os import system
from datetime import datetime
from psutil import sensors_battery
# from socket import gethostname, gethostbyname
from subprocess import check_output
from sys import stdout
from time import sleep
from math import floor

def write(data):
    stdout.write(data + '\n')
    stdout.flush()

def nice_bat(percent, charging):
    eight = int(round(percent * 8 / 100))
    mapping = ['░','▁','▂','▃','▄','▅','▆','▇','█']
    if eight <= 2:
        return '<span foreground="red"  background="#efefef">' + mapping[eight] + '</span>'
    if eight <= 8 and eight >= 0:
        return '<span foreground="green" background="#efefef">' + mapping[eight] + '</span>'
    return '╳'
    # This ╳ is a box drawing charcters with full width

def refresh():
    # light = system("light -G")
    # ip = gethostbyname(gethostname())
    try:
        ssid = check_output("iwgetid -r", shell=True).strip().decode("utf-8")
        ssid = 'Connected: ' + ssid if ssid else 'No Internet'
    except Exception:
        ssid = 'No Internet'
    ssid = ssid.ljust(20)
    bat_sens = sensors_battery()
    if bat_sens:
        bat_percent = int(bat_sens.percent)
        bat_symbol = nice_bat(bat_percent, bat_sens.power_plugged)
        bat_status = ("ϟ" if bat_sens.power_plugged else ' ')
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
        bat_symbol = '╳'
        bat_status = ' '
        bat_time = ' ' * 10
    date = datetime.now().strftime('%Y-%m-%d %a %H:%M:%S')
    write(f"│ {ssid} │ {bat_status}{bat_symbol} {str(bat_percent).rjust(2, '0')}% {bat_time} │ {date}")

while True:
    refresh()
    sleep(1)