# HAdV-RE
RE analysis of HAdV

## data

```bash
taxid="10508"

python -m ffbio.ffdb "data/genbank/$taxid" \
  -term "txid$taxid[PORGN]" \
  -rettype gb \
  -email dnegron2@gmu.edu

mkdir -p data/blast

python -m ffbio.ffidx "data/genbank/$taxid.db" -dump -fo gb | \
  python -m ffbio.ffqual - db_xref | \
  awk -F '\t' 'NR > 1 { match($2, /taxon:([0-9]+)/, arr); print $1, arr[1] ? arr[1] : 0; }' > \
  "data/blast/$taxid.ssv"

python -m ffbio.ffidx "data/genbank/$taxid.db" -dump | \
  makeblastdb \
    -in - -dbtype nucl \
    -title "$taxid" -out "data/blast/$taxid" \
    -parse_seqids -hash_index -blastdb_version 5 \
    -taxid_map "data/blast/$taxid.ssv" -logfile "data/blast/$taxid.log"

mkdir -p data/fasta
blastdbcmd -db data/blast/10508 -entry all > data/fasta/10508.fasta
```

```bash
num_alignments="$(blastdbcmd -list data/blast -list_outfmt %n)"

blastdbcmd -db data/blast/10508 -entry AY599837.1 | \
  blastn \
    -task megablast \
    -query - \
    -db data/blast/10508 \
    -num_alignments "$num_alignments" \
    -num_threads 16 \
    -subject_besthit \
    -outfmt '7 std stitle qlen' > \
    hit-4a.tsv

blastdbcmd -db data/blast/10508 -entry AY594253.1 | \
  blastn \
    -task megablast \
    -query - \
    -db data/blast/10508 \
    -num_alignments "$num_alignments" \
    -num_threads 16 \
    -subject_besthit \
    -outfmt '7 std stitle qlen' > \
    hit-4p.tsv
```
