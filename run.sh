#!/bin/sh
cd /home/g2corretora/sistema.g2corretora.com.br
screen -m -d -S g2 flask run --port=5002 --debug=true --host="0.0.0.0" --cert=../ssl/certs/sistema_g2corretora_com_br_a4c7f_19251_1669889305_ad3dfb566c05b98143d221b43261d932.crt --key=../ssl/keys/a4c7f_19251_776d999e8a12d4d31683cd7deecce633.key