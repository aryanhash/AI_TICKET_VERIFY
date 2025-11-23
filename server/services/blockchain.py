from web3 import Web3
from eth_account.messages import encode_defunct
import json
import os

try:
    from web3.middleware import geth_poa_middleware
except ImportError:
    geth_poa_middleware = None

QIE_RPC_URL = os.getenv("QIE_RPC_URL", "https://rpc-mainnet.qie.digital")
QIE_CHAIN_ID = 5656
CONTRACT_ADDRESS = os.getenv("NFT_CONTRACT_ADDRESS", "")
ORGANIZER_PRIVATE_KEY = os.getenv("ORGANIZER_PRIVATE_KEY", "")

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
    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider(QIE_RPC_URL))
        if geth_poa_middleware:
            self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)
        
        if CONTRACT_ADDRESS:
            self.contract = self.w3.eth.contract(
                address=Web3.to_checksum_address(CONTRACT_ADDRESS),
                abi=NFT_ABI
            )
        else:
            self.contract = None
    
    def verify_signature(self, message: str, signature: str, wallet_address: str) -> bool:
        try:
            message_hash = encode_defunct(text=message)
            recovered_address = self.w3.eth.account.recover_message(message_hash, signature=signature)
            return recovered_address.lower() == wallet_address.lower()
        except Exception as e:
            print(f"Signature verification error: {e}")
            return False
    
    async def mint_ticket(self, wallet_address: str, metadata_uri: str) -> dict:
        if not self.contract or not ORGANIZER_PRIVATE_KEY:
            raise Exception("Contract not initialized or private key not set")
        
        try:
            checksum_address = Web3.to_checksum_address(wallet_address)
            
            account = self.w3.eth.account.from_key(ORGANIZER_PRIVATE_KEY)
            
            nonce = self.w3.eth.get_transaction_count(account.address)
            
            transaction = self.contract.functions.mint(
                checksum_address,
                metadata_uri
            ).build_transaction({
                'chainId': QIE_CHAIN_ID,
                'gas': 300000,
                'gasPrice': self.w3.eth.gas_price,
                'nonce': nonce,
            })
            
            signed_txn = self.w3.eth.account.sign_transaction(transaction, ORGANIZER_PRIVATE_KEY)
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.raw_transaction)
            
            tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            
            total_supply = self.contract.functions.totalSupply().call()
            token_id = total_supply - 1
            
            return {
                "success": True,
                "tx_hash": tx_hash.hex(),
                "token_id": token_id,
                "transaction_receipt": dict(tx_receipt)
            }
        except Exception as e:
            print(f"Minting error: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def get_tickets_of_owner(self, wallet_address: str) -> list:
        if not self.contract:
            return []
        
        try:
            checksum_address = Web3.to_checksum_address(wallet_address)
            balance = self.contract.functions.balanceOf(checksum_address).call()
            
            tickets = []
            total_supply = self.contract.functions.totalSupply().call()
            
            for token_id in range(total_supply):
                try:
                    owner = self.contract.functions.ownerOf(token_id).call()
                    if owner.lower() == checksum_address.lower():
                        token_uri = self.contract.functions.tokenURI(token_id).call()
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
    
    def get_token_uri(self, token_id: int) -> str:
        if not self.contract:
            return ""
        
        try:
            return self.contract.functions.tokenURI(token_id).call()
        except Exception as e:
            print(f"Error fetching token URI: {e}")
            return ""

blockchain_service = BlockchainService()
