#
# Copyright (c) 2022 Wind River Systems, Inc.
#
# SPDX-License-Identifier: Apache-2.0
#
# All Rights Reserved.
#

""" System inventory App lifecycle operator."""

import os

from k8sapp_kubevirt.common import constants as app_constants
from oslo_log import log as logging
from sysinv.common import constants
from sysinv.common import exception
from sysinv.common import kubernetes
from sysinv.common import utils as cutils
from sysinv.helm import lifecycle_base as base
from sysinv.helm.lifecycle_constants import LifecycleConstants


LOG = logging.getLogger(__name__)

class KubeVirtAppLifecycleOperator(base.AppLifecycleOperator):
    def app_lifecycle_actions(self, context, conductor_obj, app_op, app, hook_info):
        """Perform lifecycle actions for an operation

        :param context: request context, can be None
        :param conductor_obj: conductor object, can be None
        :param app_op: AppOperator object
        :param app: AppOperator.Application object
        :param hook_info: LifecycleHookInfo object

        """
        if hook_info.lifecycle_type == constants.APP_LIFECYCLE_TYPE_OPERATION:
            if hook_info.operation == constants.APP_REMOVE_OP:
                if hook_info.relative_timing == constants.APP_LIFECYCLE_TIMING_PRE:
                    return self.pre_remove(app)
                elif hook_info.relative_timing == constants.APP_LIFECYCLE_TIMING_POST:
                    return self.post_remove(app)

        super(KubeVirtAppLifecycleOperator, self).app_lifecycle_actions(
            context, conductor_obj, app_op, app, hook_info
        )

    def pre_remove(self, app):
        # Due to ordering of deletes, to prevent the namespace finalizer from waiting indefinitely,
        # we need to ensure that the kubevirt and cdi custom resource.

        LOG.debug(
            "Executing pre_remove for {} app".format(app_constants.HELM_APP_KUBEVIRT)
        )
        cmd = ['kubectl', '--kubeconfig', kubernetes.KUBERNETES_ADMIN_CONF,
               'delete', app_constants.HELM_APP_CDI_CR, '-n', app_constants.HELM_NS_CDI]
        stdout, stderr = cutils.trycmd(*cmd)
        LOG.debug("{} app: cmd={} stdout={} stderr={}".format(app.name, cmd, stdout, stderr))

        cmd = ['kubectl', '--kubeconfig', kubernetes.KUBERNETES_ADMIN_CONF,
               'delete', app_constants.HELM_APP_KUBEVIRT_CR, '-n', app_constants.HELM_NS_KUBEVIRT]
        stdout, stderr = cutils.trycmd(*cmd)
        LOG.debug("{} app: cmd={} stdout={} stderr={}".format(app.name, cmd, stdout, stderr))

    def post_remove(self, app):
        LOG.debug(
            "Executing post_remove for {} app".format(app_constants.HELM_APP_KUBEVIRT)
        )

        # Due to ordering of deletes, to prevent the namespace finalizer from waiting indefinitely,
        # we need to ensure we delete 2 APIs
        cmd = ['kubectl', '--kubeconfig', kubernetes.KUBERNETES_ADMIN_CONF,
               'delete', 'apiservices.apiregistration.k8s.io', app_constants.HELM_APP_CDI_UPLOAD_API_V1_ALPHA_1]
        stdout, stderr = cutils.trycmd(*cmd)
        LOG.debug("{} app: cmd={} stdout={} stderr={}".format(app.name, cmd, stdout, stderr))
 
        cmd = ['kubectl', '--kubeconfig', kubernetes.KUBERNETES_ADMIN_CONF,
               'delete', 'apiservices.apiregistration.k8s.io', app_constants.HELM_APP_CDI_UPLOAD_API_V1_BETA_1]
        stdout, stderr = cutils.trycmd(*cmd)
        LOG.debug("{} app: cmd={} stdout={} stderr={}".format(app.name, cmd, stdout, stderr))
       
        # Helm doesn't delete CRDs.  To clean up after application-remove, we need to explicitly delete the CRDs.
        cmd = ['kubectl', '--kubeconfig', kubernetes.KUBERNETES_ADMIN_CONF,
               'delete','crd',  app_constants.HELM_APP_CDI_CRD]
        stdout, stderr = cutils.trycmd(*cmd)
        LOG.debug("{} app: cmd={} stdout={} stderr={}".format(app.name, cmd, stdout, stderr))

        cmd = ['kubectl', '--kubeconfig', kubernetes.KUBERNETES_ADMIN_CONF,
               'delete','crd',  app_constants.HELM_APP_KUBEVIRT_CRD]
        stdout, stderr = cutils.trycmd(*cmd)
        LOG.debug("{} app: cmd={} stdout={} stderr={}".format(app.name, cmd, stdout, stderr))

        # Remove virtctl binary
        if os.path.exists(app_constants.HELM_VIRTCTL_PATH):
          os.remove(app_constants.HELM_VIRTCTL_PATH)
        else:
          LOG.warning("Failed to delete {}".format(app_constants.HELM_VIRTCTL_PATH))

        # Remove /var/opt/kubevirt if it is empty
        dir = os.listdir(app_constants.HELM_VIRTCTL_DIR)
        if len(dir) == 0:
          os.rmdir(app_constants.HELM_VIRTCTL_DIR)
          LOG.debug("Deleted directory {}".format(app_constants.HELM_VIRTCTL_DIR))
        else:
          LOG.warning("Directory {} is not empty - will not be deleted.".format(app_constants.HELM_VIRTCTL_DIR))
