@echo off
echo Passing through usb devices to docker ...
usbipd attach -i 04e8:6860
echo Starting Program ...
set CONTAINER_NAME="sips"
docker run -d -p 3000:3000 --name sips -itd -v .\shared\results:/src/shared/results --gpus all sips
docker exec sips scripts/entrypoint.sh
docker exec sips node /src/SIP-GUI/main.js
start /wait firefox "http://localhost:3000"
docker exec -it sips scripts/exit.sh
docker container rm -f sips