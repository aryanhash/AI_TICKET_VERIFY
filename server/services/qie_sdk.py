"""
QIE Blockchain SDK Wrapper
This module provides QIE Blockchain SDK functionality for:
- Wallet signature verification
- Reading NFT ownership
- Minting NFT tickets
"""

from web3 import Web3
from eth_account.messages import encode_defunct
import json
import os
from dotenv import load_dotenv
from typing import Optional, Dict, List

# Load environment variables
load_dotenv()

try:
    from web3.middleware import geth_poa_middleware
except ImportError:
    geth_poa_middleware = None


class QIEWeb3:
    """
    QIE Blockchain SDK - Web3 Provider
    Initializes connection to QIE network and provides blockchain operations
    """
    
    def __init__(self, rpc_url: Optional[str] = None):
        """
        Initialize QIE Web3 provider
        
        Args:
            rpc_url: QIE RPC endpoint (defaults to testnet)
        """
        self.rpc_url = rpc_url or os.getenv("QIE_RPC_URL", "https://rpc1testnet.qie.digital")
        self.chain_id = int(os.getenv("QIE_CHAIN_ID", "1983"))
        self.w3 = Web3(Web3.HTTPProvider(self.rpc_url))
        
        # Inject POA middleware for QIE network compatibility
        if geth_poa_middleware:
            self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    
    def is_connected(self) -> bool:
        """Check if connected to QIE network"""
        return self.w3.is_connected()
    
    def get_chain_id(self) -> int:
        """Get QIE chain ID"""
        return self.chain_id


