const express = require('express');
const axios = require('axios');
const multer = require('multer');
const cors = require('cors');
const fs = require('fs');
const FormData = require('form-data');

const app = express();
app.use(cors());
app.use(express.json());

const upload = multer({ dest: 'uploads/' });
const USER_ID = "user1";

app.post('/upload', upload.single('file'), async (req, res) => {
  const formData = new FormData();
  formData.append('file', fs.createReadStream(req.file.path));

  const response = await axios.post(
    `http://localhost:8000/upload?user_id=${USER_ID}`,
    formData,
    { headers: formData.getHeaders() }
  );

  res.json(response.data);
});

app.post('/ask', async (req, res) => {
  const response = await axios.post(
    `http://localhost:8000/ask`,
    null,
    {
      params: {
        user_id: USER_ID,
        q: req.body.question
      }
    }
  );

  res.json(response.data);
});

app.listen(5000, () => console.log('Node running on 5000'));
