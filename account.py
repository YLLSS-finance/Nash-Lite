
# Order Format
# 0 / timestamp
# 1 / orderID
# 2 / mpid
# 3 / contractID
# 4 / price
# 5 / side
# 6 / [red, inc]
# 7 / [head, tail]

class account:
    def __init__(self, _master, _mpid):
        self.contracts = _master.books
        self.mpid = mpid
        
        self.balance = [0, 0]
        
        self.positions = {}
    
    def remove_existing_order(self, contract, side):
        contract = str(contract)
        if not contract in self.positions: return False
        
        orders, position_data = self.positions[contract]
        pos, avbl = position_data
        
        order = order[side]
        if order is None: return 
        
        # Remove the order from the book
        self.contracts[contract].remove_order(order)
        
        order_red, order_inc = order[6]
        order_side = order[5]
        order_price = order[4]
        order_contract = order[3]
        
        if order_red and (not order_contract in self.positions):
            raise Exception('Fatal error')
        
        # Return margin and used position
        avbl[1 - order_side] += order_red
        self.balance[1] += order_inc * (order_price if order_side == 0 else 100 - order_price)

        orders[side] = None
        
    def add_order(self, timestamp, contract, price, side, qty):
        if not contract in self.contracts: return False
        price = int(price)
        side = int(side)
        qty = int(qty)
        
        if price < 1 or price > 99 or (not side in (0, 1)) or qty < 1: return False
        
        if not contract in self.positions[contract]: self.positions[contract] = [[None, None], [[0, 0], [0, 0]]]
        
        orders, positions = self.positions[contract]
        
        if contract in self.positions:
            pos, avbl = positions
            red = min(qty, avbl[1 - side])
        else:
            red = 0
        
        inc = qty - red
        margin_used = qty * (price if side == 0 else 100 - side)
        
        if margin_used > self.balance[1]: return False
        self.balance[1] -= margin_used
        if red: avbl[1 - side] -= red
        
        order = [timestamp, self.mpid, contract, price, side, [red, inc]]
        orders[side] = order
        self.contracts[contract].add_order(order)