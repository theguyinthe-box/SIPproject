cd ../model

echo Killing adb
pkill adb
echo Starting Program...
#Starting the Docker Container
docker compose up -d
docker exec sips /workspace/scripts/get_images.sh
docker exec sips /workspace/scripts/run_model.sh
docker exec sips /workspace/script/start_gui.sh
