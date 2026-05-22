import httpx
import os

def get_info():
    return {
        "name": "token_price_lookup",
        "tier": "micro_task",
        "description": "Live token price lookup from CoinGecko.",
        "input_schema": {
            "type": "object",
            "properties": {
                "token_id": {"type": "string", "description": "CoinGecko token ID (e.g., 'ethereum', 'solana')."}
            },
            "required": ["token_id"]
        }
    }

async def execute(params: dict) -> dict:
    token_id = params.get("token_id", "").lower()
    if not token_id:
        return {"error": "Missing token_id", "live": False}
        
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={token_id}&vs_currencies=usd"
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(url)
            resp.raise_for_status()
            data = resp.json()
            if token_id in data:
                return {
                    "result": {
                        "token": token_id,
                        "price_usd": data[token_id].get("usd")
                    },
                    "source": "coingecko",
                    "live": True
                }
            return {"error": "Token not found", "live": False}
    except Exception as e:
        return {"error": str(e), "live": False}

async def run(params: dict) -> dict:
    return await execute(params)
