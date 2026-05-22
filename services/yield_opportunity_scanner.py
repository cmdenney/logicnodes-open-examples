import httpx

def get_info():
    return {
        "name": "yield_opportunity_scanner",
        "tier": "micro_task",
        "description": "Live yield opportunities via DefiLlama Yields API.",
        "input_schema": {
            "type": "object",
            "properties": {
                "chain": {"type": "string", "description": "Optional chain filter (e.g., 'Base', 'Ethereum')."}
            }
        }
    }

async def execute(params: dict) -> dict:
    chain = params.get("chain", "").lower()
    url = "https://yields.llama.fi/pools"
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(url)
            resp.raise_for_status()
            data = resp.json()
            pools = data.get("data", [])
            
            results = []
            for pool in pools:
                if chain and pool.get("chain", "").lower() != chain:
                    continue
                results.append({
                    "pool": pool.get("pool"),
                    "project": pool.get("project"),
                    "chain": pool.get("chain"),
                    "symbol": pool.get("symbol"),
                    "tvlUsd": pool.get("tvlUsd"),
                    "apy": pool.get("apy")
                })
                if len(results) >= 5:
                    break
                    
            return {
                "result": {
                    "yields": results
                },
                "source": "defillama",
                "live": True
            }
    except Exception as e:
        return {"error": str(e), "live": False}

async def run(params: dict) -> dict:
    return await execute(params)
