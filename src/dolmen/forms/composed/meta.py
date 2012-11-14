# -*- coding: utf-8 -*-

import martian
import cromlech.browser
import grokcore.component as grok
from dolmen.forms.base.interfaces import IPrefixable, IForm
from dolmen.forms.composed.interfaces import ISubForm, ISubFormGroup
from dolmen.forms.composed.form import SubFormBase
from zope.component import provideAdapter
from zope.interface.interfaces import IInterface


def is_form_slot(value, default=ISubFormGroup):
    if IInterface.providedBy(value):
        if not value.isOrExtends(default):
            return False
    else:
        if not default.implementedBy(value):
            return False

    return True


def default_name(factory, module=None, **data):
    return factory.__name__.lower()


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

        assert is_form_slot(slot)

        adapts = (context, slot, request)
        config.action(
            discriminator=('adapter', adapts, ISubForm, name),
            callable=provideAdapter,
            args=(factory, adapts, ISubForm, name))

        return True
