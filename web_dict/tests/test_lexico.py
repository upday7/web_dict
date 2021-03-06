#  Copyright (C) 2016-2020  Kyle.Hwang <upday7[at]163.com>
#  #
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as
#  published by the Free Software Foundation, either version 3 of the
#  License, or (at your option) any later version, with the additions
#  listed at the end of the accompanied license file.
#  #
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#  #
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#  #
#  NOTE: This program is subject to certain additional terms pursuant to
#  Section 7 of the GNU Affero General Public License.  You should have
#  received a copy of these additional terms immediately following the
#  terms and conditions of the GNU Affero General Public License which
#  accompanied this program.

import json
import unittest

from web_dict.core.prviders.lexico import Lexico


class CollinsTest(unittest.TestCase):

    # def test_spanish_1(self):
    #     c = Lexico('dia',)
    #     self._p(c)

    def test_es_1(self):
        c = Lexico("in", "en")
        self._p(c)

    # def test_english_1(self):
    #     c = Lexico('test', 'en')
    #     self._p(c)

    def _p(self, c):
        print(json.dumps(c.to_dict(), indent=4, ensure_ascii=False))


if __name__ == "__main__":
    unittest.main()
