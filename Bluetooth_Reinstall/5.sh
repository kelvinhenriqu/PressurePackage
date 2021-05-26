echo "verificando status do bluetooth"
sudo systemctl status bluetooth
echo "$(tput setaf 1)dando start no bluetoooth$(tput setaf 7)"
sudo systemctl start bluetooth
sudo systemctl status bluetooth
echo "$(tput setaf 1)verifique manualmente se o bluetooth esta funcionando, caso negativo execute 6.sh$(tput setaf 7)"
