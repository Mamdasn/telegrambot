#!/bin/sh

PORTSSL=443

[ -z $IP_ADDRESS ] &&
	echo set the IP_ADDRESS by running: export IP_ADDRESS={IP_ADDRESS}. &&
		return
[ -z $TG_BOT_TOKEN ] &&
	echo set the TG_BOT_TOKEN by running: export TG_BOT_TOKEN={TG_BOT_TOKEN}. &&
		return


echo Setting up ssl files
mkdir -p SSLFILES
cd SSLFILES
openssl req -newkey rsa:8192 -sha256 -nodes -keyout YOURPRIVATE.key -x509 -days 365 -out YOURPUBLIC.pem -subj "/C=US/ST=New York/L=Brooklyn/O=Example Brooklyn Company/CN=8.8.8.8"
SSL_PUBLIC=$(realpath YOURPUBLIC.pem)
SSL_PRIVATE=$(realpath YOURPRIVATE.key)
curl -F "ip_address=$IP_ADDRESS" -F "url=https://$IP_ADDRESS:$PORTSSL/" -F "certificate=@YOURPUBLIC.pem" https://api.telegram.org/bot$TG_BOT_TOKEN/setWebhook
cd ..

echo
echo Downloading a list of telegram server ips to make a whitelist for nginx...
IPLIST=$(curl -s https://core.telegram.org/resources/cidr.txt)
WHITE_LISTED_IPS=$(echo "$IPLIST" | awk '{print "		allow " $0";"}')
# Escape forward slashes and replace newlines with '\n' to prepare the data for sed
WHITE_LISTED_IPS_ESCAPED=$(echo "$WHITE_LISTED_IPS" | sed 's#/#\\/#g' | awk '{printf "%s\\n", $0}')

echo
echo Setting up the white listed IPs in the nginx configuration file
sed -i "s#WHITE_LISTED_IPS#$WHITE_LISTED_IPS_ESCAPED#g" portforwarding.conf
echo Done.

echo "Run this command to start the telegram bot: source setenv.sh && docker compose up"
