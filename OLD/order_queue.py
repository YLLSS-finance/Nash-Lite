
from sortedcontainers import SortedDict

class order_queue:
    def __init__(self, side, fill_order):
        self.levels = SortedDict(key=lambda x:-x) if side == 0 else SortedDict()
        self.best_price_cache = [None, None]
        self.fill_order = fill_order
        
    def add_price_level(self, price, order):
        if price in self.levels: return
        self.levels[price] = [[None, None], [order, order, sum(order[6]), 1]] 
        if not self.levels:
            self.best_price_cache = [price, price]
            return
        
        price_links, level_data = self.levels[price]
        
        prices = self.levels.keys()
        price_index = prices.index(price)
        index_length = len(prices)
        
        if price_index > 0:
            head_price = prices[price_index - 1]
            price_links[0] = head_price
            self.levels[head_price][0][1] = price
            
        if price_index < index_length - 1:
            tail_price = prices[price_index + 1]
            price_links[1] = tail_price
            
            self.levels[tail_price][0][0] = price
            
    def add_order(self, order):
        timestamp, order_id, mpid, contractID, price, side, qty, links = order
        # There is no need to add an order to the book if it has nothing to be filled
        if not qty: return
        if not price in self.levels: 
            self.add_price_level(price, order)
            return 
        level_ends, level_data = self.levels[price]
        prev_tail_order = level_data[1]
        prev_tail_order[7][1] = order
        links[:] = [prev_tail_order, None]
        level_data[1] = order
        
        level_data[2] += sum(order[6])
        level_data[3] += 1
    
    def remove_order(self, order):
        timestamp, order_id, mpid, contractID, price, side, qty, links = order
        price_links, level_data = self.levels[price]
        head_order, tail_order = level_data[0:2]
        
        if not head_order is None: head_order[7][1] = order
        if not tail_order is None: tail_order[7][0] = order
        
        if level_data[0] == order: level_data[0] = order[1]
        if level_data[1] == order: level_data[1] = order[0]
    
        level_data[3] -= 1
        
        if not level_data[3]:
            price_links, level_data = self.levels[price]
            del self.levels[price]
            if price_links == [None, None]: 
                self.best_price_cache = [None, None]
                return 
        
            head_price, tail_price = price_links
            if self.best_price_cache[0] == price: self.best_price_cache[0] = tail_price
            if self.best_price_cache[1] == price: self.best_price_cache[1] = head_price
        
            if not head_price is None: self.levels[head_price][1] = tail_price
            if not tail_price is None: self.levels[tail_price][0] = head_price