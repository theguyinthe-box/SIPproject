SCRIPT_PATH=$(readlink -f "$0")
SCRIPT_DIR=$(dirname "$SCRIPT_PATH")
docker container rm -f sips
echo Killing adb
pkill adb
echo Starting Program...
docker run --gpus all --name sips -itd -p 3000:3000 --privileged -v /dev/bus/usb:/dev/bun/usb -v ./src:/src sips
sh scripts/clear_shared_folders.sh
sh ./src/scripts/clear_shared_folders.sh
docker exec sips scripts/entrypoint.sh
firefox "http://localhost:3000" &
docker exec sips scripts/start_gui.sh
echo "waiting for firefox to close"
wait $!
docker exec -it sips scripts/exit.sh
docker contianer stop sips
docker container rm -f sips
