
import numpy as np

class orders:
    # ORDER INDEX CALCULATIONS
    # STARTING INDEX OF ORDER WITH ACCOUNT-NATIVE ORDER ID N: 
    # self.account_order_map[account_id] + 9 * N
    
    # ORDER SCHEMA
    # timestamp, account_id, contract_id, price, side, red, inc, head_order, tail_order
    
    def __init__(self, account_ids, orders_per_account):
        self.orders_per_account = int(orders_per_account)
        
        amount_of_orders = len(accounts * orders_per_account)