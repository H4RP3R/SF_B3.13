from xml.dom import minidom
import re


class HTML():
    def __init__(self, output=None):
        self.tag = 'html'
        self.output = output
        self.text = ''

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        if self.output == 'console':
            print(self)
        if self.output == 'file':
            with open('index.html', 'w') as f:
                print(self, file=f)

    def __add__(self, other):
        self.text += str(other)
        return self

    def __str__(self):
        # formats output text
        html = minidom.parseString(f'<{self.tag}>{self.text}</{self.tag}>')
        return re.sub(r'<\?.+\?>', '', html.toprettyxml())[1:]


class TopLevelTag(HTML):
    def __init__(self, tag, is_single=False, klass=None, **kwargs):
        self.tag = tag
        self.text = ''
        self.is_single = is_single
        self.attributes = {}
        self.klass = klass
        self.args = kwargs

        if klass is not None:
            self.attributes['class'] = ' '.join(klass)

    def __exit__(self, exception_type, exception_value, traceback):
        pass

    def __add__(self, other):
        self.text += str(other)
        return self

    def __str__(self):
        attrs = []
        for attribute, value in self.attributes.items():
            attrs.append(f' {attribute}="{value}"')
        for attribute, value in self.args.items():
            attrs.append(f' {attribute}="{value}"')
        attrs = ' '.join(attrs)
        if self.is_single:
            return f'<{self.tag}{attrs}/>'
        return f'<{self.tag}{attrs}>{self.text}</{self.tag}>'


class Tag(TopLevelTag):
    # I decided to determine all the necessary fields for this class in "TopLevelTag"
    # not to redetermine __init__ and __str__ only for "is_single"
    pass


if __name__ == '__main__':
    with HTML(output='console') as doc:  # or output='file'
        with TopLevelTag('head') as head:
            with Tag('title') as title:
                title.text = 'hello'
                head += title
            doc += head

        with TopLevelTag('body') as body:
            with Tag('h1', klass=('main-text',)) as h1:
                h1.text = 'Test'
                body += h1

            with Tag('div', klass=('container', 'container-fluid'), id='lead') as div:
                with Tag('p') as paragraph:
                    paragraph.text = 'another test'
                    div += paragraph

                with Tag('img', is_single=True, src='/icon.png') as img:
                    div += img

                body += div

            doc += body
