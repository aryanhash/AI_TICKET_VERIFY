/**
 * Web3 Integration using QIE Blockchain SDK
 * This module uses QIE SDK for all blockchain operations
 */

import { BrowserProvider } from 'ethers';
import {
  createQIEWeb3,
  createQIESignature,
  QIEWeb3,
  QIESignature,
  QIE_CHAIN_ID,
  QIE_CHAIN_ID_HEX,
  QIE_NETWORK,
} from './qie-sdk';

// Re-export QIE constants for backward compatibility
export { QIE_CHAIN_ID, QIE_CHAIN_ID_HEX, QIE_NETWORK };

// Global QIE SDK instances
let qieWeb3Instance: QIEWeb3 | null = null;
let qieSignatureInstance: QIESignature | null = null;

/**
 * Connect wallet using QIE Blockchain SDK
 * @returns Provider and connected address
 */
export async function connectWallet(): Promise<{ provider: BrowserProvider; address: string } | null> {
  // Use QIE SDK to connect
  qieWeb3Instance = createQIEWeb3();
  const result = await qieWeb3Instance.connect();
  
  if (result) {
    // Initialize QIE signature verifier
    qieSignatureInstance = createQIESignature(result.provider);
  }
  
  return result;
}

/**
 * Switch to QIE network using QIE Blockchain SDK
 * @returns True if successful
 */
export async function switchToQIENetwork(): Promise<boolean> {
  if (!qieWeb3Instance) {
    qieWeb3Instance = createQIEWeb3();
  }
  return await qieWeb3Instance.switchToQIENetwork();
}

/**
 * Sign message using QIE Blockchain SDK
 * @param message Message to sign
 * @returns Signature hex string
 */
export async function signMessage(message: string): Promise<string | null> {
  if (typeof window === 'undefined' || !window.ethereum) {
    return null;
  }

  try {
    // Ensure QIE SDK is initialized
    if (!qieWeb3Instance) {
      const result = await connectWallet();
      if (!result) {
        return null;
      }
    }

    // Get provider from QIE SDK
    const provider = qieWeb3Instance?.getProvider();
    if (!provider) {
      return null;
    }

    // Use QIE SDK to sign message
    if (!qieSignatureInstance) {
      qieSignatureInstance = createQIESignature(provider);
    }

    return await qieSignatureInstance.signMessage(message);
  } catch (error) {
    console.error('Error signing message with QIE SDK:', error);
    return null;
  }
}

declare global {
  interface Window {
    ethereum?: any;
  }
}
