"""
We will define a composed form with some ordered subforms.

Let's grok our example:

  >>> from dolmen.forms.composed.testing import grok
  >>> grok('dolmen.forms.composed.ftests.forms.explicitorder')

We can now lookup our form by the name of its class:

  >>> from cromlech.browser.testing import TestRequest
  >>> request = TestRequest()

  >>> from dolmen.forms.composed.ftests.forms.explicitorder import Content
  >>> context = Content()

  >>> from zope import component
  >>> form = component.getMultiAdapter(
  ...     (context, request), name='form')
  >>> form
  <dolmen.forms.composed.ftests.forms.explicitorder.Form object at ...>

Our form have subforms, which are in order D, C, B, and A, because we
used the order directive:

  >>> form.update()
  >>> form.subforms
  [<dolmen.forms.composed.ftests.forms.explicitorder.DSubForm object at ...>,
   <dolmen.forms.composed.ftests.forms.explicitorder.CSubForm object at ...>,
   <dolmen.forms.composed.ftests.forms.explicitorder.BSubForm object at ...>,
   <dolmen.forms.composed.ftests.forms.explicitorder.ASubForm object at ...>]

"""

from dolmen.forms import composed
from grokcore import component as grok


class Content(grok.Context):
    pass


class Form(composed.ComposedForm):
    label = u"Main form"


class ASubForm(composed.SubForm):
    composed.slot(Form)
    composed.order(20)
    label = u"Sub Form A"


class CSubForm(composed.SubForm):
    composed.slot(Form)
    composed.order(10)
    label = u"Sub Form C"


class DSubForm(composed.SubForm):
    composed.slot(Form)
    composed.order(0)
    label = u"Sub Form D"


class BSubForm(composed.SubForm):
    composed.slot(Form)
    composed.order(15)
    label = u"Sub Form B"
