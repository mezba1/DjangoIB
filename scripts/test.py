import micawber

from bs4 import BeautifulSoup


# load up rules for some default providers, such as youtube and flickr
providers = micawber.bootstrap_basic()

# providers.request('http://www.youtube.com/watch?v=54XHDUOHuzU')


def f(s):
    o = providers.parse_html(s)
    print(o)
    print('=' * 80)


def clean(s):
    o = BeautifulSoup(s, 'lxml').text
    print(o)
    print('=' * 80)


f('''
<p>this<p> is a test: http://www.youtube.com/watch?v=54XHDUOHuzU
some link https://stackoverflow.com/questions/11286809/how-to-make-youtube-videos-embed-on-your-webpage-when-a-link-is-posted
and some text stackoverflow.com
''')

clean('''
not so many
<a href="" target="">hello
''')
