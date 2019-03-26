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
from jagtag import Method, jagtag_method


class MethodTests(TestCase):

    def test_method_parse_simple(self):
        method = Method('test', lambda env: env['foo'])
        self.assertEqual('bar', method.parse_simple({'foo': 'bar'}))

    def test_method_parse_simple_returns_None_if_no_simple_fn_is_provided(self):
        method = Method('test', None, lambda env: 'dummy')
        self.assertIsNone(method.parse_simple({}))

    def test_method_parse_complex_with_default_splitter(self):
        method = Method('test', None, lambda env, args: f'{args[0]} & {args[1]} & {args[2]}', True)
        self.assertEqual('foo & bar & baz', method.parse_complex({}, 'foo|bar|baz'))

    def test_method_parse_complex_with_custom_splitter(self):
        method = Method('test', None, lambda env, args: f'[{", ".join(args)}]', ['/', '|', '\\'])
        self.assertEqual('[sally, sunny, shady, sands]', method.parse_complex({}, 'sally/sunny|shady\\sands'))

    def test_method_parse_complex_fails_when_custom_splitter_requirements_are_not_met(self):
        method = Method('test', None, lambda env, args: f'{args[0]} says \'{args[1]}\'', ['|'])
        # verify it works when requirements are met first
        self.assertEqual('cow says \'moo\'', method.parse_complex({}, 'cow|moo'))
        self.assertEqual('<invalid test statement>', method.parse_complex({}, 'bad arguments'))

    def test_method_parse_complex_returns_None_if_no_complex_fn_is_provided(self):
        method = Method('test', lambda env: 'dummy')
        self.assertIsNone(method.parse_complex({}, ''))

    def test_method_init_fails_when_neither_parse_fn_is_not_None(self):
        self.assertRaises(ValueError, Method, 'test')

    def test_simple_method_decorator(self):
        @jagtag_method('test')
        def test(_):
            return 'bar'
        method = test()
        self.assertEqual('test', method.name)
        self.assertIsNotNone(method._fn_simple)
        self.assertIsNone(method._fn_complex)
        self.assertEqual('bar', method.parse_simple({}))
