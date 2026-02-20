const path = require('path');

const os = require('os')
const { spawn } = require('child_process');
const { exec } = require('child_process');

const express = require('express');
const app = express();
const port = 3000;

//let subjectID = null;

const publicDir = path.resolve(__dirname, 'public');

app.use(express.static(publicDir));
app.use(express.json());

app.get('/', (req, res) => {
  res.sendFile(path.resolve(publicDir, 'dashboard.html'));
})

let server = app.listen(port, () => {
  console.log(`app listening on port ${port}`)
})

server.on('error', (e) => {
  if (e.code === 'EADDRINUSE') {
    console.error('PORT ' + port +  ' in use');
  }
});

app.get('/stop-container', (req, res, next) => {
  res.setHeader('Content-Type', 'text/event-stream');
  res.setHeader('Cache-Control', 'no-cache');
  res.setHeader('Connection', 'keep-alive');
  
  console.log("Running the stop script")
  const container = spawn('sh', ['../scripts/stop.sh'])

  container.stdout.on('data', (data) => {
    res.write(`data: ${data}\n\n`);
    process.stdout.write(`${data}`);
  });

  container.stderr.on('data', (data) => {
    res.write(`data: ${data}\n\n`)
    process.stdout.write(`${data}`);
  });

  container.on('close', (code) => {
    res.write(`Process exited with code ${code}\n\n`);
    process.stdout.write(`process exited with code ${code}`);
    res.end();
  });
});

app.get('/run-container', (req, res, next) => {
  res.setHeader('Content-Type', 'text/event-stream');
  res.setHeader('Cache-Control', 'no-cache');
  res.setHeader('Connection', 'keep-alive');

  console.log("Running the Start script")
  const model = spawn('sh', ['../scripts/start.sh', 'false'])

  model.stdout.on('data', (data) => {
    process.stdout.write(`model: ${data}`);
  });

  model.stderr.on('data', (data) => {
    process.stdout.write(`model: ${data}`);
  });

  model.on('close', (code) => {
    process.stdout.write(`model process exited with code ${code}`);
  });
});

app.get('/container-logs', (req, res) => {
  res.setHeader('Content-Type', 'text/event-stream');
  res.setHeader('Cache-Control', 'no-cache');
  res.setHeader('Connection', 'keep-alive');

  console.log("Running the Start script and streaming logs...");
  const container = spawn('sh', ['../scripts/start.sh', 'false']);

  container.stdout.on('data', (data) => {
    res.write(`data: ${data}\n\n`); // Send data to the browser
    process.stdout.write(`${data}`);
  });

  container.stderr.on('data', (data) => {
    res.write(`data: ${data}\n\n`);
    process.stdout.write(`${data}`);
  });

  container.on('close', (code) => {
    res.write(`data: Process exited with code ${code}\n\n`);
    process.stdout.write(`${code}`);
    res.end();
  });
});