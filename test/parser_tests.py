#  Copyright 2019 Kaidan Gustave
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from unittest import TestCase
from jagtag import Parser, Method, jagtag_method


class ParserTests(TestCase):

    def test_parser_simple_method_parse(self):
        m = Method('test', lambda _: 'foo')
        p = Parser([m])
        self.assertEqual('foo', p.parse('{test}'))

    def test_parser_complex_method_parse(self):
        m = Method('test', None, lambda _, args: f'{args[0]} and {args[1]}', list('&'))
        p = Parser([m])
        self.assertEqual('foo and bar', p.parse('{test:foo&bar}'))

    def test_parser_with_decorated_simple_method(self):
        @jagtag_method(name='chat', simplifiable=True)
        def my_parse_func(env, args):
            user = env['user']
            if args is None:
                return f'{user} has entered the chat!'
            return f'{user} said: "{args[0]}"'

        parser = Parser([my_parse_func])
        parser['user'] = 'Kaidan'

        self.assertEqual('Kaidan has entered the chat!', parser.parse('{chat}'))
        self.assertEqual('Kaidan said: "Hello, World!"', parser.parse('{chat:Hello, World!}'))
