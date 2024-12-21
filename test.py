import unittest
from vr import VirtualFileSystem  # Импортируем из vr.py

class TestVirtualFileSystem(unittest.TestCase):
    def setUp(self):
        self.vfs = VirtualFileSystem("tests/test_fs.zip")

    def test_list_dir(self):
        result = self.vfs.list_dir("/")
        self.assertIn("dir1", result)

    def test_change_dir(self):
        self.vfs.change_dir("/dir1")
        self.assertEqual(self.vfs.current_path, "/dir1/")

if __name__ == "__main__":
    unittest.main()
