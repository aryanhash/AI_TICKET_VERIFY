"""
Blockchain Service using QIE Blockchain SDK
This service uses QIE SDK for all blockchain operations:
- Wallet signature verification (QIE SDK)
- Reading NFT ownership (QIE SDK)
- Minting NFT tickets (QIE SDK)
"""

import json
import os
from dotenv import load_dotenv
from typing import Optional

# Load environment variables from .env file
load_dotenv()

# Import QIE Blockchain SDK
from .qie_sdk import (
    create_qie_web3,
    load_qie_contract,
    create_qie_signature_verifier,
    QIENFT
)

QIE_RPC_URL = os.getenv("QIE_RPC_URL", "https://rpc1testnet.qie.digital")
CONTRACT_ADDRESS = os.getenv("QIE_CONTRACT_ADDRESS", "")
ORGANIZER_PRIVATE_KEY = os.getenv("ORGANIZER_PRIVATE_KEY", "")

# NFT ABI from QIEDEX Token Creator
# This ABI should match the contract deployed via QIEDEX Token Creator
NFT_ABI = [
    {
        "inputs": [
            {"internalType": "address", "name": "to", "type": "address"},
            {"internalType": "string", "name": "uri", "type": "string"}
        ],
        "name": "mint",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "uint256", "name": "tokenId", "type": "uint256"}],
        "name": "tokenURI",
        "outputs": [{"internalType": "string", "name": "", "type": "string"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "uint256", "name": "tokenId", "type": "uint256"}],
        "name": "ownerOf",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "address", "name": "owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "totalSupply",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    }
]


class BlockchainService:
    """
    Blockchain Service using QIE Blockchain SDK
    All blockchain operations use QIE SDK as required
    """
    
    def __init__(self):
        # Initialize QIE Web3 provider using QIE SDK
        self.qie_web3 = create_qie_web3(QIE_RPC_URL)
        
        # Initialize QIE signature verifier using QIE SDK
        self.signature_verifier = create_qie_signature_verifier(QIE_RPC_URL)
        
        # Load QIE contract from QIEDEX Token Creator using QIE SDK
        self.qie_contract = None
        self.qie_nft = None
        
        if CONTRACT_ADDRESS:
            try:
                self.qie_contract = load_qie_contract(
                    CONTRACT_ADDRESS,
                    NFT_ABI,
                    QIE_RPC_URL
                )
                self.qie_nft = QIENFT(self.qie_contract)
            except Exception as e:
                print(f"Error loading QIE contract: {e}")
                self.qie_contract = None
                self.qie_nft = None
    
    def verify_signature(self, message: str, signature: str, wallet_address: str) -> bool:
        """
        Verify wallet signature using QIE Blockchain SDK
        
        Args:
            message: Original message that was signed
            signature: Signature hex string
            wallet_address: Expected wallet address
            
        Returns:
            True if signature is valid
        """
        return self.signature_verifier.verify(message, signature, wallet_address)
    
    async def mint_ticket(self, wallet_address: str, metadata_uri: str) -> dict:
        """
        Mint NFT ticket using QIE Blockchain SDK
        
        Args:
            wallet_address: Recipient wallet address
            metadata_uri: IPFS URI for ticket metadata
            
        Returns:
            Transaction result with tx_hash and token_id
        """
        if not self.qie_contract or not ORGANIZER_PRIVATE_KEY:
            raise Exception("QIE contract not initialized or private key not set. Please deploy contract using QIEDEX Token Creator.")
        
        # Use QIE SDK to mint ticket
        result = self.qie_contract.mint(
            wallet_address,
            metadata_uri,
            ORGANIZER_PRIVATE_KEY
        )
        
        return result
    
    async def get_tickets_of_owner(self, wallet_address: str) -> list:
        """
        Get all tickets owned by a wallet using QIE Blockchain SDK
        
        Args:
            wallet_address: Wallet address to query
            
        Returns:
            List of tickets with token_id and token_uri
        """
        if not self.qie_nft:
            return []
        
        # Use QIE SDK to get tickets
        return self.qie_nft.get_tickets_of_owner(wallet_address)
    
    def get_token_uri(self, token_id: int) -> str:
        """
        Get token URI using QIE Blockchain SDK
        
        Args:
            token_id: Token ID to query
            
        Returns:
            Token URI string
        """
        if not self.qie_contract:
            return ""
        
        # Use QIE SDK to get token URI
        return self.qie_contract.get_token_uri(token_id)

blockchain_service = BlockchainService()
