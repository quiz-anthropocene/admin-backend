from django.test import TestCase

from api import utilities_notion


class UtilitiesNotionTest(TestCase):
    def test_clean_markdown_links(self):
        string_with_markdown_links_list = [
            (
                "string with single link [https://quiztaplanete.fr/](https://quiztaplanete.fr/)",
                "string with single link https://quiztaplanete.fr/",
            ),
            (
                "string with single http link [http://test](http://test)",
                "string with single http link http://test",
            ),
            (
                "string with single link with text [test](http://test)",
                "string with single link with text test",
            ),
            (
                "string with single link with title [http://test](http://test title='test')",
                "string with single link with title http://test",
            ),
            (
                "string with two links [https://quiztaplanete.fr/](https://quiztaplanete.fr/) and again [https://quiztaplanete.fr/](https://quiztaplanete.fr/)",  # noqa
                "string with two links https://quiztaplanete.fr/ and again https://quiztaplanete.fr/",  # noqa
            ),
            (
                "string with normal link https://quiztaplanete.fr/",
                "string with normal link https://quiztaplanete.fr/",
            ),
            ("string with brackets []", "string with brackets []"),
            ("string with parenthesis ()", "string with parenthesis ()"),
            ("strange string []()", "strange string []()"),
            ("string without link", "string without link"),
            ("", ""),
        ]
        for string_with_markdown_links in string_with_markdown_links_list:
            self.assertEqual(
                utilities_notion.clean_markdown_links(string_with_markdown_links[0]),
                string_with_markdown_links[1],
            )
