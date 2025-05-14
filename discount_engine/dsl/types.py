class DSLRule:
    def __init__(
        self,
        name,
        condition,
        actions,
        priority=100,
        exclusive=False,
        scope="cart",
        code=None,
    ):
        self.name = name
        self.condition = condition
        self.actions = actions
        self.priority = priority
        self.exclusive = exclusive
        self.scope = scope
        self.code = code.upper() if code else None
