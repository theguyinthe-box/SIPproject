const path = require('path');

const os = require('os')
const { exec } = require('child_process');

const express = require('express');
const app = express();
const port = 3000;

//let subjectID = null;

const publicDir = path.resolve(__dirname, 'public');

app.use(express.static(publicDir));
app.use(express.json());

app.get('/', (req, res) => {
  res.sendFile(path.resolve(publicDir, 'id_input.html'));
})


let server = app.listen(port, () => {
  console.log(`app listening on port ${port}`)
})

server.on('error', (e) => {
  if (e.code === 'EADDRINUSE') {
    console.error('Address in use, retrying...');
  }
});

app.get('/stopContainer', (req, res, next) => {

});

app.get('/runModel', (req, res, next) => {
  exec('sh ../scripts/start.sh', (error, stdout, stderr) => {
    if (error) {
      console.error(`exec error: ${error}`);
      return;
    }
    console.log(`stdout: ${stdout}`);
    console.error(`stderr: ${stderr}`);
  });
});