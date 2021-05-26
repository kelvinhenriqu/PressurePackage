# Disable autostart of services
sudo systemctl daemon-reload
sudo systemctl stop pressurepackage.service
sudo systemctl disable pressurepackage.service
sudo systemctl status pressurepackage.service
