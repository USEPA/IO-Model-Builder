import iomb.util as util
import unittest
import uuid


class TestUtil(unittest.TestCase):

    def test_make_uuid(self):
        expected = str(uuid.uuid3(uuid.NAMESPACE_OID, "flow/a/1/b"))
        actual = util.make_uuid("Flow", None, "a", 1, "B")
        self.assertEqual(expected, actual)

if __name__ == '__main__':
    unittest.main()
