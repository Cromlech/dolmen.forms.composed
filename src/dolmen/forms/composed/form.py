# -*- coding: utf-8 -*-

from dolmen.template import ITemplate, TALTemplate
from dolmen.forms.base import Fields, Form, FormCanvas
from dolmen.forms.composed.interfaces import (
    ISubFormGroup, ISubForm, ISimpleSubForm, IComposedForm)

from grokcore.component.util import sort_components
from grokcore.component import baseclass, adapter, implementer

from zope.component import getAdapters, getMultiAdapter
from zope.interface import implements, Interface


class SubFormBase(object):
    """Base class to be applied on a FormCanvas to get a subform.
    """
    baseclass()

    # Set prefix to None, so it's changed by the grokker
    label = u''
    description = u''
    prefix = None

    def __init__(self, context, parent, request):
        super(SubFormBase, self).__init__(context, request)
        self.parent = parent

    @property
    def template(self):
        return getMultiAdapter((self, self.request), ITemplate)

    def available(self):
        return True

    def htmlId(self):
        return self.prefix.replace('.', '-')

    def getComposedForm(self):
        return self.parent.getComposedForm()

    def render(self, *args, **kwargs):
        return self.template.render(self)


class SubFormGroupBase(object):
    """A group of subforms: they can be grouped inside a composed form.
    """
    implements(ISubFormGroup)

    def __init__(self, context, request):
        self.context = context
        self.request = request

        # retrieve subforms by adaptation
        subforms = map(lambda f: f[1], getAdapters(
                (self.context, self,  self.request), ISubForm))

        # sort them
        self.allSubforms = sort_components(subforms)
        self.subforms = self._getAvailableSubForms()

    @property
    def template(self):
        return getMultiAdapter((self, self.request), ITemplate)

    def getSubForm(self, identifier):
        for form in self.subforms:
            if form.htmlId() == identifier:
                return form
        return None

    def getComposedForm(self):
        return self

    def htmlId(self):
        return self.prefix.replace('.', '-')

    def update(self):
        # Call update for all forms
        for subform in self.allSubforms:
            subform.update()

    def updateActions(self):
        # Set/run actions for all forms
        action, status = None, None
        for subform in self._getAvailableSubForms():
            action, status = subform.updateActions()
            if action is not None:
                break
        # The result of the actions might have changed the available subforms
        self.subforms = self._getAvailableSubForms()
        return action, status

    def updateWidgets(self):
        # Set widgets for all forms
        for subform in self._getAvailableSubForms():
            subform.updateWidgets()

    def _getAvailableSubForms(self):
        # filter out unavailables ones
        return filter(lambda f: f.available(), self.allSubforms)

    def render(self, *args, **kwargs):
        return self.template.render(self)


class SubForm(SubFormBase, FormCanvas):
    """Form designed to be included in an another form (a
    ComposedForm).
    """
    baseclass()
    implements(ISimpleSubForm)

    def namespace(self):
        namespace = FormCanvas.namespace(self)
        namespace['form'] = self
        return namespace


class SubFormGroup(SubFormBase, SubFormGroupBase):
    """A group of subforms.
    """
    baseclass()
    implements(ISubForm)

    def namespace(self):
        namespace = {}
        namespace['context'] = self.context
        namespace['request'] = self.request
        namespace['form'] = self
        namespace['subforms'] = self.subforms
        return namespace

    def available(self):
        return len(self.subforms) != 0


class ComposedForm(SubFormGroupBase, Form):
    """A form which is composed of other forms (SubForm).
    """
    baseclass()
    implements(IComposedForm)

    def __init__(self, context, request):
        SubFormGroupBase.__init__(self, context, request)
        Form.__init__(self, context, request)
        
    def update(self, *args, **kwargs):
        SubFormGroupBase.update(self)
        Form.update(self, *args, **kwargs)

    def updateForm(self):
        action, status = SubFormGroupBase.updateActions(self)
        if action is None:
            Form.updateActions(self)
        SubFormGroupBase.updateWidgets(self)
        Form.updateWidgets(self)


# Templates
import os.path

PATH = os.path.join(os.path.dirname(__file__), 'templates')

@implementer(ITemplate)
@adapter(SubForm, Interface)
def subform_template(form, request):    
    return TALTemplate(os.path.join(PATH, 'subform.pt'))


@implementer(ITemplate)
@adapter(ComposedForm, Interface)
def composedform_template(form, request):
    return TALTemplate(os.path.join(PATH, 'composedform.pt'))


@implementer(ITemplate)
@adapter(SubFormGroup, Interface)
def subformgroup_template(form, request):
    return TALTemplate(os.path.join(PATH, 'subformgroup.pt'))
