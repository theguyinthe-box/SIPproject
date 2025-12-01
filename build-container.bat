@echo off
echo Copying adb keys ...
copy /Y %USERPROFILE%\.android\ .\src\
docker build -t sips .