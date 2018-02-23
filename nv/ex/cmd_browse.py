from .tokens import TOKEN_COMMAND_BROWSE
from .tokens import TokenEof
from .tokens import TokenOfCommand
from NeoVintageous.nv import ex


@ex.command('browse', 'bro')
class TokenCommandBrowse(TokenOfCommand):
    def __init__(self, params, *args, **kwargs):
        super().__init__(params, TOKEN_COMMAND_BROWSE, 'browse', *args, **kwargs)
        self.target_command = 'ex_browse'


def scan_cmd_browse(state):
    params = {'cmd': None}

    state.skip(' ')
    state.ignore()

    m = state.match(r'(?P<cmd>.*)$')

    params.update(m.groupdict())
    if params['cmd']:
        raise NotImplementedError('parameter not implemented')

    return None, [TokenCommandBrowse(params), TokenEof()]
