SCRIPT_PATH=$(readlink -f "$0")
SCRIPT_DIR=$(dirname "$SCRIPT_PATH")
docker container rm -f sips
echo Killing adb
pkill adb
echo Starting Program...
docker run --gpus all --name sips -p 3000:3000 --privileged -v /dev/bus/usb:/dev/bun/usb -v ./src/shared:/src/shared sips scripts/entrypoint.sh &
brave "http://localhost:3000" &
echo "waiting for firefox to close"
wait $!
docker exec -it sips bash -c "sh ~/src/scripts/exit.sh"
docker container rm -f sips