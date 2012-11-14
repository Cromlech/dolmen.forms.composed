"""
We will define a composed form with two `groups` subforms. A group of
subforms is a logical ensemble of subforms, behaving like a single
subform. It is registered the same way as a SubForm.

Let's grok our example:

    >>> from dolmen.forms.composed.testing import grok
    >>> grok('dolmen.forms.composed.ftests.forms.group')

We can now lookup our form by the name of its class:

    >>> from cromlech.browser.testing import TestRequest
    >>> request = TestRequest()

    >>> animals = Animals()
    >>> animals.__name__ = 'animals'

    >>> from zope import component
    >>> form = component.getMultiAdapter(
    ...     (animals, request), name='zooform')
    >>> form
    <dolmen.forms.composed.ftests.forms.group.ZooForm object at ...>

The form should have the two groups as subforms, but it needs an
update first::

    >>> form.subforms is None
    True

    >>> form.update()

    >>> form.allSubforms
    [<dolmen.forms.composed.ftests.forms.group.Birds object at ...>,
     <dolmen.forms.composed.ftests.forms.group.Bears object at ...>]
    
    >>> form.subforms
    [<dolmen.forms.composed.ftests.forms.group.Birds object at ...>,
     <dolmen.forms.composed.ftests.forms.group.Bears object at ...>]

Each group is prefixed differently with the name of the form:

    >>> [s.prefix for s in form.subforms]
    ['form.birds', 'form.bears']

Each subform inside a group is prefixed with the name of the form and
the group::

    >>> for group in form.subforms:
    ...    [s.prefix for s in group.subforms]
    ['form.birds.blackbird', 'form.birds.eagle', 'form.birds.vulture']
    ['form.bears.firefox', 'form.bears.grizzly',
     'form.bears.scandinavianbears']

There a group embbedded in a group here, as we can mix groups and
subforms transparently. Let's verify that our subgroup subforms are
there ::

    >>> bears = form.getSubForm('form-bears')
    >>> subbears = bears.getSubForm('form-bears-scandinavianbears')
    >>> print subbears.subforms
    [<dolmen.forms.composed.ftests.forms.group.BrownBear object at ...>,
     <dolmen.forms.composed.ftests.forms.group.PolarBear object at ...>]


Integration tests
-----------------

  >>> from infrae.testbrowser.browser import Browser

  >>> app = makeApplication(animals, 'zooform')
  >>> browser = Browser(app)
  >>> browser.handleErrors = False


Empty submission
~~~~~~~~~~~~~~~~

We are going just to submit the form without giving any required
information, and we should get an error:

  >>> browser.open('http://localhost/animals/zooform')
  200

  >>> # print browser.contents

  >>> form = browser.get_form(id='form-bears-grizzly')
  >>> action = form.get_control('form.bears.grizzly.action.growl')
  >>> action.name, action.type
  ('form.bears.grizzly.action.growl', 'submit')

  >>> action.click()
  200
  >>> 'The Grizzly growled !' in browser.contents
  True

"""

from dolmen.forms import composed, base
from grokcore import component as grok
from cromlech.webob.response import Response


class Animals(grok.Context):
    pass


class ZooForm(composed.ComposedForm):
    label = u"A zoo form"
    responseFactory = Response


## Groups

class Birds(composed.SubFormGroup):
    composed.slot(ZooForm)
    composed.order(10)
    label = u"Birds Form"


class Bears(composed.SubFormGroup):
    composed.slot(ZooForm)
    composed.order(20)
    label = u"Bears form"


class ScandinavianBears(composed.SubFormGroup):
    composed.slot(Bears)
    composed.order(20)
    label = u"Scandinavian bears form"


## Sub forms

class Eagle(composed.SubForm):
    composed.slot(Birds)
    composed.order(20)
    actions = base.Actions(base.Action("Catch rabbit"))


class Blackbird(composed.SubForm):
    composed.slot(Birds)
    composed.order(10)
    actions = base.Actions(base.Action("Chirp"))


class Vulture(composed.SubForm):
    composed.slot(Birds)
    composed.order(30)
    fields = base.Fields(base.Field("Size"), base.Field("Weight"))
    actions = base.Actions(base.Action("Eat carcass"))


class Firefox(composed.SubForm):
    composed.slot(Bears)
    composed.order(10)
    actions = base.Actions(base.Action("Eat bamboo"))


class Grizzly(composed.SubForm):
    composed.slot(Bears)
    composed.order(12)

    fields = base.Fields(base.Field("Name"), base.Field("Gender"))

    @base.action(u"Growl")
    def register(self):
        data, errors = self.extractData()
        if errors:
            return

        # In case of success we don't keep request value in the form
        self.ignoreRequest = True
        self.status = u"The Grizzly growled !"


class BrownBear(composed.SubForm):
    composed.slot(ScandinavianBears)
    composed.order(0)
    fields = base.Fields(base.Field("Name"), base.Field("Age"))
    actions = base.Actions(base.Action("Play in pool"))


class PolarBear(composed.SubForm):
    composed.slot(ScandinavianBears)
    composed.order(1)
    actions = base.Actions(base.Action("Eat seal"))
