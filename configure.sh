#sudo apt-get install python3-pip
#pip install -r req.txt

#Generar licencia
#sudo python app/Licencia/Instalador.py


#echo Instalando aplicacion
#sudo rm -r /usr/share/eum
#sudo cp -r ../eum/ /usr/share/

#sudo chmod 777 -R /usr/share/eum/iconos

#sudo rm /usr/local/share/applications/inicio.desktop
#sudo cp inicio.desktop /usr/share/applications/

sudo systemctl stop vista.service
sudo cp vista.service /lib/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable vista.service
sudo systemctl start vista.service
#sleep 5
sudo systemctl stop app.service
sudo cp app.service /lib/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable app.service
sudo systemctl start app.service
#sudo systemctl status vista.service
#echo hay fue
#read -p 'Numero de equipo: ' numero
#cd /usr/share/eum/vista
#sudo python manage.py createsuperuser
#sleep 3
#/usr/bin/firefox 0.0.0.0:8000 
#sleep 5
#xdotool key F11
