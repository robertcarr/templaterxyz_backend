import unittest

from utils.core import get_upload_folder, get_shortuuid


class TestInstance:
    uuid = None
    user = 'abc'


class TestUploadFolder(unittest.TestCase):
    def setUp(self):
        self.instance = TestInstance()

    def test_get_upload_folder_anon(self):
        """ What happens when anon user is used?"""
        self.instance.uuid = get_shortuuid()
        self.instance.user = None
        folder = get_upload_folder(self.instance, 'myname.cnf')
        self.assertEqual(folder, f"_/{self.instance.uuid}/myname.cnf")

    def test_get_upload_folder_user(self):
        """ What happens when anon user is used?"""
        self.instance.uuid = get_shortuuid()
        self.instance.user = '123'
        folder = get_upload_folder(self.instance, 'myname.cnf')
        self.assertEqual(folder, f"{self.instance.uuid}/myname.cnf")


if __name__ == '__main__':
    unittest.main()
