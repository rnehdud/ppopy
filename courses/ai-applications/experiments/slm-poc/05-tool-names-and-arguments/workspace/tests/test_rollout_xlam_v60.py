import unittest
from scripts.rollout_xlam_v60 import parse
class ParserChecks(unittest.TestCase):
    def test_native_calls(self):self.assertEqual(parse('[{"name":"x","arguments":{}}]'),[{'name':'x','arguments':{}}])
    def test_empty_array_and_plain_text(self):self.assertEqual(parse('[]'),[]);self.assertIsNone(parse('작업을 마쳤습니다.'))
    def test_no_repair_or_argument_dropping(self):
        with self.assertRaises(ValueError):parse('[{"name":"x","arguments":{}]')
        with self.assertRaises(ValueError):parse('[{"name":"x","arguments":"{}"}]')
if __name__=='__main__':unittest.main()
