echo Killing adb
pkill adb
echo Starting Program ...
set CONTAINER_NAME="sips"
docker run --gpus all --name sips -it -p 3000:3000 --privileged -v /dev/bus/usb:/dev/bun/usb --mount type=bind,source=./src/shared,target=/src/shared sips
firefox "http://localhost:3000" &
echo "waiting for firefox to close"
wait $!
docker exec -it %CONTAINER_NAME% bash -c "sh ~/src/scripts/exit.sh"
docker stop %CONTAINER_NAME%