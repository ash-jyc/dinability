class User:

    # constructor
    def __init__(self, name, dob, password):
        self.name = name
        self._dob = dob
        self._password = password
        self.ongoing_groups = {}
        self.finished_order = {}
        self.ongoing_order = {}
    
    # setters
    def update_name(self, new_name):
        self.name = new_name

    def set_password(self, new_password):
        self._password = new_password

    def add_group(self, new_group):
        self.ongoing_groups[new_group.get_name()] = new_group.get_members()
    
    def order_finished(self, group, order):
        self.finished_order[order] = group
        del self.ongoing_groups[group.get_name()]
        del self.ongoing_order[order]

    # getters
    def get_group(self):
        return self.ongoing_groups