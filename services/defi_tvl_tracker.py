import httpx

def get_info():
    return {
        "name": "defi_tvl_tracker",
        "tier": "micro_task",
        "description": "Live TVL (Total Value Locked) for a DeFi protocol via DefiLlama.",
        "input_schema": {
            "type": "object",
            "properties": {
                "protocol_slug": {"type": "string", "description": "DefiLlama protocol slug (e.g., 'lido', 'aave')."}
            },
            "required": ["protocol_slug"]
        }
    }

async def execute(params: dict) -> dict:
    slug = params.get("protocol_slug", "").lower()
    if not slug:
        return {"error": "Missing protocol_slug", "live": False}
        
    url = f"https://api.llama.fi/protocol/{slug}"
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(url)
            resp.raise_for_status()
            data = resp.json()
            return {
                "result": {
                    "protocol": data.get("name"),
                    "tvl_usd": data.get("tvl"),
                    "chain_tvls": data.get("chainTvls")
                },
                "source": "defillama",
                "live": True
            }
    except Exception as e:
        return {"error": str(e), "live": False}

async def run(params: dict) -> dict:
    return await execute(params)
