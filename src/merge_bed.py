"""Tool for cleaning up a BED file."""

import argparse  # we use this module for option parsing. See main for details.

import sys
from typing import TextIO
from bed import (
    parse_line, print_line, BedLine
)


def read_bed_file(f: TextIO) -> list[BedLine]:
    """Read an entire sorted bed file."""
    # Handle first line...
    line = f.readline()
    if not line:
        return []

    res = [parse_line(line)]
    for line in f:
        feature = parse_line(line)
        prev_feature = res[-1]
        assert prev_feature.chrom < feature.chrom or \
            (prev_feature.chrom == feature.chrom and
             prev_feature.chrom_start <= feature.chrom_start), \
            "Input files must be sorted"
        res.append(feature)

    return res

def print_output_line(bedline: BedLine, outfile: TextIO) -> None:
    chrom = bedline.chrom
    chrom_start = bedline.chrom_start
    chrom_end = bedline.chrom_end
    name = bedline.name
    output_line = f'{chrom}\t{chrom_start}\t{chrom_end}\t{name}'
    print(output_line, file = outfile)

def merge(f1: list[BedLine], f2: list[BedLine], outfile: TextIO) -> None:
    """Merge features and write them to outfile."""
    
    # FIXME: I have work to do here!
    
    l1 = len(f1)
    l2 = len(f2)
    i = 0
    j = 0
    while i < l1 or j < l2:
        if f1[i].chrom == f2[j].chrom:
            if f1[i].chrom_start < f2[j].chrom_start:
                print_output_line(f1[i], outfile)
                i += 1
            elif f1[i].chrom_start > f2[j].chrom_start:
                print_output_line(f2[j], outfile)
                j += 1
            else:
                print_output_line(f1[i], outfile)
                i += 1
                print_output_line(f2[j], outfile)
                j += 1
        else: 
            if f1[i].chrom < f2[j].chrom:
                print_output_line(f1[i], outfile)
                i += 1
            else: 
                print_output_line(f2[j], outfile)
                j += 1
                
            


def main() -> None:
    """Run the program."""
    # Setting up the option parsing using the argparse module
    argparser = argparse.ArgumentParser(description="Merge two BED files")
    argparser.add_argument('f1', type=argparse.FileType('r'))
    argparser.add_argument('f2', type=argparse.FileType('r'))
    argparser.add_argument('-o', '--outfile',  # use an option to specify this
                           metavar='output',   # name used in help text
                           type=argparse.FileType('w'),  # file for writing
                           default=sys.stdout)

    # Parse options and put them in the table args
    args = argparser.parse_args()

    # With all the options handled, we just need to do the real work
    features1 = read_bed_file(args.f1)
    features2 = read_bed_file(args.f2)
    merge(features1, features2, args.outfile)


if __name__ == '__main__':
    main()
