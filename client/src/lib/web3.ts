import { ethers, BrowserProvider } from 'ethers';

export const QIE_CHAIN_ID = 5656;
export const QIE_CHAIN_ID_HEX = '0x1618';

export const QIE_NETWORK = {
  chainId: QIE_CHAIN_ID_HEX,
  chainName: 'QIE Blockchain',
  nativeCurrency: {
    name: 'QIE',
    symbol: 'QIE',
    decimals: 18,
  },
  rpcUrls: ['https://rpc-mainnet.qie.digital'],
  blockExplorerUrls: ['https://mainnet.qie.digital'],
};

export async function connectWallet(): Promise<{ provider: BrowserProvider; address: string } | null> {
  if (typeof window === 'undefined' || !window.ethereum) {
    alert('Please install MetaMask!');
    return null;
  }

  try {
    const provider = new BrowserProvider(window.ethereum);
    
    const accounts = await provider.send('eth_requestAccounts', []);
    const address = accounts[0];

    await switchToQIENetwork();

    return { provider, address };
  } catch (error) {
    console.error('Error connecting wallet:', error);
    return null;
  }
}

export async function switchToQIENetwork(): Promise<boolean> {
  if (typeof window === 'undefined' || !window.ethereum) {
    return false;
  }

  try {
    await window.ethereum.request({
      method: 'wallet_switchEthereumChain',
      params: [{ chainId: QIE_CHAIN_ID_HEX }],
    });
    return true;
  } catch (switchError: any) {
    if (switchError.code === 4902) {
      try {
        await window.ethereum.request({
          method: 'wallet_addEthereumChain',
          params: [QIE_NETWORK],
        });
        return true;
      } catch (addError) {
        console.error('Error adding QIE network:', addError);
        return false;
      }
    }
    console.error('Error switching network:', switchError);
    return false;
  }
}

export async function signMessage(message: string): Promise<string | null> {
  if (typeof window === 'undefined' || !window.ethereum) {
    return null;
  }

  try {
    const provider = new BrowserProvider(window.ethereum);
    const signer = await provider.getSigner();
    const signature = await signer.signMessage(message);
    return signature;
  } catch (error) {
    console.error('Error signing message:', error);
    return null;
  }
}

declare global {
  interface Window {
    ethereum?: any;
  }
}
