"""
QIE Validator Routes
API endpoints for QIE blockchain validation
"""

from fastapi import APIRouter, HTTPException, Query
from services.qie_validator import qie_validator
from typing import Optional

router = APIRouter(prefix="/validator", tags=["validator"])


@router.get("/network")
async def validate_network():
    """
    Validate QIE network connectivity and status
    
    Returns:
        Network validation result
    """
    try:
        result = qie_validator.validate_network()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Validation error: {str(e)}")


@router.get("/contract")
async def validate_contract():
    """
    Validate QIE contract state and accessibility
    
    Returns:
        Contract validation result
    """
    try:
        result = qie_validator.validate_contract()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Validation error: {str(e)}")


@router.get("/transaction/{tx_hash}")
async def validate_transaction(tx_hash: str):
    """
    Validate a QIE transaction
    
    Args:
        tx_hash: Transaction hash to validate
        
    Returns:
        Transaction validation result
    """
    try:
        result = qie_validator.validate_transaction(tx_hash)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Validation error: {str(e)}")


@router.get("/wallet/{address}")
async def validate_wallet(address: str):
    """
    Validate a QIE wallet address
    
    Args:
        address: Wallet address to validate
        
    Returns:
        Wallet validation result
    """
    try:
        result = qie_validator.validate_wallet_address(address)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Validation error: {str(e)}")


@router.get("/token/{token_id}")
async def validate_token(token_id: int):
    """
    Validate a QIE NFT token
    
    Args:
        token_id: Token ID to validate
        
    Returns:
        Token validation result
    """
    try:
        result = qie_validator.validate_token(token_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Validation error: {str(e)}")


@router.get("/contract/function/{function_name}")
async def validate_contract_function(
    function_name: str,
    params: Optional[str] = Query(None, description="Optional JSON string of parameters")
):
    """
    Validate if a contract function can be called
    
    Args:
        function_name: Name of the contract function
        params: Optional JSON string of parameters
        
    Returns:
        Function validation result
    """
    try:
        import json
        params_dict = None
        if params:
            try:
                params_dict = json.loads(params)
            except:
                raise HTTPException(status_code=400, detail="Invalid JSON in params")
        
        result = qie_validator.validate_contract_interaction(function_name, params_dict)
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Validation error: {str(e)}")


@router.get("/comprehensive")
async def comprehensive_validation():
    """
    Perform comprehensive validation of all QIE components
    
    Returns:
        Complete validation report
    """
    try:
        result = qie_validator.comprehensive_validation()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Validation error: {str(e)}")


@router.get("/health")
async def validator_health():
    """
    Quick health check for QIE validator service
    
    Returns:
        Health status
    """
    try:
        network_result = qie_validator.validate_network()
        contract_result = qie_validator.validate_contract()
        
        return {
            "status": "healthy" if network_result["connected"] else "degraded",
            "network_connected": network_result["connected"],
            "contract_loaded": contract_result.get("contract_loaded", False),
            "timestamp": network_result.get("latest_block", {}).get("timestamp")
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }

