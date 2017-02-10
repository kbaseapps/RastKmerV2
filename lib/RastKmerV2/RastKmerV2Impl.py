# -*- coding: utf-8 -*-
#BEGIN_HEADER
import os
import subprocess

from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord

from GenomeAnnotationAPI.GenomeAnnotationAPIClient import GenomeAnnotationAPI
#END_HEADER


class RastKmerV2:
    '''
    Module Name:
    RastKmerV2

    Module Description:
    A KBase module: RastKmerV2
    '''

    ######## WARNING FOR GEVENT USERS ####### noqa
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    ######################################### noqa
    VERSION = "0.0.1"
    GIT_URL = ""
    GIT_COMMIT_HASH = ""

    #BEGIN_CLASS_HEADER
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.ws_url = config['workspace-url']
        self.scratch = config['scratch']
        #END_CONSTRUCTOR
        pass


    def annotate_genes(self, ctx, params):
        """
        :param params: instance of type "AnnotateGenesParams" -> structure:
           parameter "input_genome_ref" of String, parameter
           "output_workspace" of String, parameter "output_genome_name" of
           String
        """
        # ctx is the context object
        #BEGIN annotate_genes
        ga = GenomeAnnotationAPI(os.environ['SDK_CALLBACK_URL'], token=ctx['token'])
        genome = ga.get_genome_v1({"genomes": [{"ref": params['input_genome_ref']}],
                                          "included_fields": ["scientific_name"],
                                          "included_feature_fields": ["id", "protein_translation",
                                                                      "type", "function"
                                                                      ]})["genomes"][0]["data"]
        records = []
        for feature_index, feature in enumerate(genome["features"]):
            feature_id = feature["id"]
            sequence = feature.get("protein_translation")
            record = SeqRecord(Seq(sequence), id=feature_id, description="")
            records.append(record)
        fasta_file = self.scratch + "/proteins.faa"
        SeqIO.write(records, fasta_file, "fasta")
        output_file = self.scratch + '/output.txt'
        with open(fasta_file, "r") as infile:
            with open(output_file, "w") as outfile:
                p = subprocess.Popen(["kmer_search", ""], 
                                 cwd=self.scratch, stdin=infile, stdout=outfile)
                p.wait()
        fid_to_finc = {}
        with open(output_file, "r") as infile:
            for line in infile:
                fid, func, hits, hitsW = line.split("\t")
                print("fid=" + fid + ", function=" + func + ", hits=" + hits + ", hitsW=" + hitsW)
                fid_to_finc[fid] = func
        for feature_index, feature in enumerate(genome["features"]):
            feature_id = feature["id"]
            if feature_id in fid_to_finc:
                feature['function'] = fid_to_finc[feature_id]
        info = ga.save_one_genome_v1({'workspace': params['output_workspace'], 
                                      'name': params['output_genome_name'],
                                      'data': genome})['info']
        genome_ref = str(info[6]) + '/' + str(info[0]) + '/' + str(info[4])
        print("Genome saved to " + genome_ref)
        #END annotate_genes
        pass
    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK",
                     'message': "",
                     'version': self.VERSION,
                     'git_url': self.GIT_URL,
                     'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]
