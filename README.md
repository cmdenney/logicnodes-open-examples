# LogicNodes Open Examples

Welcome to the **LogicNodes Open Examples** repository! This repository contains the source code for our top 10 most requested, high-value deterministic microservices. These examples demonstrate how you can fetch real-time data from various providers (CoinGecko, DefiLlama, DexScreener, Alchemy, Helius) and return deterministic JSON structures compatible with the x402 payment protocol.

Each service is a simple Python function using `httpx` to handle live HTTP requests, making them incredibly fast, robust, and deployable as standalone AI agent tools.

## Supported Services

### 1. Token Price Lookup (`token_price_lookup.py`)
Fetches the live price of any cryptocurrency token (e.g., Bitcoin, Ethereum, Solana) directly from CoinGecko. Returns the exact USD price instantly.

### 2. DeFi TVL Tracker (`defi_tvl_tracker.py`)
Retrieves the real-time Total Value Locked (TVL) for any supported DeFi protocol (like Aave, Lido, Curve) from DefiLlama. Perfect for financial agents tracking protocol liquidity.

### 3. Wallet Balance Checker (`wallet_balance_checker.py`)
Checks the exact ETH and token balance for any given Base network wallet using the Alchemy API. Critical for accounting and transaction routing agents.

### 4. DEX Pair Analyzer (`dex_pair_analyzer.py`)
Analyzes real-time volume, price, and liquidity depth for any decentralized exchange (DEX) pair across multiple networks using DexScreener. Great for arbitrage and trading agents.

### 5. Solana Token Info (`solana_token_info.py`)
Given a Solana token mint address, returns comprehensive metadata, real-time price, and supply information directly via the Helius RPC.

### 6. Trending Tokens (`trending_tokens.py`)
Returns the top 5 most trending cryptocurrencies globally based on CoinGecko search volume and market interest, providing real-time market sentiment data.

### 7. Base Transaction Decoder (`base_transaction_decoder.py`)
Decodes an on-chain transaction hash on the Base network, extracting the exact sender, receiver, block number, and value transferred in Wei using Alchemy.

### 8. Yield Opportunity Scanner (`yield_opportunity_scanner.py`)
Scans DefiLlama's Yield API for the most lucrative liquidity pools and staking opportunities, filterable by specific chains like Base or Ethereum.

### 9. NFT Floor Price (`nft_floor_price.py`)
Gets the real-time floor price for any NFT collection contract on the Base network via Alchemy, checking prominent marketplaces like OpenSea and LooksRare.

### 10. Token Security Check (`token_security_check.py`)
Provides an automated security heuristic ("LOW", "MEDIUM", "HIGH") for a newly launched token by analyzing its FDV and liquidity depth on DexScreener. Useful for avoiding rug pulls.

---

## How It Works

Each script exposes two main functions:
- `get_info()`: Returns the service manifest including name, tier (cost in x402), and expected JSON input schema.
- `execute(params: dict)` / `run(params: dict)`: Executes the live external API call, gracefully handles errors, and returns the result in < 3 seconds.

We invite developers to study these implementations to understand how you can easily convert any public or private API into a monetizable x402 service!
