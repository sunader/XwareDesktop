# -*- coding: utf-8 -*-

import unittest
import tempfile

from libxware import mounts

_testContent = r"""# This is a comment.
/home/user/Download /home/user/.xware-desktop/profile/mnt/home\user\Download auto defaults,rw 0 0
/home/user/Down2 /home/user/.xware-desktop/profile/mnt/home\user\Down2 auto defaults,rw 0 0
"""


class XwareMountsTest(unittest.TestCase):
    def test_parse(self):
        results = mounts.parseMountsFile(_testContent.split("\n"))
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].localPath, "/home/user/Download")
        self.assertEqual(results[0].mntPath,
                         r"/home/user/.xware-desktop/profile/mnt/home\user\Download")
        self.assertEqual(results[1].localPath, "/home/user/Down2")
        self.assertEqual(results[1].mntPath,
                         r"/home/user/.xware-desktop/profile/mnt/home\user\Down2")

    def test_faker(self):
        with tempfile.NamedTemporaryFile() as tempMounts:
            tempMounts.write(_testContent.encode("UTF-8"))
            tempMounts.flush()
            # prepare done.

            # test 'mounts' property
            faker = mounts.MountsFaker(tempMounts.name)
            self.assertListEqual(faker.mounts, [
                "/home/user/Download",
                "/home/user/Down2",
            ])

            # test convertToMappedPath
            self.assertEqual(
                faker.convertToMappedPath("/home/user/Download"),
                "C:/TDDOWNLOAD/",
            )
            self.assertEqual(
                faker.convertToMappedPath("/home/user/Download/"),
                "C:/TDDOWNLOAD/",
            )

            # set mounts
            faker.mounts = ["/mnt/Down", "/media/Music"]
            self.assertListEqual(faker.mounts, [
                "/mnt/Down",
                "/media/Music",
            ])

            tempMounts.seek(0)
            newLines = tempMounts.readlines()
            self.assertEqual(
                b"".join(newLines),
                br'''# This file is automatically generated by Xware Desktop. Manually modifying this file via a text editor is not advised.
/mnt/Down /home/xinkai/.xware-desktop/profile/mnt/mnt\Down auto defaults,rw 0 0
/media/Music /home/xinkai/.xware-desktop/profile/mnt/media\Music auto defaults,rw 0 0
'''
            )
