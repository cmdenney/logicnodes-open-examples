import httpx
import os
from dotenv import load_dotenv

load_dotenv() # Load from local .env
ALCHEMY_API_KEY = os.getenv("ALCHEMY_API_KEY", "YOUR_ALCHEMY_KEY_HERE")

def get_info():
    return {
        "name": "base_transaction_decoder",
        "tier": "micro_task",
        "description": "Live transaction data from Base via Alchemy.",
        "input_schema": {
            "type": "object",
            "properties": {
                "tx_hash": {"type": "string", "description": "Base network transaction hash."}
            },
            "required": ["tx_hash"]
        }
    }

async def execute(params: dict) -> dict:
    tx_hash = params.get("tx_hash", "")
    if not tx_hash:
        return {"error": "Missing tx_hash", "live": False}
        
    url = f"https://base-mainnet.g.alchemy.com/v2/{ALCHEMY_API_KEY}"
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "eth_getTransactionByHash",
        "params": [tx_hash]
    }
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.post(url, json=payload)
            resp.raise_for_status()
            data = resp.json()
            tx = data.get("result")
            if not tx:
                return {"error": "Transaction not found", "live": False}
                
            return {
                "result": {
                    "hash": tx.get("hash"),
                    "from": tx.get("from"),
                    "to": tx.get("to"),
                    "value_wei": int(tx.get("value", "0x0"), 16),
                    "blockNumber": int(tx.get("blockNumber", "0x0"), 16) if tx.get("blockNumber") else None
                },
                "source": "alchemy",
                "live": True
            }
    except Exception as e:
        return {"error": str(e), "live": False}

async def run(params: dict) -> dict:
    return await execute(params)
