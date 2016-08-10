import iomb.model as model
import iomb.validation as validation
import unittest
import os








class TestValidation(unittest.TestCase):

    def setUp(self):
        self.drc = tf(_DRC)

    def tearDown(self):
        os.remove(self.drc)

    def test_not_a_model(self):
        v = validation.validate('not a model')
        self.assertTrue(v.failed)

    def test_missing_fields(self):
        m = model.Model(None, None, None, None, None, None, None)
        self.assertTrue(validation.validate(m).failed)

if __name__ == '__main__':
    unittest.main()
