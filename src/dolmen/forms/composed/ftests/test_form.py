# -*- coding: utf-8 -*-

import cromlech.webob.request
import doctest
import dolmen.forms.composed
import unittest
import webob.dec

from cromlech.io.interfaces import IPublicationRoot
from pkg_resources import resource_listdir
from zope.component import getMultiAdapter
from zope.component.testlayer import LayerBase
from zope.interface import Interface, directlyProvides
from zope.location import Location


class WSGIApplication(object):

    def __init__(self, context, formname):
        self.context = context
        self.formname = formname

    @webob.dec.wsgify(RequestClass=cromlech.webob.request.Request)
    def __call__(self, req):
        form = getMultiAdapter((self.context, req), Interface, self.formname)
        return form()


class BrowserLayer(LayerBase):
    """A test layer.
    """
    def makeApplication(self, context, formname):
        root = Location()
        directlyProvides(root, IPublicationRoot)
        context.__parent__ = root
        if getattr(context, '__name__', None) is None:
            context.__name__ = 'content'
        return WSGIApplication(context, formname)


FunctionalLayer = BrowserLayer(dolmen.forms.base)


def suiteFromPackage(name):
    optionflags = (
        doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS |doctest.REPORT_NDIFF)
    globs = {'makeApplication': FunctionalLayer.makeApplication}
    files = resource_listdir(__name__, name)
    suite = unittest.TestSuite()

    for filename in files:
        if not filename.endswith('.py'):
            continue
        if filename.endswith('_fixture.py'):
            continue
        if filename == '__init__.py':
            continue

        dottedname = 'dolmen.forms.composed.ftests.%s.%s' % (
            name, filename[:-3])
        test = doctest.DocTestSuite(
            dottedname, extraglobs=globs, optionflags=optionflags)
        test.layer = FunctionalLayer
        suite.addTest(test)
    return suite


def test_suite():
    suite = unittest.TestSuite()
    for name in ['forms', ]:
        suite.addTest(suiteFromPackage(name))
    return suite
