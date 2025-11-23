import { useState } from 'react';
import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export default function Validator() {
  const [validating, setValidating] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [txHash, setTxHash] = useState('');
  const [walletAddress, setWalletAddress] = useState('');
  const [tokenId, setTokenId] = useState('');

  const validateNetwork = async () => {
    setValidating(true);
    setResult(null);
    try {
      const response = await axios.get(`${API_URL}/validator/network`);
      setResult(response.data);
    } catch (error: any) {
      setResult({
        valid: false,
        errors: [error.response?.data?.detail || error.message || 'Validation failed']
      });
    } finally {
      setValidating(false);
    }
  };

  const validateContract = async () => {
    setValidating(true);
    setResult(null);
    try {
      const response = await axios.get(`${API_URL}/validator/contract`);
      setResult(response.data);
    } catch (error: any) {
      setResult({
        valid: false,
        errors: [error.response?.data?.detail || error.message || 'Validation failed']
      });
    } finally {
      setValidating(false);
    }
  };

  const validateTransaction = async () => {
    if (!txHash.trim()) {
      alert('Please enter a transaction hash');
      return;
    }
    setValidating(true);
    setResult(null);
    try {
      const response = await axios.get(`${API_URL}/validator/transaction/${txHash}`);
      setResult(response.data);
    } catch (error: any) {
      setResult({
        valid: false,
        errors: [error.response?.data?.detail || error.message || 'Validation failed']
      });
    } finally {
      setValidating(false);
    }
  };

  const validateWallet = async () => {
    if (!walletAddress.trim()) {
      alert('Please enter a wallet address');
      return;
    }
    setValidating(true);
    setResult(null);
    try {
      const response = await axios.get(`${API_URL}/validator/wallet/${walletAddress}`);
      setResult(response.data);
    } catch (error: any) {
      setResult({
        valid: false,
        errors: [error.response?.data?.detail || error.message || 'Validation failed']
      });
    } finally {
      setValidating(false);
    }
  };

  const validateToken = async () => {
    if (!tokenId.trim()) {
      alert('Please enter a token ID');
      return;
    }
    setValidating(true);
    setResult(null);
    try {
      const response = await axios.get(`${API_URL}/validator/token/${tokenId}`);
      setResult(response.data);
    } catch (error: any) {
      setResult({
        valid: false,
        errors: [error.response?.data?.detail || error.message || 'Validation failed']
      });
    } finally {
      setValidating(false);
    }
  };

  const comprehensiveValidation = async () => {
    setValidating(true);
    setResult(null);
    try {
      const response = await axios.get(`${API_URL}/validator/comprehensive`);
      setResult(response.data);
    } catch (error: any) {
      setResult({
        overall_valid: false,
        errors: [error.response?.data?.detail || error.message || 'Validation failed']
      });
    } finally {
      setValidating(false);
    }
  };

  const formatResult = (data: any) => {
    if (!data) return null;
    
    return (
      <div className="mt-6 p-6 bg-white rounded-lg shadow-lg">
        <h3 className="text-xl font-bold mb-4 text-gray-800">Validation Result</h3>
        <div className={`p-4 rounded-lg mb-4 ${data.valid || data.overall_valid ? 'bg-green-50 border border-green-200' : 'bg-red-50 border border-red-200'}`}>
          <div className="flex items-center gap-2 mb-2">
            <span className={`text-2xl ${data.valid || data.overall_valid ? 'text-green-600' : 'text-red-600'}`}>
              {data.valid || data.overall_valid ? '✅' : '❌'}
            </span>
            <span className={`font-semibold ${data.valid || data.overall_valid ? 'text-green-800' : 'text-red-800'}`}>
              {data.valid || data.overall_valid ? 'Valid' : 'Invalid'}
            </span>
          </div>
        </div>
        <pre className="bg-gray-50 p-4 rounded-lg overflow-auto text-sm">
          {JSON.stringify(data, null, 2)}
        </pre>
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 py-12 px-4">
      <div className="max-w-4xl mx-auto">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">QIE Validator</h1>
          <p className="text-gray-600">Validate QIE blockchain network, contracts, transactions, and more</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8">
          <button
            onClick={validateNetwork}
            disabled={validating}
            className="bg-qie-primary hover:bg-qie-secondary text-white py-4 px-6 rounded-lg font-semibold transition-colors disabled:bg-gray-400"
          >
            Validate Network
          </button>

          <button
            onClick={validateContract}
            disabled={validating}
            className="bg-qie-primary hover:bg-qie-secondary text-white py-4 px-6 rounded-lg font-semibold transition-colors disabled:bg-gray-400"
          >
            Validate Contract
          </button>

          <button
            onClick={comprehensiveValidation}
            disabled={validating}
            className="bg-gradient-to-r from-qie-primary to-qie-secondary text-white py-4 px-6 rounded-lg font-semibold transition-colors disabled:bg-gray-400 md:col-span-2"
          >
            Comprehensive Validation
          </button>
        </div>

        <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
          <h2 className="text-2xl font-bold mb-4 text-gray-800">Specific Validations</h2>
          
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Transaction Hash
              </label>
              <div className="flex gap-2">
                <input
                  type="text"
                  value={txHash}
                  onChange={(e) => setTxHash(e.target.value)}
                  placeholder="0x..."
                  className="flex-1 border border-gray-300 rounded-md px-4 py-2 focus:ring-2 focus:ring-qie-primary focus:border-transparent"
                />
                <button
                  onClick={validateTransaction}
                  disabled={validating}
                  className="bg-qie-primary hover:bg-qie-secondary text-white px-6 py-2 rounded-md font-semibold transition-colors disabled:bg-gray-400"
                >
                  Validate
                </button>
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Wallet Address
              </label>
              <div className="flex gap-2">
                <input
                  type="text"
                  value={walletAddress}
                  onChange={(e) => setWalletAddress(e.target.value)}
                  placeholder="0x..."
                  className="flex-1 border border-gray-300 rounded-md px-4 py-2 focus:ring-2 focus:ring-qie-primary focus:border-transparent"
                />
                <button
                  onClick={validateWallet}
                  disabled={validating}
                  className="bg-qie-primary hover:bg-qie-secondary text-white px-6 py-2 rounded-md font-semibold transition-colors disabled:bg-gray-400"
                >
                  Validate
                </button>
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Token ID
              </label>
              <div className="flex gap-2">
                <input
                  type="number"
                  value={tokenId}
                  onChange={(e) => setTokenId(e.target.value)}
                  placeholder="0"
                  className="flex-1 border border-gray-300 rounded-md px-4 py-2 focus:ring-2 focus:ring-qie-primary focus:border-transparent"
                />
                <button
                  onClick={validateToken}
                  disabled={validating}
                  className="bg-qie-primary hover:bg-qie-secondary text-white px-6 py-2 rounded-md font-semibold transition-colors disabled:bg-gray-400"
                >
                  Validate
                </button>
              </div>
            </div>
          </div>
        </div>

        {validating && (
          <div className="text-center py-8">
            <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-qie-primary"></div>
            <p className="mt-4 text-gray-600">Validating...</p>
          </div>
        )}

        {result && formatResult(result)}
      </div>
    </div>
  );
}

