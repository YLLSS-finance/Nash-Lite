
# Order Format
# 0 / timestamp
# 1 / mpid
# 2 / contractID
# 3 / price
# 4 / side
# 5 / [red, inc]

from sortedcontainers import SortedList

class order_book:
    def __init__(self):
        self.orders = [SortedList(key=self._comp_buy), SortedList(key=self._comp_sel)]
    
    def _comp_buy(self, order):
        return (-order[3], order[0])

    def _comp_sell(self, order):
        return (order[3], order[0])
    
    