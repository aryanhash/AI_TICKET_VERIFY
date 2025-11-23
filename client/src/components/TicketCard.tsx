import React, { useState } from 'react';
import QRCode from 'react-qr-code';

interface TicketCardProps {
  ticket: {
    token_id: number;
    event_id: string;
    metadata_uri: string;
    qr_code_data: string;
    minted_at: string;
    event?: {
      title: string;
      venue: string;
      date: string;
    };
  };
}

export default function TicketCard({ ticket }: TicketCardProps) {
  const [showQR, setShowQR] = useState(false);

  return (
    <div className="bg-white rounded-lg shadow-lg overflow-hidden">
      <div className="bg-gradient-to-r from-qie-primary to-qie-secondary p-6 text-white">
        <h3 className="text-xl font-bold mb-2">
          {ticket.event?.title || 'Event Ticket'}
        </h3>
        <p className="text-sm opacity-90">Token ID: #{ticket.token_id}</p>
      </div>
      
      <div className="p-6">
        {ticket.event && (
          <div className="space-y-2 mb-4">
            <div className="flex items-center text-sm text-gray-700">
              <span className="mr-2">📍</span>
              <span>{ticket.event.venue}</span>
            </div>
            <div className="flex items-center text-sm text-gray-700">
              <span className="mr-2">📅</span>
              <span>{new Date(ticket.event.date).toLocaleDateString()}</span>
            </div>
          </div>
        )}

        <div className="mb-4">
          <p className="text-xs text-gray-500">
            Minted: {new Date(ticket.minted_at).toLocaleString()}
          </p>
        </div>

        <button
          onClick={() => setShowQR(!showQR)}
          className="w-full bg-qie-primary hover:bg-qie-secondary text-white py-2 rounded-md font-semibold transition-colors"
        >
          {showQR ? 'Hide QR Code' : 'Show QR Code'}
        </button>

        {showQR && (
          <div className="mt-4 p-4 bg-white border-2 border-gray-200 rounded-lg">
            <div className="flex justify-center">
              <QRCode value={ticket.qr_code_data} size={200} />
            </div>
            <p className="text-xs text-center text-gray-500 mt-2">
              Scan this QR code at the event entrance
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
