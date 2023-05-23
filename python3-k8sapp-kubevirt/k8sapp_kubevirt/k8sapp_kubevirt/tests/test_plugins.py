#
# Copyright (c) 2023 Wind River Systems, Inc.
#
# SPDX-License-Identifier: Apache-2.0
#
"""Module provides high-level plugin test framework."""

from sysinv.tests.db import base as dbbase

from k8sapp_kubevirt.common import constants as app_constants


# pylint: disable=useless-object-inheritance
class K8SAppKubevirtAppMixin(object):
    """Class for specific plugin testcases."""

    app_name = app_constants.HELM_APP_KUBEVIRT
    path_name = app_name + '.tgz'

    # pylint: disable=invalid-name,useless-parent-delegation
    def setUp(self):
        """Setup test cases."""
        super().setUp()

    def test_stub(self):
        """Test Case Stub."""
        # Replace this with a real unit test.


# Test Configuration:
# - Controller
# - IPv6
# - Ceph Storage
# - kubevirt app

# pylint: disable=too-many-ancestors
class K8sAppKubevirtControllerTestCase(K8SAppKubevirtAppMixin,
                                       dbbase.BaseIPv6Mixin,
                                       dbbase.BaseCephStorageBackendMixin,
                                       dbbase.ControllerHostTestCase):
    """Class to test IPv6 Standard w/Ceph."""


# Test Configuration:
# - AIO
# - IPv4
# - Ceph Storage
# - kubevirt app
# pylint: disable=too-many-ancestors
class K8SAppKubevirtAIOTestCase(K8SAppKubevirtAppMixin,
                                dbbase.BaseCephStorageBackendMixin,
                                dbbase.AIOSimplexHostTestCase):
    """Class to test IPv4 AIO w/Ceph."""
