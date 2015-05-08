# -*- coding: utf-8 -*-
from collective.nitf.testing import INTEGRATION_TESTING
from plone import api

try:
    from Products.CMFPlone.interfaces.syndication import IFeed
except ImportError:  # 4.2
    from collective.syndication.interfaces import IFeed

import unittest2 as unittest


class NitfItemTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = api.portal.get()
        with api.env.adopt_roles(['Manager']):
            self.folder = api.content.create(
                type='Folder',
                title='test-folder',
                container=self.portal
            )
            self.n1 = api.content.create(
                type='collective.nitf.content',
                title='n1',
                container=self.folder
            )

    def test_adapter(self):
        self.n1.byline = 'The Author'
        adapted_folder = IFeed(self.folder)
        adapted_n1 = adapted_folder.items.next()
        self.assertEqual(adapted_n1.author_name, 'The Author')
