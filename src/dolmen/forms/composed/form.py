# -*- coding: utf-8 -*-

from cromlech.browser import IRenderable, IRequest
from dolmen.template import ITemplate, TALTemplate
from dolmen.forms.base import Form, FormCanvas
from dolmen.forms.base.errors import Errors
from dolmen.forms.base.interfaces import IPrefixable
from dolmen.forms.composed.interfaces import (
    ISubFormGroup, ISubForm, ISimpleSubForm, IComposedForm)

from grokcore.component.util import sort_components
from grokcore.component import baseclass, adapter, implementer

from zope.component import getAdapters, getMultiAdapter
from zope.interface import implements, Interface

try:
    import zope.security

    def check_security(component, attribute):
        try:
            return zope.security.canAccess(component, attribute)
        except zope.security.interfaces.Forbidden:
            return False

    CHECKER = check_security
    PROXY = zope.security.checker.ProxyFactory
except ImportError:
    CHECKER = None
    PROXY = None


def query_subforms(context, request, form, interface=ISubForm):
    """Query subforms of the given form :

    * Queries the registry according to context, request, form.
    * Updates the components.
    * Returns an iterable of components.
    """

    def registry_components():
        for name, component in getAdapters(
            (context, form, request), interface):

            if CHECKER is not None and not CHECKER(component, 'render'):
                continue

            component.update()
            yield component

    assert interface.isOrExtends(ISubForm), "interface must extends ISubForm"
    assert IRequest.providedBy(request), "request must be an IRequest"
    return registry_components()


def set_prefix(parent, base):
    prefixable = IPrefixable(parent, None)
    if prefixable is not None:
        return '%s.%s' % (prefixable.prefix, base)
    return base
    

class SubFormBase(object):
    """Base class to be applied on a FormCanvas to get a subform.
    """
    baseclass()

    label = u''
    description = u''
    prefix = None

    def __init__(self, context, parent, request):
        super(SubFormBase, self).__init__(context, request)
        self.parent = parent

    @property
    def base_prefix(self):
        return self.__class__.__name__.lower()

    def update(self):
        if self.prefix is None:
            self.prefix = set_prefix(self.parent, self.base_prefix)

    def available(self):
        return True

    def htmlId(self):
        return self.prefix.replace('.', '-')

    def getComposedForm(self):
        return self.parent.getComposedForm()


class SubFormGroupBase(object):
    """A group of subforms: they can be grouped inside a composed form.
    """
    implements(ISubFormGroup)

    subforms = None
    allSubforms = None
    prefix = None

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.errors = Errors()

    @property
    def base_prefix(self):
        return self.__class__.__name__.lower()

    def update(self):

        self.allSubforms = sort_components(
            query_subforms(self.context, self.request, self))

        self.subforms = filter(lambda f: f.available(), self.allSubforms)

        # set the prefix
        if self.prefix is None:
            self.prefix = set_prefix(self.parent, self.base_prefix)

    def getSubForm(self, identifier):
        for form in self.subforms:
            if form.htmlId() == identifier:
                return form
        return None

    def getComposedForm(self):
        return self

    def htmlId(self):
        return self.prefix.replace('.', '-')

    def namespace(self):
        namespace = FormCanvas.namespace(self)
        namespace['form'] = self
        return namespace

    def updateActions(self):
        # Set/run actions for all forms
        action, status = None, None
        for subform in self.subforms:
            action, status = subform.updateActions()
            if action is not None:
                break

        # The result of the actions might have changed the available subforms
        self.subforms = filter(lambda f: f.available(), self.allSubforms)
        return action, status

    def updateWidgets(self):
        # Set widgets for all forms
        for subform in self.subforms:
            subform.updateWidgets()


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

    @property
    def template(self):
        return getMultiAdapter((self, self.request), ITemplate)

    def render(self, *args, **kwargs):
        namespace = self.namespace()
        return self.template.render(self, target_language=None, **namespace)


class SubFormGroup(SubFormBase, SubFormGroupBase):
    """A group of subforms.
    """
    baseclass()
    implements(ISubForm)

    def update(self, *args, **kwargs):
        SubFormBase.update(self)
        SubFormGroupBase.update(self, *args, **kwargs)

    def available(self):
        # This should be computed AFTER an update
        return bool(self.subforms and len(self.subforms) != 0)

    def namespace(self):
        return dict(
            context=self.context,
            request=self.request,
            form=self,
            subforms=self.subforms)

    @property
    def template(self):
        return getMultiAdapter((self, self.request), ITemplate)

    def render(self, *args, **kwargs):
        namespace = self.namespace()
        return self.template.render(self, target_language=None, **namespace)


class ComposedForm(SubFormGroupBase, Form):
    """A form which is composed of other forms (SubForm).
    """
    baseclass()
    implements(IComposedForm)

    prefix = 'form'

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

        for subform in self.subforms:
            for error in subform.errors:
                self.errors.append(error)

    @property
    def template(self):
        return getMultiAdapter((self, self.request), ITemplate)

    def render(self, *args, **kwargs):
        namespace = self.namespace()
        return self.template.render(self, target_language=None, **namespace)


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
