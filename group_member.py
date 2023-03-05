class group_member():
    def __init__(self, name, whether_receive_order, order_item, order_price, group) -> None:
        self.name = name
        self.whether_receive_order = whether_receive_order
        self.order_item = order_item
        self.order_price = order_price
        self.group = group

    def leave_group(self):
        self.group.delete_member(self)

    def get_group(self):
        return self.group