import unittest
import sys
# sys.path.append('CS_DOWNLOADER\cs_downloader\downloader')
from downloader import api_builder as ab

class TestApiBuilder(unittest.TestCase):

    # def test_get_params_from_csv(self):
    #     self.assertIs(type(ab.get_params_from_csv()), dict)
    #     self.assertIs(type(ab.get_params_from_csv('abc')), str)
    #
    # def test_get_params_from_json(self):
    #     self.assertIs(type(ab.get_params_from_json()), dict)

    def test_has_valid_fields(self):
        self.assertIs(type(ab.has_valid_fields({})), bool)
        self.assertIs(ab.has_valid_fields({'foo': 'a', 'customerinn': '1'}), False)
        self.assertIs(ab.has_valid_fields({'fz': '44', 'customerinn': '1'}), True)

    def test_choose_strategy(self):
        self.assertIs(type(ab.choose_strategy({})), str)
        self.assertEqual(ab.choose_strategy({'fz': '44', 'customerinn': '1'}),
                         ab.SELECT)
        self.assertEqual(ab.choose_strategy({'fz': '44', 'okdp_okpd': '1'}),
                         ab.SEARCH)
    #
    # def test_build_query(self):
    #     self.assertIs(type(ab.build_query(ab.SELECT,
    #                                      {'fz': '44', 'customerinn': '1'}), tuple)


if __name__ == '__main__':
    unittest.main()
