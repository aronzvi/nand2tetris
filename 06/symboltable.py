class SymbolTable():
    def __init__(self):
        self.table = {}

    def add_entry(self, symbol, address):
        self.table[symbol] = address

    def contains(self, symbol):
        return symbol in self.table.keys()

    def get_address(self, symbol):
        return self.table[symbol]