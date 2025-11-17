// const { app, BrowserWindow } = require('electron')
const fs = require('fs');
const path = require('path');

const express = require('express');
const app = express();
const port = 3000;

//Needs:
//User input for subject ID
//Randomly select an image from test dataset
//Display image to user
//Allow user to make selection from predefined set of options
//File name is SubjectID.csv
//Record subject ID, image shown, and user selection to a local file

app.use(express.static('public'));
app.use(express.static('../shared'));
app.get('/', (req, res) => {
  res.sendFile(__dirname + '/index.html');
})

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`)
})

Array.prototype.random = function () {return this[Math.floor((Math.random()*this.length))];}

function getImageFromTestData(){
  fs.readdir(__dirname + '../shared/test', (err, files) => {
    if (err) {
      console.error('Could not list the directory.', err);
    }
    return files.random();
  });
  //We ran out of files so for now just return a static file
  return 'test-image/0.png';
}

function writeSelection(userID, userSelection, imageShown){
  let content = userID + "," + imageShown + "," + userSelection + "\n";
  fs.writeFile(__dirname + "../shared/results/" + userID + ".csv", content, { flag: 'a+' }, err => {
    if (err) {
      console.error(err);
    } else { // file written successfully
    }
  });
}