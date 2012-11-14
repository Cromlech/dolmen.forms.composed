# -*- coding: utf-8 -*-

import martian
import cromlech.browser
import grokcore.component as grok
from dolmen.forms.base.interfaces import IPrefixable, IFormCanvas
from dolmen.forms.composed.interfaces import ISubForm
from dolmen.forms.composed.form import SubFormBase
from zope.component import provideAdapter


def default_name(factory, module=None, **data):
    return factory.__name__.lower()


def set_form_prefix(subform, form, name):
    """Recursively set the form prefix (to be compatible with groups)
    """
    prefixable = IPrefixable(form, None)
    assert prefixable is not None

    if not prefixable.prefix:
        set_form_prefix(
            form,
            cromlech.browser.slot.bind().get(form),
            grok.name.bind(get_default=default_name).get(form))
    subform.prefix = '%s.%s' % (form.prefix, name)


class SubFormGrokker(martian.ClassGrokker):
    """Grokker to register sub forms.
    """
    martian.component(SubFormBase)
    martian.directive(grok.context)
    martian.directive(grok.name, get_default=default_name)
    martian.directive(cromlech.browser.request)
    martian.directive(cromlech.browser.slot)

    def grok(self, name, factory, module_info, **kw):
        factory.module_info = module_info
        return super(SubFormGrokker, self).grok(
            name, factory, module_info, **kw)

    def execute(self, factory, config, context, request, slot, name, **kw):

        assert IFormCanvas.providedBy(slot)

        set_form_prefix(factory, slot, name)

        adapts = (context, slot, request)
        config.action(
            discriminator=('adapter', adapts, ISubForm, name),
            callable=provideAdapter,
            args=(factory, adapts, ISubForm, name))
        return True
