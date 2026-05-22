import httpx

def get_info():
    return {
        "name": "token_security_check",
        "tier": "micro_task",
        "description": "Live token security info derived from DexScreener pairs.",
        "input_schema": {
            "type": "object",
            "properties": {
                "token_address": {"type": "string", "description": "Token contract address."}
            },
            "required": ["token_address"]
        }
    }

async def execute(params: dict) -> dict:
    token = params.get("token_address", "")
    if not token:
        return {"error": "Missing token_address", "live": False}
        
    url = f"https://api.dexscreener.com/latest/dex/tokens/{token}"
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(url)
            resp.raise_for_status()
            data = resp.json()
            pairs = data.get("pairs", [])
            
            if not pairs:
                return {"error": "Token not found or no pairs exist", "live": False}
                
            best_pair = pairs[0]
            liquidity = best_pair.get("liquidity", {}).get("usd", 0)
            fdv = best_pair.get("fdv", 0)
            
            # Simple security heuristic
            security_score = "LOW"
            if liquidity > 100000:
                security_score = "MEDIUM"
            if liquidity > 1000000 and fdv > 5000000:
                security_score = "HIGH"
                
            return {
                "result": {
                    "token_address": token,
                    "liquidity_usd": liquidity,
                    "fdv": fdv,
                    "security_score_estimate": security_score,
                    "pair_url": best_pair.get("url")
                },
                "source": "dexscreener",
                "live": True
            }
    except Exception as e:
        return {"error": str(e), "live": False}

async def run(params: dict) -> dict:
    return await execute(params)
