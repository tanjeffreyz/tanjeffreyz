class Setting:
    def __init__(self, allowed_values, default=None):
        assert len(allowed_values) > 0, 'Setting must have at least 1 allowed value'
        self.value = default
        self.allowed_values = set(allowed_values)


SETTINGS = {
    'order': Setting(
        ('zig-zag', 'in-order'),
        default='in-order'
    )
}
