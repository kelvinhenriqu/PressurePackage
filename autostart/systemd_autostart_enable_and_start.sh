# Disable autostart of services
sudo chmod 644 /lib/systemd/system/pressurepackage.service
sudo systemctl daemon-reload
sudo systemctl enable pressurepackage.service
sudo systemctl start pressurepackage.service
sudo systemctl status pressurepackage.service


