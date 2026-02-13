echo Killing adb
pkill adb
echo Starting Program...
#Starting the Docker Container
docker compose up -d
docker exec sips /scripts/get_images.sh
docker exec sips /scripts/run_model.sh

# Stop the Docker Container, it will also delete the shared folder because of the volume configuration in docker-compose.yml 
docker compose down