#
# Copyright (c) 2023 Wind River Systems, Inc.
#
# SPDX-License-Identifier: Apache-2.0
#
"""Module for application testing."""

from sysinv.db import api as dbapi
from sysinv.tests.db import base as dbbase
from sysinv.tests.db import utils as dbutils
from sysinv.tests.helm import base

from k8sapp_kubevirt.tests import test_plugins


class KubevirtTestCase(test_plugins.K8SAppKubevirtAppMixin,
                       base.HelmTestCaseMixin):
    """Base Test Case Class."""

    def setUp(self):
        """Common Test Case Setup."""
        super().setUp()
        self.app = dbutils.create_test_app(name='kubevirt')
        self.dbapi = dbapi.get_instance()


# pylint: disable=too-many-ancestors
class KubevirtTestCaseDummy(KubevirtTestCase,
                            dbbase.ProvisionedControllerHostTestCase):
    """Dummy Test Case Class"""

    def test_dummy(self):
        """Dummy Test Case."""
        # without a test zuul will fail
