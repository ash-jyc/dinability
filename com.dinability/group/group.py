from collections import Counter

class group():
    def __init__(self, name, still_need_n_members, price_individual, chat_history, group_owner, group_members) -> None:
        self.name = name
        self.stil_need_n_member = still_need_n_members
        self.price_individual = price_individual
        self.chat_history = chat_history
        self.group_owner = group_owner
        self.group_members = group_members
        self.orders = Counter()

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name
    
    def get_chat_name(self, name):
        return self.chat_history[name]

    def set_order(self, order):
        self.orders[order] += 1

    def get_order(self):
        return self.orders

    def delete_member(self, member):
        if member in self.group_members:
            self.group_members.remove(member)
            return True
        else:
            return False