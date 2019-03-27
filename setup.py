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

from setuptools import setup

with open('README.md', 'r') as fh:
    readme = fh.read()

setup(
    name='jagtag.py',
    version='0.1',
    author='Kaidan Gustave',
    author_email='kaidangustave@yahoo.com',
    license='APACHE-2.0',
    description='A Python port of JagTag',
    long_description=readme,
    long_description_content_type='text/markdown',
    url='https://github.com/Shengaero/jagtag.py',
    python_requires='>=3.7',
    project_urls={
        'Source': 'https://github.com/Shengaero/jagtag.py',
        'Tracker': 'https://github.com/Shengaero/jagtag.py/issues',
    },
    packages=['jagtag'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
