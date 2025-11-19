// const { app, BrowserWindow } = require('electron')
const fs = require('fs');
const path = require('path');

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

app.use(express.static('public'));
app.use(express.static(path.resolve(__dirname + "/../shared")));
app.use(express.json());

app.get('/', (req, res) => {
  res.sendFile(__dirname + '/public/id_input.html');
})

app.listen(port, () => {
  console.log(`app listening on port ${port}`)
})

app.get('/randomImage', (req, res) => {
  let file = getImageFromTestData()
  if (!file) {
    res.status(404).send('<h1>No images found</h1>');
    return;
  }

  res.set('X-Image-Filename', path.basename(file));
  res.sendFile(file);
})

app.post('/subjectID', (req, res) => {
  const { subjectID } = req.body;
  this.subjectID = subjectID;
  console.log('Received User ID:', this.subjectID);
  res.json({ success: true, received: subjectID });
})

app.post('/userInput', (req, res) => {
  const { selection, filename } = req.body;
  writeSelection(this.subjectID, selection, filename)
  deleteFileifExists(path.resolve(__dirname, '..', 'shared', 'test', filename));
  res.json({ success: true, received: { selection, filename } });
})

Array.prototype.random = function () { return this[Math.floor((Math.random() * this.length))]; }

function getImageFromTestData() {
  const files = fs.readdirSync(path.resolve(__dirname, '..', 'shared', 'test'));
  if(files.length === 0) return null;
  return path.resolve(__dirname, '..', 'shared', 'test', files.random());
}

async function writeSelection(subjectID, userSelection, imageShown) {
  let content = subjectID + "," + imageShown + "," + userSelection + "\n";
  console.log(path.resolve(__dirname, '..', 'shared', 'test'))
  console.log(path.resolve(__dirname + "/../shared/results/", subjectID + ".csv"))
  try{
    fs.writeFileSync(path.resolve(__dirname + "/../shared/results/", subjectID + ".csv"), content, { flag: 'a' });
    console.log("Writing : " + content)
  } catch(err){
    console.log(err);
  }
}

async function deleteFileifExists(filePath) {
  try {
    if (fs.existsSync(filePath)) {
      fs.unlinkSync(filePath);
      console.log(`Deleted file: ${filePath}`);
    } else {
      console.log(`File not found, nothing to delete: ${filePath}`);
    }
  } catch (err) {
    console.error(`Error deleting file: ${filePath}`, err);
  }
}