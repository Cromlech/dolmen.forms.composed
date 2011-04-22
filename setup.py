# -*- coding: utf-8 -*-

from os.path import join
from setuptools import setup, find_packages

name = 'dolmen.forms.composed'
version = '2.0a1dev'
readme = open(join('src', 'dolmen', 'forms', 'composed', 'README.txt')).read()
history = open(join('docs', 'HISTORY.txt')).read()


install_requires = [
    'dolmen.forms.base',
    'dolmen.template',
    'dolmen.view',
    'dolmen.viewlet',
    'grokcore.component',
    'martian',
    'setuptools',
    'zope.component',
    'zope.interface',
    ],

tests_require = [
    'WebOb',
    'dolmen.location',
    'cromlech.webob',
    'cromlech.browser [test]',
    'infrae.testbrowser',
    ]

setup(name=name,
      version=version,
      description="Composed form support for dolmen.forms",
      long_description=readme + '\n\n' + history,
      classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='Dolmen form composed',
      author='The Dolmen Team',
      author_email='dolmen@list.dolmen-project.org',
      url='http://pypi.python.org/pypi/dolmen.forms.composed',
      license='BSD',
      package_dir={'': 'src'},
      packages=find_packages('src'),
      namespace_packages=['dolmen', 'dolmen.forms'],
      include_package_data=True,
      zip_safe=False,
      tests_require=tests_require,
      install_requires=install_requires,
      extras_require={'test': tests_require},
      )
