docker build -t iot-api-endpoint:latest .
docker container stop mycontainer
docker container rm mycontainer
echo "Press button on bridge to complete setup"
docker container run -d --name=mycontainer --restart=unless-stopped -p 192.168.1.31:80:80 iot-api-endpoint:latest

