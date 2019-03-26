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

from typing import List, Union, Callable
from jagtag import Method


class Parser:
    def __init__(
        self,
        methods: List[Union[Method, Callable]],
        iterations: int = 200,
        max_len: int = 4000,
        max_output: int = 1995
    ):
        self._methods = dict()
        for method in methods:
            # Direct provision of the Method
            if type(method) == Method:
                self._methods[method.name] = method
            # Indirect provision, most likely a decorated function
            # that can be converted into a Method via a no-args call.
            # This is very hacky, but it works fairly well.
            # TODO Check if @jagtag_method decorator exists on function?
            else:
                try:
                    generated = method()
                except Exception:
                    raise Parser.__cannot_convert_to_method(method)
                if type(generated) != Method:
                    raise Parser.__cannot_convert_to_method(method)
                self._methods[generated.name] = generated
        self._env = {}
        self._iterations = iterations
        self._max_len = max_len
        self._max_output = max_output

    def __setitem__(self, key, value):
        self._env[key] = value

    def clear(self):
        self._env.clear()

    def parse(self, text_input: str):
        output = Parser.__filter_escapes(text_input)
        count = 0
        last_output = ''

        while last_output != output and count < self._iterations and len(output) <= self._max_len:
            last_output = output
            i1 = output.find('}')
            i2 = -1 if i1 == -1 else output.rfind('{')
            if i1 != -1 and i2 != -1:
                contents = output[i2 + 1:i1]
                result = None
                split = contents.find(':')
                if split == -1:
                    method = self._methods[contents.strip()]
                    if method is not None:
                        try:
                            result = method.parse_simple(self._env)
                        except ParseException as ex:
                            return ex.msg
                else:
                    name = contents[0:split]
                    params = contents[split + 1:]
                    method = self._methods[name.strip()]
                    if method is not None:
                        try:
                            result = method.parse_complex(self._env, params)
                        except ParseException as ex:
                            return ex.msg

                if result is None:
                    result = '{' + contents + '}'
                output = output[0:i2] + Parser.__filter_all(result) + output[i1 + 1:]
            count = count + 1

        output = Parser.__defilter_all(output)
        if len(output) > self._max_output:
            output = output[0:self._max_output]
        return output

    # Internal Utilities
    # TODO Maybe move these to a separate file?

    @staticmethod
    def __filter_escapes(text_input: str):
        return text_input.replace('\\{', '\u0012').replace('\\|', '\u0013').replace('\\}', '\u0014')

    @staticmethod
    def __filter_all(text_input: str):
        return Parser.__filter_escapes(text_input).replace('{', '\u0015').replace('}', '\u0016')

    @staticmethod
    def __defilter_escapes(text_input: str):
        return text_input.replace('\u0012', '\\{').replace('\u0013', '\\|').replace('\u0014', '\\}')

    @staticmethod
    def __defilter_all(text_input: str):
        return Parser.__defilter_escapes(text_input).replace('\u0015', '{').replace('\u0016', '}')

    @staticmethod
    def __cannot_convert_to_method(method):
        return ValueError(f'Unable to convert value to Method: {method}')


class ParseException:
    def __init__(self, msg: str):
        self.msg = msg
