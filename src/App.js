import React, { useState, useEffect } from 'react';
import { Button, Container, Typography, LinearProgress } from '@mui/material';
import axios from 'axios';

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploadResult, setUploadResult] = useState(null);
  const [loaderValue, setLoaderValue] = useState(null);

  const handleFileSelect = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleFileUpload = () => {
    if (selectedFile) {
      const formData = new FormData();
      formData.append('file', selectedFile);

      setLoaderValue(1)
      axios.post('http://localhost:8888/upload', formData)
        .then((response) => {
          console.log(response.data);
          localStorage.setItem('uploadTask', JSON.stringify(response.data));
          setUploadResult(response.data);
          const cleanupPolling = startPolling();
          return () => {
            cleanupPolling(); // Cleanup the polling on component unmount
          };
        })
        .catch((error) => {
          console.error(error);
        });
    }
  };

  const startPolling = () => {
    const storedResult = localStorage.getItem('uploadTask');
    let taskID;
    if(storedResult) {
      taskID = JSON.parse(storedResult)['task_id'];
    }
    const intervalId = setInterval(() => {
      axios
        .get(`http://localhost:8888/status/${taskID}`)
        .then((response) => {
          const isCompleted = response.data['data'][3]
          const totalRows = response.data['data'][2]
          const processedRows = response.data['data'][4] + response.data['data'][5]
          setLoaderValue(parseInt(processedRows / totalRows * 100))
          console.log(response.data)
          if(isCompleted) {
            clearInterval(intervalId);
            localStorage.removeItem('uploadTask');
            setUploadResult(null)
          } else {
            setUploadResult(response.data);
          }
          console.log(loaderValue, totalRows, processedRows)
        })
        .catch((error) => {
          console.error(error);
        });
    }, 1000); // Polling interval set to 5 seconds (adjust as needed)
  
    return () => {
      clearInterval(intervalId); // Cleanup the interval on component unmount
    };
  };

  useEffect(() => {
    const storedResult = localStorage.getItem('uploadTask');
    if (storedResult) {
      setUploadResult(JSON.parse(storedResult));
      const cleanupPolling = startPolling();
      return () => {
        cleanupPolling(); // Cleanup the polling on component unmount
      };
    }

  }, []);

  return (
    <Container maxWidth="sm">
      <Typography variant="h4" component="h1" align="center" gutterBottom>
        CSV Uploader
      </Typography>
      <input
        type="file"
        accept=".csv"
        onChange={handleFileSelect}
        style={{ marginBottom: '1rem' }}
      />
      <Button variant="contained" onClick={handleFileUpload} disabled={uploadResult !== null}>
        Upload
      </Button>
      {uploadResult && <LinearProgress value={loaderValue} variant='determinate'/> }
    </Container>
  );
}

export default App;
