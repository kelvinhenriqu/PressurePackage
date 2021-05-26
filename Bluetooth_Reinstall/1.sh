echo "$(tput setaf 1)processo para reinstalar drivers bluetooth em caso de erro$(tput setaf 7)"
echo "$(tput setaf 1)desinstalando drivers antigos$(tput setaf 7)"

sudo apt-get remove bluetooth 
echo "$(tput setaf 1)etapa finalizada, seguindo para a proxima$(tput setaf 7)"
sudo apt-get remove bluez 
echo "$(tput setaf 1)etapa finalizada, seguindo para a proxima$(tput setaf 7)"
sudo apt-get remove blueman
echo "$(tput setaf 1)etapa finalizada, seguindo para a proxima$(tput setaf 7)"
sudo apt-get autoclean
echo "$(tput setaf 1)etapa finalizada, seguindo para a proxima$(tput setaf 7)"
sudo apt-get update
echo "$(tput setaf 1)etapa finalizada, seguindo para a proxima$(tput setaf 7)"
sudo apt-get upgrade -y
echo "$(tput setaf 1)etapa finalizada, seguindo para a proxima$(tput setaf 7)"
sudo apt-get autoclean
echo "$(tput setaf 1)etapa finalizada$(tput setaf 7)"
echo "execute o script 2.sh$(tput setaf 7)"
