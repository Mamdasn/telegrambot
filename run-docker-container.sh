docker build -t telegrambot:0.0.0 .
docker run  -d -p 443:443 -e IP_ADDRESS=${IP_ADDRESS} -e TG_BOT_TOKEN=${TG_BOT_TOKEN} -v ./output:/app/output --name telegrambot telegrambot:0.0.0
