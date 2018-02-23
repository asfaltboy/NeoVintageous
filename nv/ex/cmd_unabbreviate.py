from .tokens import TOKEN_COMMAND_UNABBREVIATE
from .tokens import TokenEof
from .tokens import TokenOfCommand
from NeoVintageous.nv import ex


@ex.command('unabbreviate', 'una')
class TokenCommandUnabbreviate(TokenOfCommand):
    def __init__(self, params, *args, **kwargs):
        super().__init__(params, TOKEN_COMMAND_UNABBREVIATE, 'unabbreviate', *args, **kwargs)
        self.target_command = 'ex_unabbreviate'

    @property
    def short(self):
        return self.params['lhs']


def scan_cmd_unabbreviate(state):
    params = {'lhs': None}

    m = state.expect_match(r'\s+(?P<lhs>.+?)\s*$')
    params.update(m.groupdict())

    return None, [TokenCommandUnabbreviate(params), TokenEof()]
