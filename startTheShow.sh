SCRIPT_PATH=$(readlink -f "$0")
SCRIPT_DIR=$(dirname "$SCRIPT_PATH")
docker container rm -f sips
echo Killing adb
pkill adb
echo Starting Program...
docker run --gpus all --name sips -itd -p 3000:3000 --privileged -v /dev/bus/usb:/dev/bun/usb -v ./src/shared/results:/src/shared/results sips
docker exec sips scripts/entrypoint.sh
brave "http://localhost:3000" &
docker exec sips node /src/SIP-GUI/main.js
echo "waiting for firefox to close"
docker exec sips scripts/start_gui.sh
wait $!
docker exec -it sips scripts/exit.sh
docker container rm -f sips