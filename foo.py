#!/uer/bin/evn python2
import sys
sys.path.append('.')

from jinja2 import Template
from apps.common import mongodb

tmp ={
    'foo': 'foo',
    'bar': '{{ foo }}'
}

t = Template("Hello {{ bar }}!")

print (t.render(tmp))


