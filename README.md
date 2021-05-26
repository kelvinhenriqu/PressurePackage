# PressurePackage

[![AUTOSTART](https://img.shields.io/badge/autostart%20service%20-%23323330.svg?&style=for-the-badge&logo=autostart%20ff&logoColor=black&color=FF0000)](https://github.com/kelvinhenriqu/PressurePackage/tree/main/autostart)

The pressurepackage.service need to be moved to /lib/systemd/system/
can be done using the following command:

sudo cp pressurepackage.service /lib/systemd/system/pressurepackage.service

than execute the following to start the autostart service:

sh systemd_autostart_enable_and_start.sh

you can execute the following to stop the service temporaly

sh systemd_autostart_disable_and_stop.sh

the iniciar.sh need to be in "/home/pi" folder
