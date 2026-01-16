
# order schame
# order_id (order's position in the order list), timestamp, contract, price, side, red, inc, head, tail

class orders:
    # ORDER INDEX CALCULATIONS
    # STARTING INDEX OF ORDER WITH ACCOUNT-NATIVE ORDER ID N: 
    # self.account_order_map[account_id] + 9 * N
    
    def __init__(self, orders_per_account):
        self.orders_per_account = int(orders_per_account)
        
        self.account_order_map = {}
        self.account_vacant_orders = {}
        self.orders = []
    
    def add_account(self, account_id):
        if not account_id in self.account_order_map:
            self.account_order_map = len(self.orders)
            self.account_vacant_orders = [i for i in range(0, self.orders_per_account)]
    
    def add_order(self, account_id, timestamp, contract, price, side, red, inc):
        if not account_id in self.account_order_map:
            return False
        
        vacant_orders = self.account_vacant_orders[account_id]
        if not vacant_orders:
            return False

        avbl_order_id = vacant_orders.pop()
        