from sortedcontainers import SortedDict

class position:
    def __init__(self, user_balances):
        # A position and margin manager class.
        self.userBalance = user_balances
        
        self.position = [0, 0]
        self.reducible = [0, 0]

        self.priceLevels = [SortedDict(key=lambda x:-x), SortedDict()]
        self.redOnlyLevels = [0, 0]
        
        self.redOnlyBoundaryPrice = [None, None]
        self.comparators = [lambda x, y: x < y or y is None, lambda x, y: x > y or y is None]
    
    def addOrder(self, side, price, red, inc):
        price_level = self.priceLevels[side]
        
        if not price in price_level:
            price_level[price] = [red, inc]
            
            if red and (not inc):
                self.redOnlyLevels += 1
                price_is_new_boundary = self.comparators[side]
                
                if price_is_new_boundary(price, self.redOnlyBoundaryPrice[side]):
                    self.redOnlyBoundaryPrice[side] = price
            
            return 
        
        else:
            qtys = price_level[price]
            prev_red_only = qtys[0] and (not qtys[1])
            qtys[0] += red
            qtys[1] += inc
            
            if prev_red_only and inc:
                self.redOnlyLevels[side] -= 1
                new_red_levels = self.redOnlyLevels[side]
                self.redOnlyBoundaryPrice = None if (not new_red_levels) else price_level.keys[new_red_levels - 1]
            
            return
        