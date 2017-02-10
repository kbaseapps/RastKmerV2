FROM kbase/kbase:sdkbase.latest
MAINTAINER KBase Developer
# -----------------------------------------

# Insert apt-get instructions here to install
# any required dependencies for your module.

# RUN apt-get update
RUN pip install coverage

WORKDIR /kb/deployment/plbin
RUN wget https://raw.githubusercontent.com/kbase/kb_seed/master/service-scripts/kmer_search.pl && \
    echo 'perl /kb/deployment/plbin/kmer_search.pl "$@"' > ../bin/kmer_search && \
    chmod +x ../bin/kmer_search
RUN wget https://raw.githubusercontent.com/kbase/kb_seed/master/service-scripts/km_process_hits_to_regions.pl && \
    echo 'perl /kb/deployment/plbin/km_process_hits_to_regions.pl "$@"' > ../bin/km_process_hits_to_regions && \
    chmod +x ../bin/km_process_hits_to_regions
RUN wget https://raw.githubusercontent.com/kbase/kb_seed/master/service-scripts/km_pick_best_hit_in_peg.pl && \
    echo 'perl /kb/deployment/plbin/km_pick_best_hit_in_peg.pl "$@"' > ../bin/km_pick_best_hit_in_peg && \
    chmod +x ../bin/km_pick_best_hit_in_peg

# -----------------------------------------

COPY ./ /kb/module
RUN mkdir -p /kb/module/work
RUN chmod 777 /kb/module

WORKDIR /kb/module

RUN make all

ENTRYPOINT [ "./scripts/entrypoint.sh" ]

CMD [ ]
