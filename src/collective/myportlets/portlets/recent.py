from collective.myportlets.portlets.interfaces import IRecentPortlet
from plone.app.portlets.portlets import base
from z3c.form import field
from zope.interface import implements
from Products.CMFPlone import PloneMessageFactory as _
from plone.memoize.instance import memoize
from zope.component import getMultiAdapter
from Acquisition import aq_inner
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class Assignment(base.Assignment):
    implements(IRecentPortlet)

    def __init__(self, count=5):
        self.count = count

    @property
    def title(self):
        return _(u"Recent items")


class AddForm(base.AddForm):
    form_fields = field.Fields(IRecentPortlet)
    label = _(u"Add Recent Portlet")
    description = _(u"This portlet displays recently modified content.")

    def create(self, data):
        return Assignment(count=data.get('count', 5))


class EditForm(base.EditForm):
    form_fields = field.Fields(IRecentPortlet)
    label = _(u"Edit Recent Portlet")
    description = _(u"This portlet displays recently modified content.")


class Renderer(base.Renderer):
    _template = ViewPageTemplateFile('recent.pt')

    def __init__(self, *args):
        base.Renderer.__init__(self, *args)

        context = aq_inner(self.context)
        portal_state = getMultiAdapter((context, self.request), name=u'plone_portal_state')
        self.anonymous = portal_state.anonymous()  # whether or not the current user is Anonymous
        self.portal_url = portal_state.portal_url()  # the URL of the portal object

        # a list of portal types considered "end user" types
        self.typesToShow = portal_state.friendly_types()

        plone_tools = getMultiAdapter((context, self.request), name=u'plone_tools')
        self.catalog = plone_tools.catalog()

    def render(self):
        return self._template()

    @property
    def available(self):
        """Show the portlet only if there are one or more elements."""
        return not self.anonymous and len(self._data())

    def recent_items(self):
        return self._data()

    def recently_modified_link(self):
        return '%s/recently_modified' % self.portal_url

    @memoize
    def _data(self):
        limit = self.data.count
        return self.catalog(portal_type=self.typesToShow,
                            sort_on='modified',
                            sort_order='reverse',
                            sort_limit=limit)[:limit]
