import React, { useState } from 'react';
import dynamic from 'next/dynamic';
import { verifyTicket } from '@/lib/api';

const QRScanner = dynamic(() => import('@/components/QRScanner'), { ssr: false });

export default function Verify() {
  const [qrData, setQrData] = useState<string>('');
  const [selfie, setSelfie] = useState<File | null>(null);
  const [verifying, setVerifying] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [scanMode, setScanMode] = useState(true);

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

  const handleVerify = async () => {
    if (!qrData || !selfie) {
      alert('Please scan QR code and upload a selfie');
      return;
    }

    setVerifying(true);
    setResult(null);

    try {
      const formData = new FormData();
      formData.append('qr_data', qrData);
      formData.append('selfie', selfie);

      const verificationResult = await verifyTicket(formData);
      setResult(verificationResult);
    } catch (error: any) {
      console.error('Verification error:', error);
      setResult({
        verified: false,
        status: 'error',
        message: error.response?.data?.detail || 'Verification failed',
      });
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
              {scanMode ? (
                <div>
                  <QRScanner onScan={handleQRScan} />
                  <button
                    onClick={handleManualInput}
                    className="mt-4 text-qie-primary hover:underline"
                  >
                    Enter QR data manually
                  </button>
                </div>
              ) : (
                <div>
                  <textarea
                    value={qrData}
                    onChange={(e) => setQrData(e.target.value)}
                    placeholder="Paste QR code data here"
                    className="w-full border border-gray-300 rounded-md p-3 min-h-[100px]"
                  />
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
                </div>
              )}
            </div>

            <div>
              <h2 className="text-xl font-semibold mb-4">Step 2: Upload Selfie</h2>
              <input
                type="file"
                accept="image/*"
                capture="user"
                onChange={handleSelfieSelect}
                className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-qie-primary file:text-white hover:file:bg-qie-secondary"
              />
              {selfie && (
                <div className="mt-4">
                  <img
                    src={URL.createObjectURL(selfie)}
                    alt="Selfie preview"
                    className="w-48 h-48 object-cover rounded-lg border-2 border-gray-300"
                  />
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
                <p className="text-lg">{result.message || 'Verification complete'}</p>
                {result.confidence && (
                  <p className="text-sm mt-2 opacity-75">
                    Confidence: {result.confidence}
                  </p>
                )}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
