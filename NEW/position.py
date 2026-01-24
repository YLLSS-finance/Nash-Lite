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
        self.invaildPriceCheck = [lambda x: x >None]
        self.incCosts = [lambda x:x, lambda x:100 - x]
    
    
    def add_order(self, price, side, qty):
        '''
        Adds an order into the specified price level, side and quantity.
        If the margin is insufficiant, returns a null value.
        '''
        
        # when we are adding a new order into the user margin manager there are a few things to worry about.
        # first of all we have to get the reduce and increase quantity of the order.
        # then, check if the order would cause a position increase before full reduction (the limit price is crossing the reduce-only price)
        # if so, realloc the side of the red
        
        insert_price = price

print('hello there')
print(5 > None)