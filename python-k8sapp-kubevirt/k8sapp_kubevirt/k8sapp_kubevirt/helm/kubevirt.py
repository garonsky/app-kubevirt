# Copyright (c) 2022 Wind River Systems, Inc.
#
# SPDX-License-Identifier: Apache-2.0
#
from k8sapp_kubevirt.common import constants as app_constants
from sysinv.common import exception
from sysinv.common import utils
from sysinv.helm import base
from oslo_log import log as logging
from sysinv.db import api as dbapi

LOG = logging.getLogger(__name__)

class KubeVirtHelm(base.FluxCDBaseHelm):
    """Class to encapsulate helm operations for the kubevirt chart"""

    CHART = app_constants.HELM_CHART_KUBEVIRT
    HELM_RELEASE = app_constants.HELM_RELEASE_KUBEVIRT
    SERVICE_NAME = 'kubevirt'


    SUPPORTED_NAMESPACES = base.BaseHelm.SUPPORTED_NAMESPACES + \
        [app_constants.HELM_NS_KUBEVIRT] + [app_constants.HELM_NS_CDI]

    SUPPORTED_APP_NAMESPACES = {
        app_constants.HELM_APP_KUBEVIRT:
            base.BaseHelm.SUPPORTED_NAMESPACES + [app_constants.HELM_NS_KUBEVIRT] + [app_constants.HELM_NS_CDI],
    }

    def get_namespaces(self):
        return self.SUPPORTED_NAMESPACES

    def get_overrides(self, namespace=None):
        overrides = {
            app_constants.HELM_NS_KUBEVIRT: {
                'featureGates': ['Snapshot'],
                'useEmulation': utils.is_virtual(),
                'replicas': '1' if utils.is_single_controller(dbapi.get_instance()) else '2'
            }
        }

        if namespace in self.SUPPORTED_NAMESPACES:
            return overrides[namespace]
        elif namespace:
            raise exception.InvalidHelmNamespace(chart=self.CHART,
                                                 namespace=namespace)
        else:
            return overrides
