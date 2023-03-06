import group
import group_member

class GroupOwner(group_member):

    # constructor
    def __init__(self, name: str, group: group):
        super().__init__()
        self.name = name
        self.price_total = 0.0
        self.payment_code = None
        self.group = group
    
    # getters
    def get_name(self):
        return self.name
    
    def get_group(self):
        return self.group
    
    def cancel_group(self):
        self.group = None
        return True

    # setters
    def set_payment_code(self, picture):
        self.payment_code = picture