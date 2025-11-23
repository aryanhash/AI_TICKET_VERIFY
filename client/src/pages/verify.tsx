import React, { useState } from 'react';
import dynamic from 'next/dynamic';
import { verifyTicket } from '@/lib/api';

const QRScanner = dynamic(() => import('@/components/QRScanner'), { ssr: false });
const CameraCapture = dynamic(() => import('@/components/CameraCapture'), { ssr: false });

export default function Verify() {
  const [qrData, setQrData] = useState<string>('');
  const [selfie, setSelfie] = useState<File | null>(null);
  const [verifying, setVerifying] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [scanMode, setScanMode] = useState(true);
  const [cameraMode, setCameraMode] = useState(true);

  const handleQRScan = (data: string) => {
    setQrData(data);
    setScanMode(false);
  };

  const handleManualInput = () => {
    setScanMode(false);
  };

  const handleSelfieSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setSelfie(e.target.files[0]);
    }
  };

  const handleCameraCapture = (file: File) => {
    setSelfie(file);
    setCameraMode(false);
  };

  const handleCameraError = (error: string) => {
    console.error('Camera error:', error);
    alert(`Camera error: ${error}. You can use file upload instead.`);
  };

  const handleVerify = async () => {
    if (!qrData || !selfie) {
      alert('Please scan QR code and upload a selfie');
      return;
    }

    // Validate QR data format
    try {
      const qrJson = JSON.parse(qrData);
      if (!qrJson.token_id || !qrJson.metadata_uri) {
        alert('Invalid QR code data. Please make sure you scanned the correct QR code from your ticket.');
        return;
      }
    } catch (e) {
      alert('Invalid QR code format. The QR code should contain JSON data. Please check your ticket QR code.');
      return;
    }

    setVerifying(true);
    setResult(null);

    try {
      const formData = new FormData();
      formData.append('qr_data', qrData);
      formData.append('selfie', selfie);

      console.log('Verifying ticket with QR data:', qrData.substring(0, 100) + '...');
      const verificationResult = await verifyTicket(formData);
      console.log('Verification result:', verificationResult);
      setResult(verificationResult);
    } catch (error: any) {
      console.error('Verification error:', error);
      const errorMessage = error.response?.data?.detail || error.message || 'Verification failed';
      setResult({
        verified: false,
        status: 'error',
        message: errorMessage,
      });
      alert(`Verification failed: ${errorMessage}`);
    } finally {
      setVerifying(false);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'verified':
        return 'text-green-600 bg-green-100';
      case 'suspicious':
        return 'text-yellow-600 bg-yellow-100';
      case 'denied':
      case 'error':
        return 'text-red-600 bg-red-100';
      default:
        return 'text-gray-600 bg-gray-100';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'verified':
        return '✅';
      case 'suspicious':
        return '⚠️';
      case 'denied':
      case 'error':
        return '❌';
      default:
        return '❓';
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <h1 className="text-4xl font-bold text-gray-900 mb-8">Verify Ticket</h1>

        <div className="bg-white rounded-lg shadow-lg p-8">
          <div className="space-y-6">
            <div>
              <h2 className="text-xl font-semibold mb-4">Step 1: Scan QR Code</h2>
              <p className="text-sm text-gray-600 mb-4">
                Go to your Dashboard → My Tickets → Click "Show QR Code" on your ticket, then scan it here.
              </p>
              {scanMode ? (
                <div>
                  <QRScanner onScan={handleQRScan} />
                  <button
                    onClick={handleManualInput}
                    className="mt-4 text-qie-primary hover:underline"
                  >
                    Enter QR data manually instead
                  </button>
                </div>
              ) : (
                <div>
                  <textarea
                    value={qrData}
                    onChange={(e) => setQrData(e.target.value)}
                    placeholder='Paste QR code data here (should be JSON like: {"token_id": 1, "event_id": "...", "metadata_uri": "ipfs://..."})'
                    className="w-full border border-gray-300 rounded-md p-3 min-h-[100px] text-gray-900 bg-white"
                  />
                  <p className="text-xs text-gray-500 mt-2">
                    💡 Tip: Copy the QR code data from your ticket in the Dashboard
                  </p>
                  <button
                    onClick={() => setScanMode(true)}
                    className="mt-2 text-qie-primary hover:underline"
                  >
                    Scan QR code instead
                  </button>
                </div>
              )}
              {qrData && (
                <div className="mt-2 p-2 bg-green-50 border border-green-200 rounded">
                  <p className="text-sm text-green-700">✓ QR Code data captured</p>
                  {(() => {
                    try {
                      const qrJson = JSON.parse(qrData);
                      return (
                        <p className="text-xs text-green-600 mt-1">
                          Token ID: {qrJson.token_id}, Event ID: {qrJson.event_id?.substring(0, 8)}...
                        </p>
                      );
                    } catch {
                      return <p className="text-xs text-yellow-600 mt-1">⚠️ Invalid JSON format</p>;
                    }
                  })()}
                </div>
              )}
            </div>

            <div>
              <h2 className="text-xl font-semibold mb-4">Step 2: Capture Selfie</h2>
              <p className="text-sm text-gray-600 mb-4">
                Take a clear photo of the ticket holder using your camera. The AI will compare this with the photo used when purchasing the ticket.
              </p>
              
              {!selfie ? (
                <div>
                  {cameraMode ? (
                    <div>
                      <CameraCapture onCapture={handleCameraCapture} onError={handleCameraError} />
                      <button
                        onClick={() => setCameraMode(false)}
                        className="mt-4 text-qie-primary hover:underline text-sm"
                      >
                        Or upload from file instead
                      </button>
                    </div>
                  ) : (
                    <div>
                      <input
                        type="file"
                        accept="image/*"
                        capture="user"
                        onChange={handleSelfieSelect}
                        className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-qie-primary file:text-white hover:file:bg-qie-secondary"
                      />
                      <button
                        onClick={() => setCameraMode(true)}
                        className="mt-2 text-qie-primary hover:underline text-sm"
                      >
                        Or use camera capture instead
                      </button>
                    </div>
                  )}
                </div>
              ) : (
                <div className="mt-4">
                  <div className="relative inline-block">
                    <img
                      src={URL.createObjectURL(selfie)}
                      alt="Selfie preview"
                      className="w-64 h-64 object-cover rounded-lg border-2 border-gray-300"
                    />
                  </div>
                  <p className="text-xs text-gray-500 mt-2">
                    ✓ Selfie captured: {selfie.name} ({(selfie.size / 1024).toFixed(1)} KB)
                  </p>
                  <button
                    onClick={() => {
                      setSelfie(null);
                      setCameraMode(true);
                    }}
                    className="mt-2 text-qie-primary hover:underline text-sm"
                  >
                    Retake photo
                  </button>
                </div>
              )}
            </div>

            <button
              onClick={handleVerify}
              disabled={verifying || !qrData || !selfie}
              className="w-full bg-qie-primary hover:bg-qie-secondary disabled:bg-gray-400 text-white py-3 rounded-lg font-semibold text-lg transition-colors"
            >
              {verifying ? 'Verifying...' : 'Verify Ticket'}
            </button>
          </div>

          {result && (
            <div className={`mt-8 p-6 rounded-lg ${getStatusColor(result.status)}`}>
              <div className="text-center">
                <div className="text-6xl mb-4">{getStatusIcon(result.status)}</div>
                <h3 className="text-2xl font-bold mb-2 uppercase">{result.status}</h3>
                <p className="text-lg whitespace-pre-wrap">{result.message || 'Verification complete'}</p>
                {result.confidence && result.confidence !== 'unknown' && (
                  <p className="text-sm mt-2 opacity-75">
                    Confidence: {result.confidence}
                  </p>
                )}
                {result.status === 'error' && (
                  <div className="mt-4 p-4 bg-white bg-opacity-50 rounded-lg">
                    <p className="text-sm font-semibold mb-2">Troubleshooting:</p>
                    <ul className="text-xs text-left space-y-1">
                      {result.message?.includes('quota') && (
                        <>
                          <li>• Check your API usage at: <a href="https://aistudio.google.com/app/apikey" target="_blank" rel="noopener noreferrer" className="text-blue-600 underline">Google AI Studio</a></li>
                          <li>• Gemini free tier limits: Check your quota at <a href="https://aistudio.google.com/app/apikey" target="_blank" rel="noopener noreferrer" className="text-blue-600 underline">Google AI Studio</a></li>
                          <li>• Wait for quota reset (usually daily) or upgrade your plan</li>
                        </>
                      )}
                      {result.message?.includes('API key') && (
                        <li>• Check your GEMINI_API_KEY or OPENAI_API_KEY in server/.env file</li>
                      )}
                      {result.message?.includes('Gemini') && (
                        <li>• Get a new Gemini API key at: <a href="https://aistudio.google.com/app/apikey" target="_blank" rel="noopener noreferrer" className="text-blue-600 underline">Google AI Studio</a></li>
                      )}
                      {result.message?.includes('OpenAI') && (
                        <>
                          <li>• Add credits at: <a href="https://platform.openai.com/account/billing" target="_blank" rel="noopener noreferrer" className="text-blue-600 underline">OpenAI Billing</a></li>
                          <li>• Check usage at: <a href="https://platform.openai.com/usage" target="_blank" rel="noopener noreferrer" className="text-blue-600 underline">OpenAI Usage</a></li>
                        </>
                      )}
                    </ul>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
