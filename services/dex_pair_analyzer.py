import httpx

def get_info():
    return {
        "name": "dex_pair_analyzer",
        "tier": "micro_task",
        "description": "Live DEX pair data (price, volume, liquidity) via DexScreener.",
        "input_schema": {
            "type": "object",
            "properties": {
                "pair_address": {"type": "string", "description": "Contract address of the liquidity pair."}
            },
            "required": ["pair_address"]
        }
    }

async def execute(params: dict) -> dict:
    pair = params.get("pair_address", "")
    if not pair:
        return {"error": "Missing pair_address", "live": False}
        
    url = f"https://api.dexscreener.com/latest/dex/pairs/{pair}"
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(url)
            resp.raise_for_status()
            data = resp.json()
            pairs = data.get("pairs", [])
            if pairs:
                p = pairs[0]
                return {
                    "result": {
                        "chainId": p.get("chainId"),
                        "dexId": p.get("dexId"),
                        "priceUsd": p.get("priceUsd"),
                        "volume24h": p.get("volume", {}).get("h24"),
                        "liquidityUsd": p.get("liquidity", {}).get("usd")
                    },
                    "source": "dexscreener",
                    "live": True
                }
            return {"error": "Pair not found", "live": False}
    except Exception as e:
        return {"error": str(e), "live": False}

async def run(params: dict) -> dict:
    return await execute(params)
