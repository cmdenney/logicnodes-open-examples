import httpx
import os
from dotenv import load_dotenv

load_dotenv() # Load from local .env
HELIUS_API_KEY = os.getenv("HELIUS_API_KEY", "YOUR_HELIUS_KEY_HERE")

def get_info():
    return {
        "name": "solana_token_info",
        "tier": "micro_task",
        "description": "Solana token metadata and price via Helius.",
        "input_schema": {
            "type": "object",
            "properties": {
                "mint_address": {"type": "string", "description": "Solana token mint address."}
            },
            "required": ["mint_address"]
        }
    }

async def execute(params: dict) -> dict:
    mint = params.get("mint_address", "")
    if not mint:
        return {"error": "Missing mint_address", "live": False}
        
    url = f"https://mainnet.helius-rpc.com/?api-key={HELIUS_API_KEY}"
    payload = {
        "jsonrpc": "2.0",
        "id": "1",
        "method": "getAsset",
        "params": {"id": mint}
    }
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.post(url, json=payload)
            resp.raise_for_status()
            data = resp.json()
            if "result" in data:
                return {
                    "result": data["result"],
                    "source": "helius",
                    "live": True
                }
            return {"error": "Token not found", "live": False}
    except Exception as e:
        return {"error": str(e), "live": False}

async def run(params: dict) -> dict:
    return await execute(params)
