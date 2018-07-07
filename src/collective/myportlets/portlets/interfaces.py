from plone.portlets.interfaces import IPortletDataProvider
from Products.CMFPlone import PloneMessageFactory as _
from zope import schema


class IRecentPortlet(IPortletDataProvider):
    count = schema.Int(title=_(u'Number of items to display'),
                       description=_(u'How many items to list.'),
                       required=True,
                       default=5)
