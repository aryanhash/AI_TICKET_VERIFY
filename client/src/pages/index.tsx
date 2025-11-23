import React from 'react';
import Link from 'next/link';

export default function Home() {
  return (
    <div className="min-h-screen">
      <div className="bg-gradient-to-r from-qie-primary to-qie-secondary text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
          <div className="text-center">
            <h1 className="text-5xl font-bold mb-6">
              AI-Verified NFT Ticketing System
            </h1>
            <p className="text-xl mb-8 opacity-90">
              Secure, transparent, and fraud-proof event tickets on QIE Blockchain
            </p>
            <div className="flex justify-center space-x-4">
              <Link
                href="/events"
                className="bg-white text-qie-primary hover:bg-gray-100 px-8 py-3 rounded-lg font-semibold text-lg transition-colors"
              >
                Browse Events
              </Link>
              <Link
                href="/verify"
                className="bg-qie-dark hover:bg-opacity-80 px-8 py-3 rounded-lg font-semibold text-lg transition-colors"
              >
                Verify Ticket
              </Link>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <h2 className="text-3xl font-bold text-center mb-12 text-gray-900">
          How It Works
        </h2>
        
        <div className="grid md:grid-cols-3 gap-8">
          <div className="bg-white p-8 rounded-lg shadow-lg text-center">
            <div className="text-5xl mb-4">🔗</div>
            <h3 className="text-xl font-bold mb-3 text-gray-900">Connect Wallet</h3>
            <p className="text-gray-600">
              Connect your MetaMask wallet to the QIE Blockchain network and authenticate securely.
            </p>
          </div>

          <div className="bg-white p-8 rounded-lg shadow-lg text-center">
            <div className="text-5xl mb-4">🎫</div>
            <h3 className="text-xl font-bold mb-3 text-gray-900">Buy NFT Tickets</h3>
            <p className="text-gray-600">
              Purchase event tickets as NFTs. Each ticket is unique and stored on the blockchain.
            </p>
          </div>

          <div className="bg-white p-8 rounded-lg shadow-lg text-center">
            <div className="text-5xl mb-4">🤖</div>
            <h3 className="text-xl font-bold mb-3 text-gray-900">AI Verification</h3>
            <p className="text-gray-600">
              At the event, scan your QR code and take a selfie. AI verifies it matches your ticket.
            </p>
          </div>
        </div>

        <div className="mt-16 bg-gradient-to-r from-qie-primary/10 to-qie-secondary/10 p-8 rounded-lg">
          <h3 className="text-2xl font-bold mb-4 text-gray-900">Why NFT Tickets?</h3>
          <ul className="space-y-3 text-gray-700">
            <li className="flex items-start">
              <span className="mr-2">✅</span>
              <span><strong>Fraud Prevention:</strong> AI-powered selfie verification prevents ticket scalping and fraud</span>
            </li>
            <li className="flex items-start">
              <span className="mr-2">✅</span>
              <span><strong>Blockchain Security:</strong> Immutable ownership records on QIE Blockchain</span>
            </li>
            <li className="flex items-start">
              <span className="mr-2">✅</span>
              <span><strong>Ultra-Low Fees:</strong> QIE's low gas costs make NFT tickets affordable</span>
            </li>
            <li className="flex items-start">
              <span className="mr-2">✅</span>
              <span><strong>Instant Verification:</strong> Real-time AI comparison at event entry</span>
            </li>
          </ul>
        </div>
      </div>
    </div>
  );
}
