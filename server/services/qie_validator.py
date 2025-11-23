"""
QIE Validator Service
Comprehensive validation for QIE blockchain operations:
- Network connectivity validation
- Transaction validation
- Contract state validation
- Wallet address validation
- Contract interaction validation
"""

from typing import Dict, List, Optional, Tuple
from web3 import Web3
from .qie_sdk import (
    create_qie_web3,
    load_qie_contract,
    QIEWeb3,
    QIEContract
)
import os
from dotenv import load_dotenv

load_dotenv()


class QIEValidator:
    """
    QIE Blockchain Validator
    Validates various aspects of QIE blockchain operations
    """
    
    def __init__(self):
        """Initialize QIE Validator"""
        self.qie_web3 = create_qie_web3()
        self.contract_address = os.getenv("QIE_CONTRACT_ADDRESS", "")
        self.contract = None
        
        if self.contract_address:
            try:
                # Load contract ABI (same as in blockchain.py)
                from .blockchain import NFT_ABI
                self.contract = load_qie_contract(
                    self.contract_address,
                    NFT_ABI
                )
            except Exception as e:
                print(f"Warning: Could not load QIE contract for validation: {e}")
    
    def validate_network(self) -> Dict:
        """
        Validate QIE network connectivity and status
        
        Returns:
            Validation result with network status
        """
        result = {
            "valid": False,
            "network": "QIE Testnet",
            "chain_id": 1983,
            "connected": False,
            "latest_block": None,
            "gas_price": None,
            "errors": []
        }
        
        try:
            # Check connection
            if not self.qie_web3.is_connected():
                result["errors"].append("Not connected to QIE network")
                return result
            
            result["connected"] = True
            
            # Get latest block
            try:
                latest_block = self.qie_web3.w3.eth.get_block('latest')
                result["latest_block"] = {
                    "number": latest_block.number,
                    "hash": latest_block.hash.hex(),
                    "timestamp": latest_block.timestamp
                }
            except Exception as e:
                result["errors"].append(f"Failed to get latest block: {str(e)}")
            
            # Get gas price
            try:
                gas_price = self.qie_web3.w3.eth.gas_price
                result["gas_price"] = str(gas_price)
            except Exception as e:
                result["errors"].append(f"Failed to get gas price: {str(e)}")
            
            # Check chain ID
            try:
                chain_id = self.qie_web3.w3.eth.chain_id
                if chain_id != 1983:
                    result["errors"].append(f"Unexpected chain ID: {chain_id}, expected 1983")
                else:
                    result["chain_id"] = chain_id
            except Exception as e:
                result["errors"].append(f"Failed to get chain ID: {str(e)}")
            
            result["valid"] = len(result["errors"]) == 0
            
        except Exception as e:
            result["errors"].append(f"Network validation error: {str(e)}")
        
        return result
    
    def validate_contract(self) -> Dict:
        """
        Validate QIE contract state and accessibility
        
        Returns:
            Validation result with contract status
        """
        result = {
            "valid": False,
            "contract_address": self.contract_address,
            "contract_loaded": False,
            "total_supply": None,
            "contract_functions": [],
            "errors": []
        }
        
        if not self.contract_address:
            result["errors"].append("QIE_CONTRACT_ADDRESS not configured")
            return result
        
        try:
            # Validate address format
            try:
                checksum_address = Web3.to_checksum_address(self.contract_address)
                result["contract_address"] = checksum_address
            except Exception as e:
                result["errors"].append(f"Invalid contract address format: {str(e)}")
                return result
            
            if not self.contract:
                result["errors"].append("Contract not loaded. Check contract address and ABI.")
                return result
            
            result["contract_loaded"] = True
            
            # Test contract functions
            try:
                total_supply = self.contract.total_supply()
                result["total_supply"] = total_supply
            except Exception as e:
                result["errors"].append(f"Failed to call totalSupply(): {str(e)}")
            
            # Check available functions
            if self.contract and hasattr(self.contract, 'contract'):
                contract_functions = [func for func in dir(self.contract.contract.functions) 
                                    if not func.startswith('_')]
                result["contract_functions"] = contract_functions[:10]  # Limit to first 10
            
            result["valid"] = len(result["errors"]) == 0
            
        except Exception as e:
            result["errors"].append(f"Contract validation error: {str(e)}")
        
        return result
    
    def validate_transaction(self, tx_hash: str) -> Dict:
        """
        Validate a QIE transaction
        
        Args:
            tx_hash: Transaction hash to validate
            
        Returns:
            Validation result with transaction details
        """
        result = {
            "valid": False,
            "tx_hash": tx_hash,
            "exists": False,
            "confirmed": False,
            "block_number": None,
            "status": None,
            "from_address": None,
            "to_address": None,
            "gas_used": None,
            "errors": []
        }
        
        try:
            # Validate hash format
            if not tx_hash or not tx_hash.startswith('0x'):
                result["errors"].append("Invalid transaction hash format")
                return result
            
            # Get transaction receipt
            try:
                tx_receipt = self.qie_web3.w3.eth.get_transaction_receipt(tx_hash)
                result["exists"] = True
                result["confirmed"] = True
                result["block_number"] = tx_receipt.blockNumber
                result["status"] = tx_receipt.status
                result["from_address"] = tx_receipt.get('from')
                result["to_address"] = tx_receipt.get('to')
                result["gas_used"] = tx_receipt.gasUsed
                
                if tx_receipt.status == 1:
                    result["valid"] = True
                else:
                    result["errors"].append("Transaction failed (status: 0)")
                    
            except Exception as e:
                if "not found" in str(e).lower():
                    result["errors"].append("Transaction not found on QIE network")
                else:
                    result["errors"].append(f"Failed to get transaction: {str(e)}")
            
        except Exception as e:
            result["errors"].append(f"Transaction validation error: {str(e)}")
        
        return result
    
    def validate_wallet_address(self, address: str) -> Dict:
        """
        Validate a QIE wallet address
        
        Args:
            address: Wallet address to validate
            
        Returns:
            Validation result
        """
        result = {
            "valid": False,
            "address": address,
            "checksum_address": None,
            "is_contract": False,
            "balance": None,
            "errors": []
        }
        
        try:
            # Validate address format
            if not address or not address.startswith('0x'):
                result["errors"].append("Invalid address format (must start with 0x)")
                return result
            
            if len(address) != 42:
                result["errors"].append(f"Invalid address length: {len(address)}, expected 42")
                return result
            
            # Convert to checksum
            try:
                checksum_address = Web3.to_checksum_address(address)
                result["checksum_address"] = checksum_address
            except Exception as e:
                result["errors"].append(f"Invalid address checksum: {str(e)}")
                return result
            
            # Check if it's a contract
            try:
                code = self.qie_web3.w3.eth.get_code(checksum_address)
                result["is_contract"] = len(code) > 2  # More than just 0x
            except Exception as e:
                result["errors"].append(f"Failed to check if address is contract: {str(e)}")
            
            # Get balance
            try:
                balance = self.qie_web3.w3.eth.get_balance(checksum_address)
                result["balance"] = str(balance)
            except Exception as e:
                result["errors"].append(f"Failed to get balance: {str(e)}")
            
            result["valid"] = len(result["errors"]) == 0
            
        except Exception as e:
            result["errors"].append(f"Address validation error: {str(e)}")
        
        return result
    
    def validate_token(self, token_id: int) -> Dict:
        """
        Validate a QIE NFT token
        
        Args:
            token_id: Token ID to validate
            
        Returns:
            Validation result with token details
        """
        result = {
            "valid": False,
            "token_id": token_id,
            "exists": False,
            "owner": None,
            "token_uri": None,
            "errors": []
        }
        
        if not self.contract:
            result["errors"].append("Contract not loaded")
            return result
        
        try:
            # Check if token exists
            try:
                owner = self.contract.owner_of(token_id)
                result["exists"] = True
                result["owner"] = owner
            except Exception as e:
                result["errors"].append(f"Token does not exist or error: {str(e)}")
                return result
            
            # Get token URI
            try:
                token_uri = self.contract.get_token_uri(token_id)
                result["token_uri"] = token_uri
            except Exception as e:
                result["errors"].append(f"Failed to get token URI: {str(e)}")
            
            result["valid"] = len(result["errors"]) == 0
            
        except Exception as e:
            result["errors"].append(f"Token validation error: {str(e)}")
        
        return result
    
    def validate_contract_interaction(self, function_name: str, params: Optional[Dict] = None) -> Dict:
        """
        Validate if a contract function can be called
        
        Args:
            function_name: Name of the contract function
            params: Optional parameters for the function
            
        Returns:
            Validation result
        """
        result = {
            "valid": False,
            "function_name": function_name,
            "function_exists": False,
            "callable": False,
            "errors": []
        }
        
        if not self.contract:
            result["errors"].append("Contract not loaded")
            return result
        
        try:
            # Check if function exists
            if hasattr(self.contract.contract.functions, function_name):
                result["function_exists"] = True
                
                # Try to get the function
                try:
                    func = getattr(self.contract.contract.functions, function_name)
                    result["callable"] = True
                    result["valid"] = True
                except Exception as e:
                    result["errors"].append(f"Function exists but not callable: {str(e)}")
            else:
                result["errors"].append(f"Function '{function_name}' not found in contract")
        
        except Exception as e:
            result["errors"].append(f"Contract interaction validation error: {str(e)}")
        
        return result
    
    def comprehensive_validation(self) -> Dict:
        """
        Perform comprehensive validation of all QIE components
        
        Returns:
            Complete validation report
        """
        report = {
            "overall_valid": False,
            "timestamp": None,
            "network": {},
            "contract": {},
            "summary": {
                "network_valid": False,
                "contract_valid": False,
                "total_errors": 0
            }
        }
        
        from datetime import datetime
        report["timestamp"] = datetime.utcnow().isoformat()
        
        # Validate network
        network_result = self.validate_network()
        report["network"] = network_result
        report["summary"]["network_valid"] = network_result["valid"]
        
        # Validate contract
        contract_result = self.validate_contract()
        report["contract"] = contract_result
        report["summary"]["contract_valid"] = contract_result["valid"]
        
        # Count total errors
        report["summary"]["total_errors"] = (
            len(network_result.get("errors", [])) +
            len(contract_result.get("errors", []))
        )
        
        # Overall validity
        report["overall_valid"] = (
            network_result["valid"] and
            contract_result["valid"]
        )
        
        return report


# Create singleton instance
qie_validator = QIEValidator()

