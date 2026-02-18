// const { app, BrowserWindow } = require('electron')
const fs = require('fs');
const path = require('path');
const exifr = require('exifr');

const express = require('express');
const app = express();
const port = 3000;

let subjectID = null;

//Needs:
//User input for subject ID
//Randomly select an image from test dataset
//Display image to user
//Allow user to make selection from predefined set of options
//File name is SubjectID.csv
//Record subject ID, image shown, and user selection to a local file

const publicDir = path.resolve(__dirname, 'public');
const sharedDir = path.resolve(__dirname, '..', 'shared');

app.use(express.static(publicDir));
//app.use(express.static(sharedDir));

console.log('Serving static files from:', publicDir);
app.use(express.json());

app.get('/', (req, res) => {
  res.sendFile(path.resolve(publicDir, 'id_input.html'));
})

let server = app.listen(port, () => {
  console.log(`app listening on port ${port}`)
})