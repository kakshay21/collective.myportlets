# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import collective.myportlets


class CollectiveMyportletsLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=collective.myportlets)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.myportlets:default')


COLLECTIVE_MYPORTLETS_FIXTURE = CollectiveMyportletsLayer()


COLLECTIVE_MYPORTLETS_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_MYPORTLETS_FIXTURE,),
    name='CollectiveMyportletsLayer:IntegrationTesting',
)


COLLECTIVE_MYPORTLETS_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_MYPORTLETS_FIXTURE,),
    name='CollectiveMyportletsLayer:FunctionalTesting',
)


COLLECTIVE_MYPORTLETS_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        COLLECTIVE_MYPORTLETS_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='CollectiveMyportletsLayer:AcceptanceTesting',
)
