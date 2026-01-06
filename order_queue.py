
from sortedcontainers import SortedDict

class order_queue:
    def __init__(self, side):
        self.levels = SortedDict(key=lambda x:-x) if side == 0 else SortedDict()
        self.best_price_cache = [None, None]
        
    def add_price_level(self, price):
        if price in self.levels: return
        self.levels[price] = [[None, None], [None, None, 0, 0]] 
        if not self.levels:
            self.best_price_cache = [price, price]
            return
        
        price_links, level_data = self.levels[price]
        
        prices = self.levels.keys()
        price_index = prices.index(price)
        index_length = len(keys)
        
        if price_index > 0:
            price_links[0] = prices[price_index - 1]
        if price_index < index_length - 1:
            price_links[1] = prices[price_index + 1]
            
        