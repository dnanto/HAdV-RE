#!/usr/bin/env python3

import sys

from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter, FileType

from Bio import Restriction, SeqIO


def argparser():
    parser = ArgumentParser(
        description="compute restriction fragment length polymorphism profile",
        formatter_class=ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("file", type=FileType(), help="the sequence file")
    parser.add_argument("enzymes", nargs="+", help="the restriction enzyme names")
    parser.add_argument(
        "-circular",
        action="store_true",
        help="the flag to set default topology to circular if not specified in annotation",
    )
    return parser

def main(argv):
    args = argparser().parse_args(argv[1:])

    for record in SeqIO.parse(args.file, "fasta"):
        for enzyme in args.enzymes:
            enzyme = getattr(Restriction, enzyme)
            for frag in enzyme.catalyze(record.seq, linear=(not args.circular)):
                print(record.id, enzyme, len(frag), sep="\t")

    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