class QIEContract:
    """
    QIE Blockchain SDK - Contract Interface
    Loads and interacts with deployed NFT contracts (from QIEDEX Token Creator)
    """
    
    def __init__(self, qie_web3: QIEWeb3, contract_address: str, abi: List[Dict]):
        """
        Initialize QIE contract interface
        
        Args:
            qie_web3: QIEWeb3 instance
            contract_address: Contract address from QIEDEX Token Creator
            abi: Contract ABI from QIEDEX Token Creator
        """
        self.qie_web3 = qie_web3
        self.contract_address = Web3.to_checksum_address(contract_address)
        self.abi = abi
        self.contract = qie_web3.w3.eth.contract(
            address=self.contract_address,
            abi=self.abi
        )
    
    def mint(self, to_address: str, metadata_uri: str, private_key: str) -> Dict:
        """
        Mint NFT ticket using QIE SDK
        
        Args:
            to_address: Recipient wallet address
            metadata_uri: IPFS URI for ticket metadata
            private_key: Organizer's private key for signing
            
        Returns:
            Transaction result with tx_hash and token_id
        """
        try:
            account = self.qie_web3.w3.eth.account.from_key(private_key)
            to_checksum = Web3.to_checksum_address(to_address)
            
            nonce = self.qie_web3.w3.eth.get_transaction_count(account.address)
            
            transaction = self.contract.functions.mint(
                to_checksum,
                metadata_uri
            ).build_transaction({
                'chainId': self.qie_web3.chain_id,
                'gas': 300000,
                'gasPrice': self.qie_web3.w3.eth.gas_price,
                'nonce': nonce,
            })
            
            signed_txn = self.qie_web3.w3.eth.account.sign_transaction(transaction, private_key)
            # Handle web3.py v7 compatibility (uses raw_transaction instead of rawTransaction)
            # Try raw_transaction first (v7), then rawTransaction (v6)
            if hasattr(signed_txn, 'raw_transaction'):
                raw_tx = signed_txn.raw_transaction
            elif hasattr(signed_txn, 'rawTransaction'):
                raw_tx = signed_txn.rawTransaction
            else:
                # Fallback: try accessing as bytes
                raw_tx = bytes(signed_txn)
            tx_hash = self.qie_web3.w3.eth.send_raw_transaction(raw_tx)
            
            tx_receipt = self.qie_web3.w3.eth.wait_for_transaction_receipt(tx_hash)
            
            total_supply = self.contract.functions.totalSupply().call()
            token_id = total_supply - 1
            
            return {
                "success": True,
                "tx_hash": tx_hash.hex(),
                "token_id": token_id,
                "transaction_receipt": dict(tx_receipt)
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_token_uri(self, token_id: int) -> str:
        """Get token URI for a specific token ID"""
        try:
            return self.contract.functions.tokenURI(token_id).call()
        except Exception as e:
            print(f"Error fetching token URI: {e}")
            return ""
    
    def owner_of(self, token_id: int) -> str:
        """Get owner address of a token"""
        try:
            return self.contract.functions.ownerOf(token_id).call()
        except Exception as e:
            print(f"Error fetching owner: {e}")
            return ""
    
    def balance_of(self, owner_address: str) -> int:
        """Get balance of tokens for an address"""
        try:
            checksum_address = Web3.to_checksum_address(owner_address)
            return self.contract.functions.balanceOf(checksum_address).call()
        except Exception as e:
            print(f"Error fetching balance: {e}")
            return 0
    
    def total_supply(self) -> int:
        """Get total supply of tokens"""
        try:
            return self.contract.functions.totalSupply().call()
        except Exception as e:
            print(f"Error fetching total supply: {e}")
            return 0


class QIESignature:
    """
    QIE Blockchain SDK - Signature Verification
    Verifies wallet signatures for authentication
    """
    
    def __init__(self, qie_web3: QIEWeb3):
        """
        Initialize QIE signature verifier
        
        Args:
            qie_web3: QIEWeb3 instance
        """
        self.qie_web3 = qie_web3
    
    def verify(self, message: str, signature: str, wallet_address: str) -> bool:
        """
        Verify wallet signature using QIE SDK
        
        Args:
            message: Original message that was signed
            signature: Signature hex string
            wallet_address: Expected wallet address
            
        Returns:
            True if signature is valid, False otherwise
        """
        try:
            message_hash = encode_defunct(text=message)
            recovered_address = self.qie_web3.w3.eth.account.recover_message(
                message_hash, 
                signature=signature
            )
            return recovered_address.lower() == wallet_address.lower()
        except Exception as e:
            print(f"Signature verification error: {e}")
            return False


class QIENFT:
    """
    QIE Blockchain SDK - NFT Operations
    High-level NFT operations for reading ownership and managing tickets
    """
    
    def __init__(self, qie_contract: QIEContract):
        """
        Initialize QIE NFT operations
        
        Args:
            qie_contract: QIEContract instance
        """
        self.contract = qie_contract
    
    def get_tickets_of_owner(self, wallet_address: str) -> List[Dict]:
        """
        Get all tickets owned by a wallet address using QIE SDK
        
        Args:
            wallet_address: Wallet address to query
            
        Returns:
            List of tickets with token_id and token_uri
        """
        try:
            checksum_address = Web3.to_checksum_address(wallet_address)
            balance = self.contract.balance_of(checksum_address)
            
            if balance == 0:
                return []
            
            tickets = []
            total_supply = self.contract.total_supply()
            
            for token_id in range(total_supply):
                try:
                    owner = self.contract.owner_of(token_id)
                    if owner.lower() == checksum_address.lower():
                        token_uri = self.contract.get_token_uri(token_id)
                        tickets.append({
                            "token_id": token_id,
                            "token_uri": token_uri
                        })
                except:
                    continue
            
            return tickets
        except Exception as e:
            print(f"Error fetching tickets: {e}")
            return []


# QIE SDK Factory Functions
def create_qie_web3(rpc_url: Optional[str] = None) -> QIEWeb3:
    """
    Create QIE Web3 provider instance
    
    Args:
        rpc_url: Optional custom RPC URL
        
    Returns:
        QIEWeb3 instance
    """
    return QIEWeb3(rpc_url)


def load_qie_contract(contract_address: str, abi: List[Dict], rpc_url: Optional[str] = None) -> QIEContract:
    """
    Load QIE contract from QIEDEX Token Creator
    
    Args:
        contract_address: Contract address from QIEDEX Token Creator
        abi: Contract ABI from QIEDEX Token Creator
        rpc_url: Optional custom RPC URL
        
    Returns:
        QIEContract instance
    """
    qie_web3 = create_qie_web3(rpc_url)
    return QIEContract(qie_web3, contract_address, abi)


def create_qie_signature_verifier(rpc_url: Optional[str] = None) -> QIESignature:
    """
    Create QIE signature verifier
    
    Args:
        rpc_url: Optional custom RPC URL
        
    Returns:
        QIESignature instance
    """
    qie_web3 = create_qie_web3(rpc_url)
    return QIESignature(qie_web3)

