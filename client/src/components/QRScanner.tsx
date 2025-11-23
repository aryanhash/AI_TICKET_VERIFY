import React, { useEffect, useState } from 'react';
import { Html5QrcodeScanner } from 'html5-qrcode';

interface QRScannerProps {
  onScan: (result: string) => void;
}

export default function QRScanner({ onScan }: QRScannerProps) {
  const [scanner, setScanner] = useState<Html5QrcodeScanner | null>(null);

  useEffect(() => {
    const qrScanner = new Html5QrcodeScanner(
      'qr-reader',
      { fps: 10, qrbox: { width: 250, height: 250 } },
      false
    );

    qrScanner.render(
      (decodedText) => {
        onScan(decodedText);
        qrScanner.clear();
      },
      (error) => {
        console.warn('QR scan error:', error);
      }
    );

    setScanner(qrScanner);

    return () => {
      qrScanner.clear();
    };
  }, [onScan]);

  return (
    <div>
      <div id="qr-reader" className="w-full"></div>
    </div>
  );
}
