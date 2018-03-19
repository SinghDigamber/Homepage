from collective.soupstrainer import SoupStrainer
import bs4
import unittest


class TestCase(unittest.TestCase):
    def test_return_type(self):
        strainer = SoupStrainer()
        data = u''
        self.assertTrue(isinstance(strainer(data), unicode))
        data = bs4.BeautifulSoup(u'', 'html.parser')
        self.assertTrue(isinstance(strainer(data), bs4.Tag))

    def test_default_exludes(self):
        strainer = SoupStrainer()
        testdata = []
        for tag in ['center', 'tt', 'big', 'small', 'basefont', 'font']:
            testdata.append(
                (u'<%s><img src="foo.gif" /></%s>' % (tag, tag),
                 u'<img src="foo.gif"/>')
            )
        for attribute in ['lang', 'valign', 'halign', 'border', 'frame',
                          'rules', 'cellspacing', 'cellpadding', 'bgcolor']:
            testdata.append(
                (u'<p %s="bar"><img src="foo.gif" /></p>' % attribute,
                 u'<p><img src="foo.gif"/></p>')
            )
        testdata.append(
            (u'<table width="100%" border="1" class="sortable">'
             u'<tr height="10" class="odd"><td colspan="2">Cell</td></tr>'
             u'<tr class="even"><td valign="bottom">Cell1</td><td height="10">Cell2</td></tr>'
             u'</table>',
             u'<table class="sortable">'
             u'<tr class="odd" height="10"><td colspan="2">Cell</td></tr>'
             u'<tr class="even"><td>Cell1</td><td>Cell2</td></tr>'
             u'</table>')
        )
        testdata.append(
            (u'<p style="float: left; border-bottom: 1px solid black; text-align: right">Bar</p>',
             u'<p style="float: left; text-align: right">Bar</p>')
        )
        for data, expected in testdata:
            self.assertEquals(strainer(data), expected)

    def test_class_blacklist(self):
        data = u'<p class="foo bar">Blubb</p>'
        strainer = SoupStrainer()
        expected = u'<p class="foo bar">Blubb</p>'
        self.assertEquals(strainer(data), expected)
        strainer = SoupStrainer(class_blacklist=['foo'])
        expected = u'<p class="bar">Blubb</p>'
        self.assertEquals(strainer(data), expected)
        strainer = SoupStrainer(class_blacklist=['bar'])
        expected = u'<p class="foo">Blubb</p>'
        self.assertEquals(strainer(data), expected)
        strainer = SoupStrainer(class_blacklist=['ba'])
        expected = u'<p class="foo bar">Blubb</p>'
        self.assertEquals(strainer(data), expected)


def test_suite():
    import sys
    return unittest.findTestCases(sys.modules[__name__])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
