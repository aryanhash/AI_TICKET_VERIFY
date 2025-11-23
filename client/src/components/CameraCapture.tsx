import React, { useEffect, useRef, useState } from 'react';

interface CameraCaptureProps {
  onCapture: (file: File) => void;
  onError?: (error: string) => void;
}

export default function CameraCapture({ onCapture, onError }: CameraCaptureProps) {
  const videoRef = useRef<HTMLVideoElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const streamRef = useRef<MediaStream | null>(null);
  const [isStreaming, setIsStreaming] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    startCamera();
    return () => {
      stopCamera();
    };
  }, []);

  const startCamera = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: {
          facingMode: 'user', // Front camera
          width: { ideal: 1280 },
          height: { ideal: 720 }
        }
      });

      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        streamRef.current = stream;
        setIsStreaming(true);
        setError(null);
      }
    } catch (err: any) {
      const errorMsg = err.message || 'Failed to access camera';
      setError(errorMsg);
      if (onError) {
        onError(errorMsg);
      }
      console.error('Camera error:', err);
    }
  };

  const stopCamera = () => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach(track => track.stop());
      streamRef.current = null;
      setIsStreaming(false);
    }
  };

  const capturePhoto = () => {
    if (!videoRef.current || !canvasRef.current || !isStreaming) {
      return;
    }

    const video = videoRef.current;
    const canvas = canvasRef.current;
    const context = canvas.getContext('2d');

    if (!context) {
      return;
    }

    // Set canvas dimensions to match video
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    // Draw video frame to canvas
    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    // Convert canvas to blob
    canvas.toBlob((blob) => {
      if (blob) {
        const file = new File([blob], `selfie-${Date.now()}.jpg`, {
          type: 'image/jpeg',
          lastModified: Date.now()
        });
        onCapture(file);
        stopCamera();
      }
    }, 'image/jpeg', 0.95);
  };

  const retakePhoto = () => {
    startCamera();
  };

  return (
    <div className="w-full">
      {error ? (
        <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
          <p className="text-red-700 text-sm mb-2">Camera Error: {error}</p>
          <button
            onClick={startCamera}
            className="text-red-600 hover:text-red-800 underline text-sm"
          >
            Try Again
          </button>
        </div>
      ) : (
        <div className="space-y-4">
          <div className="relative bg-black rounded-lg overflow-hidden">
            <video
              ref={videoRef}
              autoPlay
              playsInline
              muted
              className="w-full h-auto max-h-96 object-cover"
            />
            <canvas ref={canvasRef} className="hidden" />
            {!isStreaming && (
              <div className="absolute inset-0 flex items-center justify-center bg-gray-900 bg-opacity-75">
                <div className="text-white text-center">
                  <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-white mx-auto mb-4"></div>
                  <p>Starting camera...</p>
                </div>
              </div>
            )}
          </div>
          
          <div className="flex gap-4">
            {isStreaming && (
              <button
                onClick={capturePhoto}
                className="flex-1 bg-qie-primary hover:bg-qie-secondary text-white py-3 rounded-lg font-semibold transition-colors"
              >
                📸 Capture Photo
              </button>
            )}
          </div>
        </div>
      )}
    </div>
  );
}


