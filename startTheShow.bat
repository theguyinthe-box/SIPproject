@echo off
echo Copying adb keys ...
copy /Y .\adbkey* %USERPROFILE%\.android\
echo Passing through usb devices to docker ...
usbipd attach -i 04e8:6860
echo Starting Program ...
set CONTAINER_NAME="sips"
docker run -d -p 3000:3000 --name %CONTAINER_NAME% --volume .\data --gpus all SIPS_Container
start /wait chrome "http://localhost"
docker exec -it %CONTAINER_NAME% bash -c "sh ~/src/scripts/exit.sh"
docker stop %CONTAINER_NAME%