import React, { useRef, useState, useEffect } from "react";
import './App.css';

function App() {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState("");
  const [isCapturing, setIsCapturing] = useState(false);
  const [showResult, setShowResult] = useState(false);
  

  useEffect(() => {
    navigator.mediaDevices
      .getUserMedia({ video: { facingMode: "environment" } })
      .then((stream) => {
        let video = videoRef.current;
        video.srcObject = stream;
        video.play();
      })
      .catch((err) => {
        console.error("An error occurred: " + err);
      });
  }, []);

  const captureImage = async () => {
    // If a capture is already in progress, exit the function
    if (isCapturing) {
      return;
    }

    // Set the flag to indicate a capture is in progress
    setIsCapturing(true);

    setIsLoading(true);
    const context = canvasRef.current.getContext("2d");
    context.drawImage(videoRef.current, 0, 0, 640, 480);

    canvasRef.current.toBlob(async (blob) => {
      const formData = new FormData();
      formData.append("file", blob, "image.jpg");

      try {
        const response = await fetch("https://eat-or-not-container-3metrifzyq-lz.a.run.app/analyze/", {
          method: "POST",
          body: formData,
        });
        if (response.ok) {
          const data = await response.json();
          setResult(data.analysis || "No analysis available.");
        } else {
          setResult("An error occurred while analyzing.");
        }
      } catch (error) {
        console.error('Fetch error:', error);
        setResult("An error occurred while analyzing.");
      }
      finally {
        setIsLoading(false);
        setIsCapturing(false);
        setShowResult(true)
      }
    });
  };

  return (
    <div>
      <h1>Gluten Analyzer</h1>
      <p>Take a photo of the product label</p>
      <button onClick={captureImage} disabled={isCapturing}>Capture</button>
      <video id="video" width="640" height="480" ref={videoRef}></video>
      <canvas id="canvas" width="640" height="480" ref={canvasRef} style={{ display: "none" }}></canvas>
      {isLoading && (
        <div className="overlay">
          <p className="result-background">Analysing...</p>
        </div>
      )}
      {showResult && (
        <div className="overlay">
          <p className="result-background">{result}</p>
          <button onClick={() => setShowResult(false)}>Continue Scanning</button>
        </div>
      )}
    </div>
  );
}

export default App;
