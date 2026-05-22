import httpx
import os
from dotenv import load_dotenv

load_dotenv() # Load from local .env
ALCHEMY_API_KEY = os.getenv("ALCHEMY_API_KEY", "YOUR_ALCHEMY_KEY_HERE")

def get_info():
    return {
        "name": "nft_floor_price",
        "tier": "micro_task",
        "description": "Live NFT floor price on Base via Alchemy.",
        "input_schema": {
            "type": "object",
            "properties": {
                "contract_address": {"type": "string", "description": "NFT collection contract address."}
            },
            "required": ["contract_address"]
        }
    }

async def execute(params: dict) -> dict:
    contract = params.get("contract_address", "")
    if not contract:
        return {"error": "Missing contract_address", "live": False}
        
    url = f"https://base-mainnet.g.alchemy.com/nft/v3/{ALCHEMY_API_KEY}/getFloorPrice?contractAddress={contract}"
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(url)
            resp.raise_for_status()
            data = resp.json()
            
            return {
                "result": {
                    "contractAddress": contract,
                    "openSea": data.get("openSea", {}),
                    "looksRare": data.get("looksRare", {})
                },
                "source": "alchemy",
                "live": True
            }
    except Exception as e:
        return {"error": str(e), "live": False}

async def run(params: dict) -> dict:
    return await execute(params)
