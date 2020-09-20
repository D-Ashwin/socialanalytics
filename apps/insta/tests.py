from pprint import pprint

from common.BaseTestingHelper import BaseTestingHelper


class TestDemo(BaseTestingHelper):
    def test_01_demo_view(self):
        endpoint = '/insta/test/'
        test = "test_01_demo_view"

        self.print_nice(test, 'Start')

        r = self.client.get(endpoint)
        if r.status_code != 200:
            pprint(r.content)
        self.assertEqual(r.status_code, 200, "failed " + test)
        self.print_nice(test, 'OK')
