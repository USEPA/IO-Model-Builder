import unittest

import iomb.olca.dqx as dqx


class TestDqx(unittest.TestCase):
    def test_process_scheme(self):
        process_system = dqx.dq_process_system()
        self.assertEqual('70bf370f-9912-4ec1-baa3-fbd4eaf85a10',
                         process_system['@id'])
        self.assertEqual(2, len(process_system['indicators']))

    def test_exchange_scheme(self):
        exchange_system = dqx.dq_exchanges_system()
        self.assertEqual('d13b2bc4-5e84-4cc8-a6be-9101ebb252ff',
                         exchange_system['@id'])
        self.assertEqual(5, len(exchange_system['indicators']))


if __name__ == '__main__':
    unittest.main()
