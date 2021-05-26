echo "$(tput setaf 1)instalando drivers novamente$(tput setaf 7)"
sudo apt-get install Bluetooth bluez blueman
echo "$(tput setaf 1)etapa finalizada, seguindo para a proxima$(tput setaf 7)"
sudo apt-get install bluez bluez-firmware
echo "$(tput setaf 1)etapa finalizada, seguindo para a proxima$(tput setaf 7)"
sudo systemctl daemon-reload
echo "$(tput setaf 1)etapa finalizada, seguindo para a proxima$(tput setaf 7)"
sudo systemctl restart bluetooth
echo "$(tput setaf 1)etapa finalizada, seguindo para a proxima$(tput setaf 7)"
sudo usermod -G bluetooth -a pi
echo "$(tput setaf 1)etapa finalizada, seguindo para a proxima$(tput setaf 7)"
sudo cat /etc/group | grep bluetooth
echo "$(tput setaf 1)etapa finalizada$(tput setaf 7)"
echo "finalisado, execute 4.sh$(tput setaf 7)"
