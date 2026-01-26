from sortedcontainers import SortedDict

class position:
    def __init__(self, user_balances):
        # A position and margin manager class.
        self.userBalance = user_balances
        
        self.position = [0, 0]
        self.reducible = [0, 0]

        self.priceLevels = [SortedDict(key=lambda x:-x), SortedDict()]
        
        self.redLevels = [0, 0]
        self.redBoundaryPrice = [None, None]
        
        self.incCosts = [lambda x:x, lambda x:100 - x]            

    def invaild_inc_price(self, side, price):
        boundary = self.redBoundaryPrice[side]
        if boundary is None: return False
        if side == 0:
            return price > boundary
        else:
            return price < boundary
    
    def set_boundary_price(self, side):
        self.redBoundaryPrice[side] = self.priceLevels[side].keys()[self.redLevels[side] - 1]
        
    def add_order(self, price, side, qty):
        '''
        Adds an order into the specified price level, side and quantity.
        If the margin is insufficiant, returns a null value.
        '''
        
        # basically we are just checking if the order crosses the boundary price (red-only best price)

        # Potential cases:
        # Reduce-only order - no foul
        # Order containing increase component - start allocating the increase component beginning from the worst level containing an reduce component (swap operation) 
        
        # reduce orders cannot commit any fouls as the possibility of an reduce order being placed implies that there are no increase orders in the system, and thus there is no price to cross.
        
        order_red = min(self.reducible[1 - side], qty)
        order_inc = qty - order_red
        margin_required = self.incCosts[side](price) * order_inc
    
        levels = self.priceLevels[side]
        changes = []
        for n in range(self.redLevels[side] - 1, -1, -1):
            if not order_inc: break
            if not self.priceLevels: break
            
            #TODO: check if there is a potential overflow error with the peekitem (critical error)
            swap_level_price, swap_level = levels.peekitem(-1 - n)
            if side == 0 and swap_level_price >= price: break
            if side == 0 and swap_level_price <= price: break
            
            # here we are decreasing the increase component of the order and making the levels at the better price that we are looking at do it instead
            swap_qty = min(order_inc, swap_level[1])
            order_inc -= swap_qty
            order_red += swap_qty
            
            margin_required -= abs(swap_level_price - price) * swap_qty
            changes.append([swap_level, swap_qty])
            
        if self.userBalance[1] < margin_required: 
            return False
        
        for swap_level, swap_qty in changes:
            prev_reduce = swap_level[0]
            swap_level[0] -= swap_qty
            swap_level[1] += swap_qty
            
            # Check if we have eradicated one of the levels containing reduce orders by turning all orders in it into inc
            if prev_reduce and swap_level[0] == 0:
                self.redLevels[side] -= 1
                
        if not price in levels:
            levels[price] = [0, 0]
        
        levels[price][0] += order_red
        levels[price][1] += order_inc
        return True
    
    def allocate_reducible_position(self):
        alloc_side = 0 if self.reducible[0] else 1
        alloc_qty = self.reducible[alloc_side]
        levels = self.priceLevels[1 - alloc_side]
        
        first_red_lvl = self.redLevels[alloc_side] - 1
        if first_red_lvl == -1: return 
        
        for i in range(first_red_lvl, len(levels.keys())):
            price, quantities = levels.peekitem(i)     
        