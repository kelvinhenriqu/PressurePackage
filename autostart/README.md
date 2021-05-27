# PressurePackage


The pressurepackage.service need to be moved to /lib/systemd/system/
can be done using the following command:

```python
sudo cp pressurepackage.service /lib/systemd/system/pressurepackage.service
```
than execute the following to start the autostart service:
```python
sh systemd_autostart_enable_and_start.sh
```
you can execute the following to stop the service temporaly
```python
sh systemd_autostart_disable_and_stop.sh
```
the iniciar.sh need to be in "/home/pi" folder
```python
cp iniciar.sh ~/iniciar.sh
```
## 📫 Connections :

[![AUTOSTART](https://img.shields.io/badge/Main%20-%23323330.svg?&style=for-the-badge&logo=Main%20ff&logoColor=black&color=8000FF)](https://github.com/kelvinhenriqu/PressurePackage/tree/main/)
