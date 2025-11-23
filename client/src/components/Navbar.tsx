import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { connectWallet, signMessage } from '@/lib/web3';
import { walletLogin } from '@/lib/api';

export default function Navbar() {
  const [walletAddress, setWalletAddress] = useState<string | null>(null);
  const [isOrganizer, setIsOrganizer] = useState(false);

  useEffect(() => {
    const savedAddress = localStorage.getItem('walletAddress');
    const savedIsOrganizer = localStorage.getItem('isOrganizer') === 'true';
    if (savedAddress) {
      setWalletAddress(savedAddress);
      setIsOrganizer(savedIsOrganizer);
    }
  }, []);

  const handleConnect = async () => {
    try {
      console.log('Starting wallet connection...');
      const result = await connectWallet();
      if (!result) {
        console.error('Wallet connection failed');
        return;
      }

      const { address } = result;
      console.log('Wallet connected, address:', address);
      
      const message = `Sign this message to login to NFT Ticketing System.\nNonce: ${Date.now()}`;
      console.log('Requesting signature...');
      
      const signature = await signMessage(message);
      if (!signature) {
        alert('Failed to sign message. Please try again.');
        return;
      }

      console.log('Signature received, logging in...');
      const loginResult = await walletLogin(address, signature, message);
      
      setWalletAddress(address);
      setIsOrganizer(loginResult.is_organizer || false);
      
      localStorage.setItem('walletAddress', address);
      localStorage.setItem('isOrganizer', String(loginResult.is_organizer || false));
      
      alert(`Connected successfully! ${loginResult.is_organizer ? 'You are an organizer.' : ''}`);
    } catch (error: any) {
      console.error('Login failed:', error);
      const errorMessage = error.response?.data?.detail || error.message || 'Login failed';
      alert(`Login failed: ${errorMessage}`);
    }
  };

  const handleDisconnect = () => {
    setWalletAddress(null);
    setIsOrganizer(false);
    localStorage.removeItem('walletAddress');
    localStorage.removeItem('isOrganizer');
  };

  return (
    <nav className="bg-gradient-to-r from-qie-primary to-qie-secondary text-white shadow-lg">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Link href="/" className="text-2xl font-bold">
              🎫 QIE Tickets
            </Link>
            <div className="ml-10 flex space-x-4">
              <Link href="/events" className="hover:bg-white/20 px-3 py-2 rounded-md">
                Events
              </Link>
              {walletAddress && (
                <Link href="/dashboard" className="hover:bg-white/20 px-3 py-2 rounded-md">
                  My Tickets
                </Link>
              )}
              {walletAddress && (
                <Link href="/verify" className="hover:bg-white/20 px-3 py-2 rounded-md">
                  Verify
                </Link>
              )}
              {isOrganizer && (
                <Link href="/organizer/create" className="hover:bg-white/20 px-3 py-2 rounded-md">
                  Create Event
                </Link>
              )}
            </div>
          </div>
          <div className="flex items-center">
            {walletAddress ? (
              <div className="flex items-center space-x-2">
                <span className="bg-white/20 px-3 py-2 rounded-md text-sm">
                  {walletAddress.slice(0, 6)}...{walletAddress.slice(-4)}
                </span>
                <button
                  onClick={handleDisconnect}
                  className="bg-red-500 hover:bg-red-600 px-4 py-2 rounded-md"
                >
                  Disconnect
                </button>
              </div>
            ) : (
              <button
                onClick={handleConnect}
                className="bg-white text-qie-primary hover:bg-gray-100 px-4 py-2 rounded-md font-semibold"
              >
                Connect Wallet
              </button>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
}
