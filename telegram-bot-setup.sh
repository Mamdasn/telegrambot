#!/bin/sh

[ -z $IP_ADDRESS ] &&
	read -p "Enter the IP address of your vps: " IP_ADDRESS &&
		sed -i "s/IP_ADDRESS\=/IP_ADDRESS\=$IP_ADDRESS/g" setenv.sh
[ -z $TG_BOT_TOKEN ] &&
	read -p "Enter the http api token of your telegram bot: " TG_BOT_TOKEN &&
		sed -i "s/TG_BOT_TOKEN\=/TG_BOT_TOKEN\=$TG_BOT_TOKEN/g" setenv.sh

PORTSSL=443

echo Setting up ssl files
mkdir SSLFILES
cd SSLFILES
openssl req -newkey rsa:8192 -sha256 -nodes -keyout YOURPRIVATE.key -x509 -days 365 -out YOURPUBLIC.pem -subj "/C=DE/ST=Berlin/L=Berlin/O=FERI Company/CN"
SSL_PUBLIC=$(realpath YOURPUBLIC.pem)
SSL_PRIVATE=$(realpath YOURPRIVATE.key)
curl -F "ip_address=$IP_ADDRESS" -F "url=https://$IP_ADDRESS:$PORTSSL/" -F "certificate=@YOURPUBLIC.pem" https://api.telegram.org/bot$TG_BOT_TOKEN/setWebhook
cd ..

echo Downloading a list of telegram server ips to make a whitelist for nginx...
IPLIST=$(curl -s https://core.telegram.org/resources/cidr.txt)
WHITE_LISTED_IPS=$(echo "$IPLIST" | awk '{print "    allow " $0";"}')
echo Done.

echo
echo Setting up the white listed IPs in the nginx configuration file
sed -i "s/WHITE_LISTED_IPS/$WHITE_LISTED_IPS/g" portforwarding.conf

echo "Run this command to start the telegram bot: source setenv.sh && docker compose up"
