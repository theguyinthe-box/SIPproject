cd ../model

echo Killing adb
pkill adb
echo Starting Program...

#Stop the docker container first just in case 😉
#docker compose down
#Starting the Docker Container
docker compose up -d

docker exec sips bash /workspace/scripts/get_images.sh

docker exec sips bash /workspace/scripts/run_model.sh
docker exec sips bash /workspace/scripts/start_gui.sh
