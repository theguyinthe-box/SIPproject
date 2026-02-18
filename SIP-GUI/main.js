const path = require('path');

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

app.get('/closeApp', (req, res) => {
  console.log("Closing App as per user request.");
  server.close();
  res.json({ success: true });
  process.exit(0);
})