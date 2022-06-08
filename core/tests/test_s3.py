from django.test import TestCase

from core.utils import s3


class UtilitiesTest(TestCase):
    def test_create_image_name(self):
        INSTANCE_IMAGES = [
            (5, "test.png", "000005-UUID.png"),
            (15, "another-test.jpeg", "000015-UUID.jpeg"),
            (150, "https://example.com/another-test.gif", "000150-UUID.gif"),
            (1500, "https://example.com/another-test.webp?height=100", "001500-UUID.webp"),
        ]
        for item in INSTANCE_IMAGES:
            image_name = s3.create_image_name(item[0], item[1])
            self.assertTrue(image_name[:4] in item[2])
