#!/usr/bin/env python3
"""Kurz-Smoketest für das Maximum Autonomous Profit System (ohne Endlos-Loops).

- Initialisiert LiveDataIntegrator
- Sammelt einmal Daten
- Lässt Trading-Entscheidungen einmal laufen
- Lässt Dropshipping Trending-Produktsuche einmal laufen
- Berechnet Korrelationen einmal

Usage:
  python smoke_test_max_profit.py
"""

from __future__ import annotations

import asyncio

from live_data_integrator import live_data_integrator
from autonomous_trading_engine import autonomous_trader
from autonomous_dropshipping_engine import dropshipping_engine
from multi_asset_optimization_engine import multi_asset_optimizer


async def main() -> None:
    await live_data_integrator.initialize()

    try:
        data = await live_data_integrator.collect_all_data()

        social = data.get("social", {})
        print(f"social platforms: {list(social.keys())}")

        # Trading: eine Entscheidung
        await autonomous_trader.make_autonomous_decisions(data)

        # Dropshipping: einmal Trending-Produkte
        products = await dropshipping_engine.find_trending_products()
        print(f"trending_products: {len(products)}")

        # Multi-Asset: einmal Korrelationen
        correlations = await multi_asset_optimizer.analyze_market_correlations(data)
        div = correlations.get("diversification_score") if isinstance(correlations, dict) else None
        print(f"diversification_score: {div}")

        print("SMOKE_TEST_OK")

    finally:
        await live_data_integrator.close()


if __name__ == "__main__":
    asyncio.run(main())
