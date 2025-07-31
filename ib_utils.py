import nest_asyncio
nest_asyncio.apply()

from ib_insync import IB, Stock
import time

def enviar_ordre_ib(symbol, amount, direction, stop_loss_pct, stop_profit_pct=None):
    try:
        ib = IB()
        ib.connect('127.0.0.1', 7497, clientId=1)

        contract = Stock(symbol, 'SMART', 'USD')
        ib.qualifyContracts(contract)
        ib.reqMarketDataType(4)  # Use delayed market data for paper trading
        market_data = ib.reqMktData(contract, '', False, False)
        # time.sleep(2)
        ib.sleep(2) 
        current_price = market_data.last or market_data.close or 0
        ib.cancelMktData(contract)

        if current_price == 0:
            return {"success": False, "error": "No s'ha pogut obtenir el preu actual"}

        action = 'BUY' if direction.lower() == 'long' else 'SELL'

        # Calcula preus
        limit_price = round(current_price, 2)
        stop_loss_price = round(current_price * (1 - stop_loss_pct / 100), 2) if action == 'BUY' else round(current_price * (1 + stop_loss_pct / 100), 2)
        take_profit_price = None
        if stop_profit_pct:
            take_profit_price = round(current_price * (1 + stop_profit_pct / 100), 2) if action == 'BUY' else round(current_price * (1 - stop_profit_pct / 100), 2)
        else:
            # Si no es defineix take profit, el posem lluny per fer feliç la funció
            take_profit_price = round(current_price * (1 + 100 / 100), 2)

        bracket = ib.bracketOrder(
            action,
            amount,
            limit_price,
            take_profit_price,
            stop_loss_price
        )

        for order in bracket:
            ib.placeOrder(contract, order)

        ib.disconnect()

        return {
            "success": True,
            "status": bracket[0].orderId,
            "avgFillPrice": current_price
        }

    except Exception as e:
        return {"success": False, "error": str(e)}

def get_exit_price_ib(symbol):
    try:
        ib = IB()
        ib.connect('127.0.0.1', 7497, clientId=1)

        contract = Stock(symbol, 'SMART', 'USD')
        ib.qualifyContracts(contract)
        ib.reqMarketDataType(4)  # Use delayed market data for paper trading
        market_data = ib.reqMktData(contract, '', False, False)
        # time.sleep(2)
        ib.sleep(2)
        exit_price = market_data.last or market_data.close or 0
        ib.cancelMktData(contract)
        ib.disconnect()

        if exit_price == 0:
            return {"success": False, "error": "No s'ha pogut obtenir el preu de sortida"}

        return {"success": True, "exit_price": exit_price}

    except Exception as e:
        return {"success": False, "error": str(e)}
