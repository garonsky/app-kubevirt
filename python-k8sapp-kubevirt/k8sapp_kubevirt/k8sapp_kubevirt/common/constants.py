#
# Copyright (c) 2022 Wind River Systems, Inc.
#
# SPDX-License-Identifier: Apache-2.0
#
# All Rights Reserved.
#

HELM_APP_KUBEVIRT = 'kubevirt'
HELM_APP_KUBEVIRT_CR = 'kubevirt.kubevirt.io/kubevirt'
HELM_APP_KUBEVIRT_CRD = 'kubevirts.kubevirt.io'
HELM_RELEASE_KUBEVIRT = 'kubevirt'
HELM_CHART_KUBEVIRT = 'kubevirt'
HELM_NS_KUBEVIRT = 'kubevirt'

HELM_APP_CDI = 'cdi'
HELM_APP_CDI_CR = 'cdi.cdi.kubevirt.io/cdi'
HELM_APP_CDI_CRD = 'cdis.cdi.kubevirt.io'
HELM_NS_CDI = 'cdi'
HELM_APP_CDI_UPLOAD_API_V1_ALPHA_1 = 'v1alpha1.upload.cdi.kubevirt.io'
HELM_APP_CDI_UPLOAD_API_V1_BETA_1 = 'v1beta1.upload.cdi.kubevirt.io'

HELM_VIRTCTL_DIR = '/var/opt/kubevirt/'
HELM_VIRTCTL_FILE_NAME = 'virtctl-v0.53.1-linux-amd64'
HELM_VIRTCTL_PATH = HELM_VIRTCTL_DIR + HELM_VIRTCTL_FILE_NAME
