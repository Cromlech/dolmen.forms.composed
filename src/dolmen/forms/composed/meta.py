# -*- coding: utf-8 -*-

import martian
import cromlech.browser
import grokcore.component

from dolmen.forms.composed.interfaces import ISubForm
from dolmen.forms.composed.form import SubFormBase
from dolmen.view.meta import default_view_name
from zope.component import provideAdapter


def set_form_prefix(subform, form, name):
    """Recursively set the form prefix (to be compatible with groups)
    """
    # We use __dict__.get not to look if prefix was set in a parent class.
    if not subform.__dict__.get('prefix'):
        if not form.prefix:
            set_form_prefix(
                form,
                cromlech.browser.view.bind().get(form),
                grokcore.component.name.bind(
                    get_default=cromlech.browser.default_view_name).get(form))
        subform.prefix = '%s.%s' % (form.prefix, name)


class SubFormGrokker(martian.ClassGrokker):
    """Grokker to register sub forms.
    """
    martian.component(SubFormBase)
    martian.directive(grokcore.component.context)
    martian.directive(
        cromlech.browser.request, default=cromlech.browser.IRequest)
    martian.directive(cromlech.browser.view)
    martian.directive(grokcore.component.name,
                      get_default=default_view_name)

    def grok(self, name, factory, module_info, **kw):
        factory.module_info = module_info
        return super(SubFormGrokker, self).grok(
            name, factory, module_info, **kw)

    def execute(self, factory, config, context, request, view, name, **kw):
        set_form_prefix(factory, view, name)

        adapts = (context, view, request)
        config.action(
            discriminator=('adapter', adapts, ISubForm, name),
            callable=provideAdapter,
            args=(factory, adapts, ISubForm, name))
        return True
