# Copyright (C) 2018 The NeoVintageous Team (NeoVintageous).
#
# This file is part of NeoVintageous.
#
# NeoVintageous is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# NeoVintageous is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with NeoVintageous.  If not, see <https://www.gnu.org/licenses/>.

from NeoVintageous.nv.options import get_option
from NeoVintageous.nv.utils import hide_panel


def _apply_cmdline_panel_settings(panel):
    _set = panel.settings().set

    _set('auto_complete', False)
    _set('auto_indent', False)
    _set('auto_match_enabled', False)
    _set('draw_centered', False)
    _set('draw_indent_guides', False)
    _set('gutter', False)
    _set('match_selection', False)
    _set('rulers', [])
    _set('scroll_past_end', False)
    _set('smart_indent', False)
    _set('translate_tabs_to_spaces', False)
    _set('word_wrap', False)


class Cmdline():

    EX = ':'
    SEARCH_BACKWARD = '?'
    SEARCH_FORWARD = '/'

    _TYPES = (
        EX,
        SEARCH_BACKWARD,
        SEARCH_FORWARD,
    )

    def __init__(self, window, type, on_done=None, on_change=None, on_cancel=None):
        self._window = window

        if type not in self._TYPES:
            raise ValueError('invalid cmdline type')

        self._type = type

        # TODO Make view a contructor dependency? window.active_view() is a race-condition whereas view.window() isn't
        if type in (self.SEARCH_FORWARD, self.SEARCH_BACKWARD) and not get_option(window.active_view(), 'incsearch'):
            on_change = None

        self._callbacks = {
            'on_done': on_done,
            'on_change': on_change,
            'on_cancel': on_cancel,
        }

    def prompt(self, initial_text):
        input_panel = self._window.show_input_panel(
            caption='',
            initial_text=self._type + initial_text,
            on_done=self._on_done,
            on_change=self._on_change,
            on_cancel=self._on_cancel
        )

        input_panel.set_name('Command-line mode')

        _set = input_panel.settings().set

        _set('_nv_ex_mode', True)

        # Mark the input panel as a widget.
        #
        # XXX This doesn't always work as expected, because the input panel is
        # already created before we setapply the settings, so there is a race-
        # condition.
        #
        # TODO [review] See if creating a Command-line mode.sublime-settings file
        # with all the relevant settings, including the "is_widget" setting solves
        # the race-condition issue described above.
        _set('is_widget', True)
        _set('is_vintageous_widget', True)

        _apply_cmdline_panel_settings(input_panel)

    def _callback(self, callback, *args):
        if self._callbacks and callback in self._callbacks:
            self._callbacks[callback](*args)

    def _is_valid_input(self, cmdline):
        return isinstance(cmdline, str) and len(cmdline) > 0 and cmdline[0] == self._type

    def _filter_input(self, inp):
        return inp[1:]

    def _on_done(self, inp):
        if not self._is_valid_input(inp):
            return self._on_cancel(force=True)

        self._callback('on_done', self._filter_input(inp))

    def _on_change(self, inp):
        if not self._is_valid_input(inp):
            return self._on_cancel(force=True)

        filtered_input = self._filter_input(inp)
        if filtered_input:
            self._callback('on_change', filtered_input)

    def _on_cancel(self, force=False):
        if force:
            hide_panel(self._window)

        self._callback('on_cancel')


class CmdlineOutput():

    def __init__(self, window):
        self._window = window

        self._output = self._window.create_output_panel('command-line')
        self._output.assign_syntax('Packages/NeoVintageous/res/Command-line output.sublime-syntax')

        _apply_cmdline_panel_settings(self._output)

    def show(self):
        self._window.run_command('show_panel', {'panel': 'output.command-line'})

    def write(self, text):
        self._output.run_command('insert', {'characters': text})
