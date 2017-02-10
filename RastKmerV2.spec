/*
A KBase module: RastKmerV2
*/

module RastKmerV2 {
    typedef structure {
        string input_genome_ref;
        string output_workspace;
        string output_genome_name;
    } AnnotateGenesParams;

    funcdef annotate_genes(AnnotateGenesParams params) returns () authentication required;
};
