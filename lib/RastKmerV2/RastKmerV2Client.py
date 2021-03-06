# -*- coding: utf-8 -*-
############################################################
#
# Autogenerated by the KBase type compiler -
# any changes made here will be overwritten
#
############################################################

from __future__ import print_function
# the following is a hack to get the baseclient to import whether we're in a
# package or not. This makes pep8 unhappy hence the annotations.
try:
    # baseclient and this client are in a package
    from .baseclient import BaseClient as _BaseClient  # @UnusedImport
except:
    # no they aren't
    from baseclient import BaseClient as _BaseClient  # @Reimport


class RastKmerV2(object):

    def __init__(
            self, url=None, timeout=30 * 60, user_id=None,
            password=None, token=None, ignore_authrc=False,
            trust_all_ssl_certificates=False,
            auth_svc='https://kbase.us/services/authorization/Sessions/Login'):
        if url is None:
            raise ValueError('A url is required')
        self._service_ver = None
        self._client = _BaseClient(
            url, timeout=timeout, user_id=user_id, password=password,
            token=token, ignore_authrc=ignore_authrc,
            trust_all_ssl_certificates=trust_all_ssl_certificates,
            auth_svc=auth_svc)

    def annotate_genes(self, params, context=None):
        """
        :param params: instance of type "AnnotateGenesParams" -> structure:
           parameter "input_genome_ref" of String, parameter
           "output_workspace" of String, parameter "output_genome_name" of
           String
        """
        return self._client.call_method(
            'RastKmerV2.annotate_genes',
            [params], self._service_ver, context)

    def status(self, context=None):
        return self._client.call_method('RastKmerV2.status',
                                        [], self._service_ver, context)
