#!/usr/bin/env python3

import os
import time


def update():
    os.system('mv firmware.py backup/firmware.py.backup')
    time.sleep(1)
    os.system('wget -O firmware.py https://raw.githubusercontent.com/kelvinhenriqu/PressurePackage/main/firmware.py')
    print('successfully updated')
    print('starting main program')
    time.sleep(5)
    os.system('python3 firmware.py')


def checkupdate():
    os.system('wget -O Version.txt https://raw.githubusercontent.com/kelvinhenriqu/PressurePackage/main/Version.txt')

    new_version = ''
    with open('Version.txt', 'r') as f:
        for line in f:
            line = line.strip()
            if '__VERSION__' in line:
                _, new_version = line.split('=', maxsplit=1)
                new_version = new_version.strip()
                break
    print('Server version is:', new_version)


    with open('firmware.py', 'r') as f:
        for line in f:
            line = line.strip()
            if '__VERSION__' in line:
                _, current_version = line.split('=', maxsplit=1)
                current_version = current_version.strip()
                break
    print('Current version is:', current_version)


    if current_version < new_version:
        print('need to update')
        os.system('rm Version.txt')
        update()
    else:
        print("don't neet to update")
        os.system('rm Version.txt')
        print('starting main program')
        os.system('python3 firmware.py')


checkupdate()

