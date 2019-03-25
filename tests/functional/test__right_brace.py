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

from NeoVintageous.tests import unittest


class Test_right_brace(unittest.FunctionalTestCase):

    def test_n(self):
        self.eq('|', 'n_}', '|')
        self.eq('fi|zz', 'n_}', 'fiz|z')
        self.eq('|1\n2\n\n3\n\n\n4\n5', 'n_}', '1\n2\n|\n3\n\n\n4\n5')
        self.eq('1\n2\n|\n3\n\n\n4\n5', 'n_}', '1\n2\n\n3\n|\n\n4\n5')
        self.eq('1\n2\n\n3\n|\n\n4\n5', 'n_}', '1\n2\n\n3\n\n\n4\n|5')

    def test_v(self):
        self.eq('fi|zz', 'v_}', 'fi|zz|')
        self.eq('|1\n2\n\n3\n\n\n4\n5', 'v_}', '|1\n2\n\n|3\n\n\n4\n5')
        self.eq('|1\n2\n\n3\n\n|\n4\n5', 'v_}', '|1\n2\n\n3\n\n\n4\n5|')
        self.eq('|1\n2\n\n|3\n\n\n4\n5', 'v_}', '|1\n2\n\n3\n\n|\n4\n5')
        self.eq('r_|1\n2\n\n3\n\n\n4\n5|', 'v_}', 'r_1\n2\n|\n3\n\n\n4\n5|')
        self.eq('r_|1\nfi|zz\n\n3\n\n\n4\n5', 'v_}', '1\nf|izz\n\n|3\n\n\n4\n5')

    def test_V(self):
        self.eq('|1\n|2\n\n3\n\n\n\n4\n5', 'l_}', '|1\n2\n\n|3\n\n\n\n4\n5')
        self.eq('|1\n2\n\n|3\n\n\n\n4\n5', 'l_}', '|1\n2\n\n3\n\n|\n\n4\n5')
        self.eq('|1\n2\n\n3\n\n|\n\n4\n5', 'l_}', '|1\n2\n\n3\n\n\n\n4\n5|')
        self.eq('r_|1\n2\n\n3\n\n\n\n4\n5|', 'l_}', 'r_1\n2\n|\n3\n\n\n\n4\n5|')
        self.eq('r_1\n2\n|\n3\n\n\n\n4\n5|', 'l_}', 'r_1\n2\n\n3\n|\n\n\n4\n5|')
        self.eq('r_|1\nfizz\n|2\n\n\n\n4', 'l_}', '1\n|fizz\n2\n\n|\n\n4')
