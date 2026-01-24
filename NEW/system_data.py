
import numpy as np

# ORDER SCHEMA
# (shift - data)
# 0 - timestamp
# 1 - trader_id
# 2 - instrument_id
# 3 - price
# 4 - side
# 5 - red
# 6 - inc
# 7 - head
# 8 - tail
#
# ORDER IDS START FROM 1 AND THE ORDER ID 0 IS USED TO REPRESENT A NULL ORDER

class system_data:
    def __init__(self, preallocAccts=1_000_000, acctOrderLimit=20):
        self.ordersPerAccount = acctOrderLimit
        
        self.acctBalances = {}
        self.acctPositions = {}
        self.acctOrderMapping = {}
        self.acctNameMapping = {}
        
        self.orders = np.empty(preallocAccts * acctOrderLimit, dtype=np.int32)
    
    def orderIndex(self, orderID):
        return 9 * (orderID - 1)
    
    def order(self, orderID):
        '''
        Takes an order at param orderID and returns a np view (mutable) of the order at the orderID.
        '''
        order_idx = self.orderIndex(orderID)
        return self.orders[order_idx, order_idx + 9]
    
    def createAccount(self, acctID, acctName):
        acctID = int(acctID)
        
        if acctID in self.acctNameMapping:
            return False

        self.acctOrderMapping[acctID] = self.ordersPerAccount * len(self.acctOrderMapping.keys())
    
    def fill_order(self, order_view, price, qty):
        trader_id = order_view[1]
        instrument_id = order_view[2]
        order_price = order_view[3]
        order_side = order_view[4]
        
        trader_balances = self.acctBalances[trader_id]
        trader_position = self.acctPositions[trader_id][instrument_id]
        
        exit_price = price if order_side == 0 else 100 - price
        price_improvement = abs(price - order_price)
        
        position_sale_revenue = exit_price * red
        trader_balances[1] += inc_fill * price_improvement + position_sale_revenue
        trader_balances[0] += position_sale_revenue
        
        trader_position.log_fill()
        
    # types of order matches
    # a - matching incoming order
    # b - matching at specified price/qty (return total acquisition cost of the position
    
    def _fill(self, top_order_id, incoming_side, incoming_price, incoming_qty, incoming_red = 0):
        while True:
            if top_order_id == 0: break
            top_order = self.order(top_order_id)
            top_order_price = top_order[3]
            
            # check if the price is no longer crossing
            
            if incoming_side == 0:
                if incoming_price < top_order_price: break
            else:
                if top_order_price < incoming_price: break

            