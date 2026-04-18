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

app.post('/api/upload', upload.single('file'), async (req, res) => {
  try {
    // ✅ Fix crash (VERY IMPORTANT)
    if (!req.file) {
      return res.status(400).json({ error: 'File is required' });
    }

    console.log('Uploaded file:', req.file.path);

    const formData = new FormData();
    formData.append('file', fs.createReadStream(req.file.path));

    // ✅ Use docker service name (NOT localhost)
    const response = await axios.post(
      `http://127.0.0.1:8000/upload?user_id=${USER_ID}`,
      formData,
      { headers: formData.getHeaders() }
    );

    res.json(response.data);

  } catch (err) {
    console.error('Upload error:', err.message);
    res.status(500).json({ error: 'Upload failed' });
  }
});

app.post('/api/ask', async (req, res) => {
  try {
    const response = await axios.post(
      `http://127.0.0.1:8000/ask`,
      null,
      {
        params: {
          user_id: USER_ID,
          q: req.body.question
        }
      }
    );

    res.json(response.data);

  } catch (err) {
    console.error('Ask error:', err.message);
    res.status(500).json({ error: 'Ask failed' });
  }
});

app.listen(5000, () => console.log('Node running on 5000'));