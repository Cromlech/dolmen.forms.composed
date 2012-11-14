"""
We will define a composed form with some un-ordered subforms.

Let's grok our example:

  >>> from dolmen.forms.composed.testing import grok
  >>> grok('dolmen.forms.composed.ftests.forms.implicitorder')

We can now lookup our form by the name of its class:

  >>> from cromlech.browser.testing import TestRequest
  >>> request = TestRequest()

  >>> from dolmen.forms.composed.ftests.forms.implicitorder import Content
  >>> context = Content()

  >>> from zope import component
  >>> form = component.getMultiAdapter(
  ...     (context, request), name='form')
  >>> form
  <dolmen.forms.composed.ftests.forms.implicitorder.Form object at ...>

Our form have subforms, which are in order D, C, B, and A:

  >>> form.update()
  >>> form.subforms
  [<dolmen.forms.composed.ftests.forms.implicitorder.ASubForm object at ...>,
   <dolmen.forms.composed.ftests.forms.implicitorder.BSubForm object at ...>,
   <dolmen.forms.composed.ftests.forms.implicitorder.CSubForm object at ...>,
   <dolmen.forms.composed.ftests.forms.implicitorder.DSubForm object at ...>]

"""

from dolmen.forms import composed
from grokcore import component as grok


class Content(grok.Context):
    pass


class Form(composed.ComposedForm):
    label = u"Main form"


class ASubForm(composed.SubForm):
    composed.slot(Form)
    label = u"Sub Form A"


class BSubForm(composed.SubForm):
    composed.slot(Form)
    label = u"Sub Form B"


class CSubForm(composed.SubForm):
    composed.slot(Form)
    label = u"Sub Form C"


class DSubForm(composed.SubForm):
    composed.slot(Form)
    label = u"Sub Form D"
