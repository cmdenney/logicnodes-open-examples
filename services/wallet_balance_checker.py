import httpx
import os
from dotenv import load_dotenv

load_dotenv() # Load from local .env
ALCHEMY_API_KEY = os.getenv("ALCHEMY_API_KEY", "YOUR_ALCHEMY_KEY_HERE")

def get_info():
    return {
        "name": "wallet_balance_checker",
        "tier": "micro_task",
        "description": "Live ETH and token balance checker on Base network via Alchemy.",
        "input_schema": {
            "type": "object",
            "properties": {
                "address": {"type": "string", "description": "Base wallet address."}
            },
            "required": ["address"]
        }
    }

async def execute(params: dict) -> dict:
    address = params.get("address", "")
    if not address:
        return {"error": "Missing address", "live": False}
        
    url = f"https://base-mainnet.g.alchemy.com/v2/{ALCHEMY_API_KEY}"
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "eth_getBalance",
        "params": [address, "latest"]
    }
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.post(url, json=payload)
            resp.raise_for_status()
            data = resp.json()
            eth_balance_wei = int(data.get("result", "0x0"), 16)
            eth_balance = eth_balance_wei / 1e18
            return {
                "result": {
                    "address": address,
                    "eth_balance": eth_balance,
                    "network": "base"
                },
                "source": "alchemy",
                "live": True
            }
    except Exception as e:
        return {"error": str(e), "live": False}

async def run(params: dict) -> dict:
    return await execute(params)
