@echo off
echo Copying adb keys ...
copy /Y .\adbkey* %USERPROFILE%\.android\
docker build -t SIPS_Container .