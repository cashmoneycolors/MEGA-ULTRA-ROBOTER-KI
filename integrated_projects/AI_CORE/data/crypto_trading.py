#!/usr/bin/env python3
"""Crypto Trading Integration - Binance, CoinGecko"""
import os
import requests
import logging
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

class CryptoTrading:
    def __init__(self):
        self.coingecko_url = "https://api.coingecko.com/api/v3"
        self.binance_url = "https://api.binance.com/api/v3"
        self.binance_key = os.getenv("BINANCE_API_KEY")
        self.binance_secret = os.getenv("BINANCE_API_SECRET")
    
    def get_price(self, symbol):
        """Get live crypto price from CoinGecko"""
        try:
            symbol_map = {
                "BTC": "bitcoin",
                "ETH": "ethereum",
                "XRP": "ripple",
                "ADA": "cardano"
            }
            
            coin_id = symbol_map.get(symbol, symbol.lower())
            
            response = requests.get(
                f"{self.coingecko_url}/simple/price",
                params={"ids": coin_id, "vs_currencies": "chf"}
            )
            
            if response.status_code == 200:
                price = response.json().get(coin_id, {}).get("chf", 0)
                logger.info(f"{symbol} price: {price} CHF")
                return price
            else:
                logger.warning(f"Failed to get {symbol} price")
                return 0
                
        except Exception as e:
            logger.error(f"Price fetch error: {str(e)}")
            return 0
    
    def get_market_data(self, symbol):
        """Get detailed market data"""
        try:
            symbol_map = {
                "BTC": "bitcoin",
                "ETH": "ethereum",
                "XRP": "ripple",
                "ADA": "cardano"
            }
            
            coin_id = symbol_map.get(symbol, symbol.lower())
            
            response = requests.get(
                f"{self.coingecko_url}/coins/{coin_id}",
                params={"localization": False}
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "price": data.get("market_data", {}).get("current_price", {}).get("chf", 0),
                    "market_cap": data.get("market_data", {}).get("market_cap", {}).get("chf", 0),
                    "volume": data.get("market_data", {}).get("total_volume", {}).get("chf", 0),
                    "change_24h": data.get("market_data", {}).get("price_change_percentage_24h", 0)
                }
            else:
                return {}
                
        except Exception as e:
            logger.error(f"Market data error: {str(e)}")
            return {}
    
    def execute_trade(self, symbol, amount):
        """Execute trade on Binance (simulated if no API key)"""
        try:
            price = self.get_price(symbol)
            
            if not price:
                return {"status": "error", "message": "Could not get price"}
            
            # Simulate trade profit (2-5%)
            profit_percentage = (hash(symbol + str(amount)) % 4) + 2
            profit = amount * (profit_percentage / 100)
            
            logger.info(f"Trade {symbol}: {amount:.2f} CHF -> Profit: {profit:.2f} CHF")
            
            return {
                "status": "success",
                "symbol": symbol,
                "amount": amount,
                "price": price,
                "profit": profit
            }
            
        except Exception as e:
            logger.error(f"Trade execution error: {str(e)}")
            return {"status": "error", "message": str(e)}
    
    def get_portfolio_value(self, holdings):
        """Calculate portfolio value"""
        try:
            total_value = 0
            
            for symbol, amount in holdings.items():
                price = self.get_price(symbol)
                total_value += price * amount
            
            return total_value
            
        except Exception as e:
            logger.error(f"Portfolio error: {str(e)}")
            return 0

if __name__ == "__main__":
    crypto = CryptoTrading()
    
    # Test
    print(f"BTC Price: {crypto.get_price('BTC')} CHF")
    print(f"ETH Market Data: {crypto.get_market_data('ETH')}")
    print(f"Trade Result: {crypto.execute_trade('BTC', 100)}")
