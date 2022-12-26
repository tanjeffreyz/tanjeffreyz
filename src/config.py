HOST = 'https://tanjeffreyz-github-overview.fly.dev'

GITHUB_STATISTICS = 'https://github.com/tanjeffreyz/github-statistics'

DELIMITERS = '|'.join([','])

NUM_COLS = 2

BANNER_WIDTH = 100

CARD_WIDTH = 49.75


class Setting:
    def __init__(self, allowed_values, default=None):
        assert len(allowed_values) > 0, 'Setting must have at least 1 allowed value'
        self.value = default
        self.allowed_values = set(allowed_values)


SETTINGS = {
    'order': Setting(
        ('zig-zag', 'in-order'),
        default='zig-zag'
    )
}
