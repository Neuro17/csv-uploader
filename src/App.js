import React, { useState, useEffect } from 'react';
import { 
  Button, Container, Typography, LinearProgress, Table, TableRow, 
  TableContainer, Paper, TableBody, TableCell, TableHead 
} from '@mui/material';
import axios from 'axios';

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploadResult, setUploadResult] = useState(null);
  const [finalResult, setfinalResult] = useState(null);
  const [loaderValue, setLoaderValue] = useState(null);
  const [uploadComplete, setUploadComplete] = useState(false);
  const [loaderType, setLoaderType] = useState(null);

  const handleFileSelect = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleFileUpload = () => {
    if (selectedFile) {
      const formData = new FormData();
      formData.append('file', selectedFile);

      setLoaderValue(1)
      setUploadResult({})
      setLoaderType('indeterminate')
      axios.post('http://localhost:8888/upload', formData)
        .then((response) => {
          console.log(response.data);
          localStorage.setItem('uploadTask', JSON.stringify(response.data));
          setUploadResult(response.data);
          setUploadComplete(false);
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
      setLoaderType('buffer')
    }
    const intervalId = setInterval(() => {
      axios
        .get(`http://localhost:8888/status/${taskID}`)
        .then((response) => {
          const isCompleted = response.data['data'][3]
          const totalRows = response.data['data'][2]
          const processedRows = response.data['data'][4] + response.data['data'][5]
          const value = parseInt(processedRows / totalRows * 100)
          if(value > 1) {
            setLoaderValue(value)
          }
          console.log(response.data)
          if(isCompleted) {
            clearInterval(intervalId);
            localStorage.removeItem('uploadTask');
            setUploadResult(null)
            setUploadComplete(true)
            setfinalResult(response.data)
          } else {
            setUploadResult(response.data);
          }
          console.log(loaderValue, totalRows, processedRows)
        })
        .catch((error) => {
          console.error(error);
        });
    }, 1000); // Polling interval set to 1 second (adjust as needed)
  
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
      {uploadResult && <LinearProgress value={loaderValue} variant={loaderType} valueBuffer={loaderValue + 10}/> }
      { uploadComplete && 
        <>
          <p>Records created: {finalResult['data'][4]}</p>
          <p>Records updated: {finalResult['data'][5]}</p>
          <p>Found the following malformed rows:</p>
          <TableContainer component={Paper}>
            <Table>
              <TableHead>
                <TableCell>ID</TableCell>
                <TableCell>Nane</TableCell>
                <TableCell>Price</TableCell>
              </TableHead>
              <TableBody>
                {finalResult['data']['6'].split('|').map(r => <TableRow>{r.split(',').map(c => <TableCell>{c}</TableCell>)}</TableRow>)}
              </TableBody>
            </Table>
          </TableContainer>
        </>
      }
    </Container>
  );
}

export default App;
