# -*- coding: utf-8 -*-

from cromlech.browser import ISlot
from dolmen.forms.base.interfaces import IForm, IFormCanvas, ISimpleFormCanvas
from zope.interface import Interface, Attribute


class ISubForm(IFormCanvas):
    """A form designed to be included in an another form.
    """
    parent = Attribute("Parent form")

    def available():
        """Return true if the form is available and should be
        rendered.
        """


class ISimpleSubForm(ISubForm, ISimpleFormCanvas):
    """A simple sub form.
    """


class ISubFormGroup(ISlot):
    """A group of subforms.
    """
    subforms = Attribute("List of available subforms")
    allSubforms = Attribute("List of all subforms")

    def getSubForm(id):
        """Return a subform based on its HTML identifier.
        """


class IComposedForm(ISubFormGroup, IForm):
    """A form which is composed of other forms.
    """
