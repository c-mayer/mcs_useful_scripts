#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 23 10:42:46 2020

for further help please use: NW_or_SW_Aligment.py -h

@author: wuffw
"""

import argparse
from Bio import SeqIO
from collections import defaultdict
import os.path

# overall description of program
parser = argparse.ArgumentParser(description="Global Alignment of two sequences with Needleman-Wunsch or Local Aligment with two sequences with Smith-Waterman",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)  # show default value in help

# the following option(s) are required, so we create an own group for them, so they do not show up under 'optional arguments'
parser_req = parser.add_argument_group('required arguments')

parser_req.add_argument("-nw", "--needleman_wunsch",
                        help="activates Needleman-Wunsch Aligment (Global Aligment)",
                        action="store_true",
                        default=False)
parser_req.add_argument("-sw", "--smith_waterman",
                        help="activates Smith-Waterman Aligment (Local Aligment)",
                        action="store_true",
                        default=False)

parser_req.add_argument("-s", "--sequence",
                        nargs=2,
                        help="input DNA/RNA strings or FASTA files which only contain one sequence; sequence can only contain A, G, C, T, U and N",
                        metavar=("SEQ1", "SEQ2"),
                        required=True)

# optional arguments
parser.add_argument("-m", "--match",
                    help="match score of the aligment",
                    type=int,
                    metavar="INT",
                    action="store",
                    default=1)
parser.add_argument("-mm", "--mismatch",
                    help="mismatch score of the aligment",
                    type=int,
                    metavar="INT",
                    action="store",
                    default=-1)
parser.add_argument("-g", "--gap",
                    help="gap score of the aligment",
                    type=int,
                    metavar="INT",
                    action="store",
                    default=-2)

parser.add_argument("-vm", "--value_matrix",
                    help="shows value matrix in output",
                    action="store_true",
                    default=False)

args = parser.parse_args()

# dictionary for costs
costs = {'match': args.match,
         'mismatch': args.mismatch,
         'gap': args.gap}


# function definitions
def validate_base_sequence(base_sequence):
    """Returns True for valid nucleotide sequence"""
    seq = base_sequence.upper()
    if "U" in seq and "T" in seq:
        raise ValueError("Mixed RNA/DNA found")
    return len(seq) == (seq.count('U') + seq.count('T') + seq.count('C') + seq.count('A') + seq.count('G') + seq.count('N'))


def NeedlemanWunsch_bt(seq1, seq2, match, mismatch, gap):
    """Creates Needleman-Wunsch matrices"""
    global matrix

    seq1.upper()
    seq2.upper()

    cols = len(seq1) + 1
    rows = len(seq2) + 1

    matrix = []
    btmatrix = []
    for i in range(rows):
        matrix.append([0] * cols)
        btmatrix.append([0] * cols)

    for j in range(cols):
        matrix[0][j] = j * gap
        # for the first index of all columns, know we walked horizontal
        btmatrix[0][j] = 'ho'

    for i in range(rows):
        matrix[i][0] = i * gap
        # for the first index of all rows, know we walked vertical
        btmatrix[i][0] = 've'

    # the upper left corner of our 'matrix' is 0 or undefined
    btmatrix[0][0] = '-'

    for i in range(1, rows):
        for j in range(1, cols):

            if seq2[i - 1] == seq1[j - 1]:
                mis_or_match = match
            else:
                mis_or_match = mismatch

            diag = matrix[i - 1][j - 1] + mis_or_match
            vert = matrix[i - 1][j] + gap
            hori = matrix[i][j - 1] + gap

            matrix[i][j] = max(diag, hori, vert)

            # let's make a copy of our value matrix filled with directions
            # instead of values to have an easy time backtracing the alignment
            if matrix[i][j] == hori:
                btmatrix[i][j] = 'ho'
            elif matrix[i][j] == vert:
                btmatrix[i][j] = 've'
            elif matrix[i][j] == diag:
                btmatrix[i][j] = 'di'

    # return the backtracing matrix
    return btmatrix


def SmithWaterman_bt(seq1, seq2, match, mismatch, gap):
    """Creates Smith-Waterman matrices"""
    global matrix
    global value2positions

    seq1.upper()
    seq2.upper()

    cols = len(seq1) + 1
    rows = len(seq2) + 1

    matrix = []
    btmatrix = []
    value2positions = defaultdict(list)  # !!! create dict to find max value for backtracing
    for i in range(rows):
        matrix.append([0] * cols)
        btmatrix.append([0] * cols)

    for j in range(cols):
        matrix[0][j] = j * gap if j * gap >= 0 else 0
        # for the first index of all columns, know we walked horizontal
        btmatrix[0][j] = 0 if matrix[0][j] <= 0 else 'ho'  # !!! prioritises 0 over ho

    for i in range(rows):
        matrix[i][0] = i * gap if i * gap >= 0 else 0
        # for the first index of all rows, know we walked vertical
        btmatrix[i][0] = 0 if matrix[i][0] <= 0 else 've'  # !!! prioritises 0 over ve

    # the upper left corner of our 'matrix' is 0 or undefined
    btmatrix[0][0] = '-'

    for i in range(1, rows):
        for j in range(1, cols):

            if seq2[i - 1] == seq1[j - 1]:
                mis_or_match = match
            else:
                mis_or_match = mismatch

            diag = matrix[i - 1][j - 1] + mis_or_match
            vert = matrix[i - 1][j] + gap
            hori = matrix[i][j - 1] + gap

            matrix[i][j] = max(diag, hori, vert, 0)  # !!! 0 added, because no value below 0 allowed
            value2positions[max(diag, hori, vert, 0)].append((i, j))  # !!! writes dict

            # let's make a copy of our value matrix filled with directions
            # instead of values to have an easy time backtracing the alignment
            if matrix[i][j] == 0:  # !!! prints 0, even if di, ve or ho are 0
                btmatrix[i][j] = 0 # 0 in btmatrix of Smith-Waterman
            elif matrix[i][j] == hori:
                btmatrix[i][j] = 'ho'
            elif matrix[i][j] == vert:
                btmatrix[i][j] = 've'
            elif matrix[i][j] == diag:
                btmatrix[i][j] = 'di'

    # return the backtracing matrix
    return btmatrix


def backtrace(i, j):
    """Traces back the btmatrix and creates aligment strings"""
    global seq1_sol
    global seq2_sol

    if i == 0 and j == 0:  # stops when sequences end
        return
    if btmatrix[i][j] == 0:  # !!! (for SW) not necessary but less bug prone
        return
    elif btmatrix[i][j] == 'di':
        seq1_sol = seq1[j-1] + seq1_sol
        seq2_sol = seq2[i-1] + seq2_sol
        backtrace(i-1, j-1)
    elif btmatrix[i][j] == 'ho':
        seq1_sol = seq1[j-1] + seq1_sol
        seq2_sol = '-' + seq2_sol # introduce 'gaps' i.e. '-' into the sequence
        backtrace(i, j-1)
    elif btmatrix[i][j] == 've':
        seq1_sol = '-' + seq1_sol # introduce 'gaps' i.e. '-' into the sequence
        seq2_sol = seq2[i-1] + seq2_sol
        backtrace(i-1, j)


# !!! takes and proofs sequence input and processes it
seqlist = []
for s in args.sequence:
    try:
        if os.path.isfile(s):
            record = SeqIO.read(s, "fasta") # reads from FASTA File (this special SeqIO.read command accepts only one sequence per file)
            if validate_base_sequence(record.seq.upper()):
                seqlist.append(record.seq.upper()) # appends FASTA sequence
            elif validate_base_sequence(s) is False:
                raise ValueError("RNA/DNA contains invalid nucleotides")
        else:
            if validate_base_sequence(s):
                seqlist.append(s.upper()) # appends manually written sequence
            elif validate_base_sequence(s) is False:
                raise ValueError("file does not exist or RNA/DNA contains invalid nucleotides")
    except ValueError as e:
        if str(e) == "No records found in handle":
            print(f"{s}\nValueError: {e} - file has to be FASTA format")
        elif str(e) == "More than one record found in handle":
            print(f"{s}\nValueError: {e} - only one sequence per FASTA file is allowed")
        else:
            print(f"{s}\nValueError: {e}")
        quit()

print("cost values:", costs)
# print(args.sequence)
# print(seqlist)
seq1 = seqlist[0]
seq2 = seqlist[1]

print(f"Sequence Input:\nSEQ1: {seq1}\nSEQ2: {seq2}")

# proofs if both strings are RNA or DNA
seqall = seq1 + seq2
if "U" in seqall and "T" in seqall:
        raise ValueError("You cant align RNA to DNA")

# both options are possible but at least one of them is required
if not (args.needleman_wunsch or args.smith_waterman):
    parser.error("at least one aligment type option is required (-nw or -sw)")


if args.needleman_wunsch:
    # now our function returns the backtracing matrix which we can use to modify our sequences to print
    # the alignment (and to be able to easily check if the output is correct if we print it)

    btmatrix = NeedlemanWunsch_bt(seq1, seq2, match=costs['match'], mismatch=costs['mismatch'], gap=costs['gap'])

# print the value matrix
    if args.value_matrix:
        print("\nNW Matrix:")
        for k in (range(len(matrix))):
            print(*matrix[k], sep="\t")

# hashed, because it does not give any necessary information for the output
    # print the backtracing matrix
    # print("\nBacktracing the NW Matrix:")
    # for k in (range(len(btmatrix))):
        # print(*btmatrix[k], sep="\t")

    seq1_sol = ''
    seq2_sol = ''

    backtrace(len(seq2), len(seq1))

    print("\nNW-Alignment:\n", seq1_sol, "\n", seq2_sol, "\tFinal Score:", matrix[len(seq2)][len(seq1)])


if args.smith_waterman:

    btmatrix = SmithWaterman_bt(seq1, seq2, match=costs['match'], mismatch=costs['mismatch'], gap=costs['gap'])

# print the value matrix
    if args.value_matrix:
        print("\nSW Matrix:")
        for k in (range(len(matrix))):
            print(*matrix[k], sep="\t")

# hashed, because it does not give any necessary information for the output
    # print the backtracing matrix
    # print("\nBacktracing the SW Matrix:")
    # for k in (range(len(btmatrix))):
        # print(*btmatrix[k], sep="\t")

# loops all positions with max score and outputs all aligments with max score
    # print(value2positions)
    print("\nSW-Alignments:")
    for i, j in max(value2positions.values()):
        seq1_sol = ''
        seq2_sol = ''
        backtrace(i, j) # !!! begins on position with max value
        print(f'{seq1_sol}\n{seq2_sol}\tmax Score: {max(value2positions)}\n')
