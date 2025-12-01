@echo off
echo Copying adb keys ...
copy /Y %USERPROFILE%\.android\ .
docker build -t sips .