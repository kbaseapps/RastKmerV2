# -*- coding: utf-8 -*-
import unittest
import os  # noqa: F401
import json  # noqa: F401
import time
import requests

from os import environ
import shutil
try:
    from ConfigParser import ConfigParser  # py2
except:
    from configparser import ConfigParser  # py3

from pprint import pprint  # noqa: F401

from biokbase.workspace.client import Workspace as workspaceService
from RastKmerV2.RastKmerV2Impl import RastKmerV2
from RastKmerV2.RastKmerV2Server import MethodContext

from GenomeFileUtil.GenomeFileUtilClient import GenomeFileUtil


class RastKmerV2Test(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        token = environ.get('KB_AUTH_TOKEN', None)
        user_id = requests.post(
            'https://kbase.us/services/authorization/Sessions/Login',
            data='token={}&fields=user_id'.format(token)).json()['user_id']
        # WARNING: don't call any logging methods on the context object,
        # it'll result in a NoneType error
        cls.ctx = MethodContext(None)
        cls.ctx.update({'token': token,
                        'user_id': user_id,
                        'provenance': [
                            {'service': 'RastKmerV2',
                             'method': 'please_never_use_it_in_production',
                             'method_params': []
                             }],
                        'authenticated': 1})
        config_file = environ.get('KB_DEPLOYMENT_CONFIG', None)
        cls.cfg = {}
        config = ConfigParser()
        config.read(config_file)
        for nameval in config.items('RastKmerV2'):
            cls.cfg[nameval[0]] = nameval[1]
        cls.wsURL = cls.cfg['workspace-url']
        cls.wsClient = workspaceService(cls.wsURL, token=token)
        cls.serviceImpl = RastKmerV2(cls.cfg)

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'wsName'):
            cls.wsClient.delete_workspace({'workspace': cls.wsName})
            print('Test workspace was deleted')

    def getWsClient(self):
        return self.__class__.wsClient

    def getWsName(self):
        if hasattr(self.__class__, 'wsName'):
            return self.__class__.wsName
        suffix = int(time.time() * 1000)
        wsName = "test_RastKmerV2_" + str(suffix)
        ret = self.getWsClient().create_workspace({'workspace': wsName})  # noqa
        self.__class__.wsName = wsName
        return wsName

    def getImpl(self):
        return self.__class__.serviceImpl

    def getContext(self):
        return self.__class__.ctx

    # NOTE: According to Python unittest naming rules test method names should start from 'test'. # noqa
    def test_annotate_genes(self):
        gbk_file = "/kb/module/test/data/kb_g.399.c.1.gbk.gz"
        temp_gbk = "/kb/module/work/tmp/kb_g.399.c.1.gbk.gz"
        shutil.copy(gbk_file, temp_gbk)
        genome_obj = "Genome.1"
        gfu = GenomeFileUtil(os.environ['SDK_CALLBACK_URL'], token=self.getContext()['token'])
        gfu.genbank_to_genome({'file': {'path': temp_gbk}, 'workspace_name': self.getWsName(),
                               'genome_name': genome_obj})
        genome_ref = self.getWsName() + '/' + genome_obj
        self.getImpl().annotate_genes(self.getContext(), {'input_genome_ref': genome_ref,
                                                          'output_workspace': self.getWsName(),
                                                          'output_genome_name': genome_obj})
        # kmer_guts -m 5 -g 200 -D /data/kmer/V2Data/ -a | km_process_hits_to_regions -a -d /data/kmer/V2Data/  | km_pick_best_hit_in_peg
