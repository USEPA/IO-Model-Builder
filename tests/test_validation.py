import iomb.model as model
import iomb.validation as validation
import unittest


class TestValidation(unittest.TestCase):

    def test_not_a_model(self):
        v = validation.validate('not a model')
        self.assertTrue(v.failed)

if __name__ == '__main__':
    unittest.main()
