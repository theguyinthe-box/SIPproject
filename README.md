Requirements for the HOST:
- nodejs
- npm
- gdown
- Docker Compose
    - v2 Docker-Compose will not work (because of the start script)


How to use:
 - Setup the Model
    1. Download the models
        - Run scripts/download_models.sh
    2. Inside model run `docker build -t sips .`
 - Setup the GUI
    - Inside the SIP-GUI repo run `npm install`

Running the Test:
 Note :: This repo assumes you are using an Android phone to get your input photos
         This also assumes that your device stores images in `sdcard/DCIM/Camera`
         if this isnt the case for you modify the path in `model/scripts/get_images.sh`
 
 To start the GUI into SIP-GUI and run `node main.js`