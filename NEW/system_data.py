
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

class orders:
    def __init__(self, orders_per_account, prealloc_accounts):
        self.orders_per_account = orders_per_account
        self.maxAccounts = prealloc_accounts
        
        self.orders = np.empty(orders_per_account * prealloc_accounts, dtype=np.uint32)
        self.accountMappings = {}
        
    def add_account(self, account_id:int):
        cur_no_of_accts = len(self.accountMappings.keys())
        
        start_index = (len(self.accountMappings.keys) - 1) * 9 * self.orders_per_account
        self.accountMappings[account_id] = start_index