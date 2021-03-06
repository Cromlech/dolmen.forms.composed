=========================
dolmen.forms.composed
=========================

This package let you defines forms containing other forms in
`dolmen.forms.base`_.

.. contents::

Example
=======

Here a simple example. Let's define a setting form::

  from dolmen.forms import composed, base
  from zope.interface import Interface


  class Setting(composed.ComposedForm):
      composed.context(Interface)

      label = u"Settings"


After, a module can add some mail settings on that screen::

  class MailSetting(composed.SubForm):
      composed.context(MyApplication)
      composed.slot(Setting)
      composed.order(99)

      label = u"Mail delivery settings"
      ...

And publications of that application could add some publication
settings::

  class PublicationSetting(composed.SubForm):
      composed.context(MyPublications)
      composed.slot(Setting)
      composed.order(10)

      label = u"Publication settings"
      ...


Some default templates are included as well, but you can replace like
you will do in `dolmen.forms.base`_.

API
===

Classes
-------

``ComposedForm``
    This class define a form which able to contain other forms. It
    behave like a ``dolmen.forms.base`` Form, but does use its fields.
    A usefull method can give you back a given subform :
    ``getSubForm(identifier)``.

``SubForm``
    This class represent a form which is contained inside a
    ``ComposedForm``. This form behave exactly like a
    ``dolmen.forms.base`` Form to which you add:

    - a method ``available()`` which is called before anything else to
      know if the form shoud still be included in the ``ComposedForm``.

    - a method ``getComposedForm()`` that gives you back the composed
      form in which this form is rendered.

``SubFormGroup``
    This class let you group ``SubForm`` together. They are rendered within
    the group template, and prefixed by the group name. Like a ``SubForm``
    they have an ``available()`` and a ``getComposedForm()`` method. It as
    well have a ``getSubForm(identifier)`` method.

Directives
----------

All those directives comes from Grokcore component. Please refer to
the `Grok documentation <http://grok.zope.org>`_ for more information.

``context``
    Define for which object the form/sub form is available.

``require``
    Define a permission need to access the form.

``slot``
    On a sub form, define for which group form the sub form is available.

``order``
    Let you specify a number to sort your sub form afterwards using
    that setting.

.. _dolmen.forms.base: http://pypi.python.org/pypi/dolmen.forms.base
