# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import os

version = '0.1dev'

tests_require = [
    ]

setup(name='dolmen.forms.composed',
      version=version,
      description="Composed form support for dolmen.forms",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='Dolmen form composed',
      author='The Dolmen Team',
      author_email='thefunny@gmail.com',
      url='http://pypi.python.org/pypi/dolmen.forms.composed',
      license='BSD',
      package_dir={'': 'src'},
      packages=find_packages('src'),
      namespace_packages=['dolmen', 'dolmen.forms'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
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
      tests_require = tests_require,
      extras_require = {'test': tests_require},
      )
