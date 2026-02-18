//This is now just a basic REST API that handles
//the images and stuff from inside the docker container


const fs = require('fs');
const path = require('path');
const exifr = require('exifr');

const express = require('express');
const app = express();
const port = 3001;

let subjectID = null;

const sharedDir = path.resolve(__dirname, '..', 'shared');

app.use(express.static(publicDir));
//app.use(express.static(sharedDir));

console.log('Serving static files from:', publicDir);
app.use(express.json());

let server = app.listen(port, () => {
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
  setupDataFile(this.subjectID);
})

app.post('/userInput', (req, res) => {
  const { selection, filename, timeTaken} = req.body;
  writeSelection(this.subjectID, selection, path.resolve(__dirname, '..', 'shared', 'test', filename), timeTaken)
  deleteFileifExists(path.resolve(__dirname, '..', 'shared', 'test', filename));
  res.json({ success: true, received: { selection, filename } });
})

Array.prototype.random = function () { return this[Math.floor((Math.random() * this.length))]; }

function getImageFromTestData() {
  let files = fs.readdirSync(path.resolve(__dirname, '..', 'shared', 'test'));
  files = files.filter(f => !f.startsWith('.'));
  if (files.length === 0) return null;
  return path.resolve(__dirname, '..', 'shared', 'test', files.random());
}

async function setupDataFile(subjectID) {
  // If file doesn't exist, create it and add headers
  const filePath = path.resolve(__dirname + "/../results/", subjectID + ".csv");

  // I do this is way for readability and extendability
  let headers = "SubjectID";
  headers += "," + "Image Shown";
  headers += "," + "User Selection";
  headers += "," + "Time Taken";
  headers += "," + "Edit Direction";
  headers += "," + "Edit Factor";
  headers += "," + "Computed LPIPS";
  headers += "," + "Computed L2";
  headers += "," + "Computed MSSSIM";
  if (!fs.existsSync(filePath)) {
    console.log(`Creating new data file for subject ${subjectID} at ${filePath}`);
    fs.writeFileSync(filePath, headers + "\n");
  }
}

async function writeSelection(subjectID, userSelection, imageShownPath, timeTaken) {
  let content = subjectID;
  try {
    const file = fs.readFileSync(path.resolve(imageShownPath));
    const exif = await exifr.parse(file);
    
  // I do this is way for readability and extendability
    content += "," + path.basename(imageShownPath);
    content += "," + userSelection;
    content += "," + timeTaken + " ms";
    content += "," + exif["edit_direction"];
    content += "," + exif["edit_factor"];
    content += "," + exif["computed_lpips"];
    content += "," + exif["computed_l2"];
    content += "," + exif["computed_msssim"];
    fs.writeFileSync(path.resolve(__dirname + "/../results/", subjectID + ".csv"), content + "\n", { flag: 'a' });
    console.log("Writing : " + content)
  } catch (err) {
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