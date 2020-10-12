import unittest

from utils.core import get_shortuuid


class TestShortUUID(unittest.TestCase):
    def test_get_shortuuid_uuid(self):
        """ Do I get a UUID when I call?"""
        id = get_shortuuid()
        self.assertTrue(len(id) == 22)

    def test_get_shortuuid_name(self):
        """ Named uuids are deterministic """
        id1 = get_shortuuid(name='mytesturl.com')
        id2 = get_shortuuid(name='mytesturl.com')
        self.assertEqual(id1, id2)

    def test_get_shortuuid_specific_length(self):
        """ Can I specify a length for a random id?"""
        id = get_shortuuid(length=10)
        self.assertTrue(len(id) == 10)


if __name__ == '__main__':
    unittest.main()
