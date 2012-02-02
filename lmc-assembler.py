#!/usr/bin/env python
import os
import sys

instructions = {'ADD': 100, 
                'SUB': 200,
                'STA': 300,
                'LDA': 500, 
                'BRA': 600, 
                'BRZ': 700, 
                'BRP': 800, 
                'INP': 901, 
                'OUT': 902, 
                'HALT': 000,
                'DAT': 000 }

def main(argv):
    if len(argv) is not 2: 
        print 'Specify a file to assemble.\nusage: LMC-assembler input.asm'
        sys.exit()

    tokens = pythonize(argv[1])
    symbols = get_symbols(tokens)
    print assemble(tokens, symbols)

def pythonize(infile):
    """Read the input file and produce easy to parse data structures.
    
    Returns a list of lists. The sublists contain each token in a given line
    from the input. The outer list is a list of the lines. Empty lines are
    included as empty lists.
    """
    lines = []
    try:
        with open(infile, 'r') as asm:
            for line in asm:
                lines.append(line.split())
    except EnvironmentError:
        print 'Specify a valid file as input\nusage: LMC-assembler input.asm'
        sys.exit()
    return lines

def get_symbols(token_list):
    """Find all of the symbols used in the assembly code.

    Returns a dictionary. Keys are symbol names, values are mailbox numbers. 
    """
    symbols = []
    for i, line in zip(range(len(token_list)), token_list):
        # ignore blank lines
        if not line:
            break
        if line[0] not in instructions.keys():
            symbols.append((line[0], i))
    return dict(symbols)

def assemble(token_list, symbols):
    program = ''
    for line in token_list:
        instruction = 0 
        # ignore blank lines
        if not line:
            break
        for i, token in zip(range(len(line)), line):
            if token in instructions.keys():
                instruction += instructions[token]
            elif token in symbols.keys() and i != 0:
                instruction += symbols[token]
            elif token.isdigit():
                instruction += int(token)

        program += str('%03d'%instruction)+'\n'

    return program

main(sys.argv)

