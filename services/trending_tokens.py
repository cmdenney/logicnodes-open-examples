import httpx

def get_info():
    return {
        "name": "trending_tokens",
        "tier": "micro_task",
        "description": "Live trending tokens from CoinGecko.",
        "input_schema": {
            "type": "object",
            "properties": {}
        }
    }

async def execute(params: dict) -> dict:
    url = "https://api.coingecko.com/api/v3/search/trending"
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(url)
            resp.raise_for_status()
            data = resp.json()
            coins = []
            for item in data.get("coins", [])[:5]:
                coin = item["item"]
                coins.append({
                    "id": coin.get("id"),
                    "name": coin.get("name"),
                    "symbol": coin.get("symbol"),
                    "market_cap_rank": coin.get("market_cap_rank")
                })
            return {
                "result": {
                    "trending": coins
                },
                "source": "coingecko",
                "live": True
            }
    except Exception as e:
        return {"error": str(e), "live": False}

async def run(params: dict) -> dict:
    return await execute(params)
