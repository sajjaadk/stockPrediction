import random

# TODO: need to change function names
# we may not have to define the schema in context.globals, might be unnecessary if typing is consistent

def behavior(state, context):

    props = context.globals()
    market = {
        "agent_name": "market",
        "behaviors": ["@hash/counter/counter.rs", "market.py"],
        "counter": 0,
        "sells": [],
        "buys": [],
        "current_price": 10
    }
    retail_traders = [dict({
        "agent_name": "retail" + str(ind),
        "agent_type": "retail",
        "behaviors": ["@hash/counter/counter.rs", "sell.py", "buy.py"], # TODO: update the correct behaviors
        "shares": round(random.gauss(props["starting_shares"], 10)),
        "counter": 0,
        "capital": round(random.gauss(props["retail_capital"], 100)),
        "sell_threshold": random.gauss(props["retail_sell"],.02),
        "buy_threshold": random.gauss(props["retail_buy"],.02)
    }) for ind in range(int(props["retail_count"]))]

    wsb_traders = [dict({
        "agent_name": "wsb" + str(ind),
        "agent_type": "wsb",
        "behaviors": ["@hash/counter/counter.rs", "sell.py", "buy.py"], # TODO: update the correct behaviors
        "shares": round(random.gauss(props["starting_shares"], 10)),
        "counter": 0,
        "capital": random.gauss(props["wsb_capital"], 100),
        "sell_threshold": random.gauss(props["wsb_sell"], .05),
        "buy_threshold": random.gauss(props["wsb_buy"], .05)
    }) for ind in range(int(props["wsb_count"]))]

    hedge_funds = [dict({
        "agent_name": "hedge" + str(ind),
        "agent_type": "hedge",
        "behaviors": ["@hash/counter/counter.rs", "sell.py", "buy.py"], # TODO: update the correct behaviors
        "shares": round(random.gauss(props["starting_shares"], 10)) * 10,
        "counter": 0,
        "capital": round(random.gauss(props["hedge_capital"], 100)),
        "sell_threshold": random.gauss(props["hedge_sell"], .01),
        "buy_threshold": random.gauss(props["hedge_buy"],.01)
    }) for ind in range(int(props["hedge_count"]))]

    melvin_funds = [dict({
        "agent_name": "melvin" + str(ind), 
        "agent_type": "melvin",
        "behaviors": ["@hash/counter/counter.rs", "sell.py", "buy.py"], # TODO: update the correct behaviors
        "shares": round(random.gauss(props["starting_shares"], 10)) * 10,
        "counter": 0,
        "capital": round(random.gauss(props["melvin_capital"], 100)),
        "sell_threshold": random.gauss(props["melvin_sell"], .005),
        "buy_threshold": random.gauss(props["melvin_buy"], .005)
    }) for ind in range(int(props["melvin_count"]))]
    
    agents = retail_traders + wsb_traders + hedge_funds + melvin_funds + [market]
    for i, agent in enumerate(agents):
        state.add_message("hash", "create_agent", agent)
    state.add_message("hash", "remove_agent")