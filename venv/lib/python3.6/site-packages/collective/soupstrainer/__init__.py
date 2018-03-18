import bs4


class SoupStrainer(object):
    def __init__(self, exclusions=None, style_whitelist=None,
                 class_blacklist=None, parser='html.parser'):
        self.parser = parser
        if exclusions is None:
            exclusions = [
                (['center', 'tt', 'big', 'small', 'basefont', 'font'],
                 []),
                ([], ['lang', 'valign', 'halign', 'border', 'frame',
                      'rules', 'cellspacing', 'cellpadding', 'bgcolor']),
                (['table', 'th', 'td'], ['width', 'height']),
            ]
        if style_whitelist is None:
            style_whitelist = ['text-align', 'list-style-type',
                               'float']
        if class_blacklist is None:
            class_blacklist = []
        self.exclusions = {}
        for tags, attrs in exclusions:
            if len(attrs) == 0:
                for tag in tags:
                    self.exclusions[tag] = None
                continue
            if len(tags) == 0:
                tags = [None]
            for tag in tags:
                self.exclusions[tag] = self.exclusions.setdefault(
                    tag, set()).union(attrs)
        self.style_whitelist = set(style_whitelist)
        self.class_blacklist = set(class_blacklist)

    def __call__(self, data):
        if isinstance(data, basestring):
            return unicode(self.clean(bs4.BeautifulSoup(data, self.parser)))
        else:
            return self.clean(data)

    def clean(self, soup):
        for elem in soup.recursiveChildGenerator():
            if not isinstance(elem, bs4.Tag):
                continue
            if self.exclusions.get(elem.name, []) is None:
                parent = elem.parent
                index = parent.contents.index(elem)
                elem.extract()
                for child in reversed(elem.contents):
                    parent.insert(index, child)
            else:
                attrs = self.exclusions.get(None, set())
                attrs = attrs.union(
                    self.exclusions.get(elem.name, set()))
                attrs = attrs.intersection(
                    set(x for x in elem.attrs))
                for attr in attrs:
                    del elem[attr]
            if elem.has_attr('class'):
                classes = (x for x in elem['class']
                           if x not in self.class_blacklist)
                elem['class'] = u" ".join(classes)
                if elem['class'].strip() == '':
                    del elem['class']
            if elem.has_attr('style'):
                styles = (x.split(':', 1)
                          for x in elem['style'].split(';'))
                styles = (x for x in styles
                          if x[0].strip() in self.style_whitelist)
                elem['style'] = u";".join(
                    u":".join(x) for x in styles)
                if elem['style'].strip() == '':
                    del elem['style']
        return soup


def main():
    print "Hallo, Welt!"
