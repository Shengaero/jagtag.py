# jagtag.py

A Python port of [JagTag](https://github.com/jagrosh/JagTag).

### Basic Usage

jagtag.py includes helpful decorators that simplify the code you write down to single functions!

```python
from jagtag import jagtag_method, Parser, ParseException

@jagtag_method(name='says')
def says(env, args):
    user = env['user']
    if user is None:
        raise ParseException('No user in env!')
    msg = args[0]
    return f'{user} says "{msg}"'

parser = Parser([says])
parser['user'] = 'Kaidan'

print(parser.parse('{says:Hello, World!}'))  # Kaidan says "Hello, World!"
```
