"""
We will define a composed form with two subforms.

Let's grok our example:

  >>> from dolmen.forms.composed.testing import grok
  >>> grok('dolmen.forms.composed.ftests.forms.composed')

We can now lookup our form by the name of its class:

  >>> from cromlech.browser.testing import TestRequest
  >>> request = TestRequest()

  >>> from dolmen.forms.composed.ftests.forms.composed import Content
  >>> context = Content()

  >>> from zope import component
  >>> form = component.getMultiAdapter(
  ...     (context, request), name='complexform')
  >>> form
  <dolmen.forms.composed.ftests.forms.composed.ComplexForm object at ...>

Our form have subforms:

  >>> form.update()
  >>> form.subforms
  [<dolmen.forms.composed.ftests.forms.composed.Hello object at ...>,
   <dolmen.forms.composed.ftests.forms.composed.ByeBye object at ...>]

Each sub form is prefixed differently with the name of the form:

  >>> [s.prefix for s in form.subforms]
  ['form.hello', 'form.byebye']

And we can render the form:

  >>> from cromlech.browser.testing import XMLDiff

  >>> rendered = str(form())
  >>> print XMLDiff(rendered, expected_sub)
  None

We add some errors to the form:

  >>> from dolmen.forms.base.errors import Error
  >>> form = component.getMultiAdapter(
  ...     (context, request), name='complexform')

  >>> form.formErrors

  >>> form.errors.append(Error(u'Something is wrong', identifier=form.prefix))
  >>> len(form.formErrors)
  1

  >>> rendered = str(form())
  >>> print XMLDiff(rendered, expected_error)
  None

"""

from dolmen.forms import composed, base
from grokcore import component as grok
from cromlech.webob.response import Response


class Content(grok.Context):
    pass


class ComplexForm(composed.ComposedForm):
    label = u"Complex form"
    responseFactory = Response


class Hello(composed.SubForm):
    composed.slot(ComplexForm)
    composed.order(10)

    label = u"Hello Form"
    actions = base.Actions(base.Action("Hello"))


class ByeBye(composed.SubForm):
    composed.slot(ComplexForm)
    composed.order(20)

    label = u"Bye Bye Form"
    actions = base.Actions(base.Action("Bye Bye"))


expected_sub = """
  <html>
    <head>
    </head>
    <body>
        <h1>Complex form</h1>
        <div class="subforms">
          <div class="subform"><form action="." method="post"
          enctype="multipart/form-data" id="form-hello">
            <h2>Hello Form</h2>
            <div class="actions">
              <div class="action">
                <input type="submit" id="form-hello-action-hello"
                name="form.hello.action.hello" value="Hello" class="action" />
              </div>
            </div>
          </form></div> <div class="subform"><form action="."
          method="post" enctype="multipart/form-data" id="form-byebye">
          <h2>Bye Bye Form</h2>
          <div class="actions">
            <div class="action">
               <input type="submit" id="form-byebye-action-bye-bye"
               name="form.byebye.action.bye-bye" value="Bye Bye"
               class="action" />
            </div>
          </div>
        </form></div>
      </div>
    </body>
  </html>"""

expected_error = """
  <html>
    <head>
    </head>
    <body>
        <h1>Complex form</h1>
        <div class="form-error">
            <ul>
              <li> Something is wrong </li>
            </ul>
        </div>
        <div class="subforms">
          <div class="subform"><form action="." method="post"
          enctype="multipart/form-data" id="form-hello">
            <h2>Hello Form</h2>
            <div class="actions">
              <div class="action">
                <input type="submit" id="form-hello-action-hello"
                name="form.hello.action.hello" value="Hello"
                class="action" />
              </div>
            </div>
          </form></div> <div class="subform"><form action="."
          method="post" enctype="multipart/form-data" id="form-byebye">
          <h2>Bye Bye Form</h2>
          <div class="actions">
            <div class="action">
              <input type="submit" id="form-byebye-action-bye-bye"
              name="form.byebye.action.bye-bye" value="Bye Bye"
              class="action" />
            </div>
          </div>
        </form></div>
      </div>
    </body>
  </html>"""
