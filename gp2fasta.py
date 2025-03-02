import argparse
import re
import os

# parser

parser = argparse.ArgumentParser(description="This script processes a GenBank Pept (.gp) file and converts it into a FASTA format (.fas). "
                "You can customize the output by specifying an organism format, ID type, detailed and additional entry information"
                " to include in the header. "
                "If no options are provided, the header will default to 'seq_i', where i "
                "is the sequence index in the .gb file.")

parser.add_argument("-f", type=str, required=True, metavar="file", help="Input GenBank file (required)")
parser.add_argument("--id", type=str, choices=["LOCUS", "ACCESSION", "GI"], help="ACCESSION, LOCUS or GI (default: None, no ID searched)")
parser.add_argument("--o", type=int, choices=[1, 2, 3], default=None, help="Type of organism string (e.g., 1 for Mus musculus, 2 for M. musculus, 3 for Musmus) (default: None, no organism)")
parser.add_argument("--d", action="store_true", help="Include whole entry definition (default: disabled)")
parser.add_argument("--a", action="store_true", help="Include additional information (default: disabled)")
parser.add_argument("--s", type=str, default="-", metavar="separator", help="Separator (default: '-')")

args = parser.parse_args()
file = args.f
id = args.id
organism = args.o
d = args.d
a = args.a 
s = args.s

# creating fasta filename

filename = os.path.basename(file)
fasta_basename = filename.split(".")[0] + ".fas"

with open(file, "r") as gb_file, open(fasta_basename, "w") as fasta_file:
    gi_list = []
    new_orgs = []
    new_defs = []
    definitions = []
    sequences = []
    sequence_lines = []
    is_origin = False
    collecting_definition = False
    
    for line in gb_file: # iterates through each file line only once
        line = line.strip()
        
        # id part 

        if id == "LOCUS" and line.startswith("LOCUS"):
            match = re.search(r"LOCUS\W+(\w+)", line)
            if match:
                gi_list.append(match.group(1))
        
        elif id == "ACCESSION" and line.startswith("ACCESSION"):
            match = re.search(r"ACCESSION\W+(\w+)", line)
            if match:
                gi_list.append(match.group(1))
        
        elif id == "GI" and line.startswith("VERSION"):
            match = re.search(r"VERSION\s+\S+\s+GI:(\d+)", line)
            if match:
                gi_list.append(match.group(1))
        
        # organism part

        elif line.startswith("ORGANISM"):
            match = re.search(r"ORGANISM\W+(.+)", line)
            if match:
                org = match.group(1).split(" ")
                len_org = len(org)
                if organism == 1: # full name, Mus musculus
                    new_orgs.append(" ".join(org))
                elif organism == 2 and len_org == 2: # M. musculus, only for names consisting of two words
                    new_orgs.append(f"{org[0][0]}.{org[1]}")
                elif organism == 3 and len_org == 2:
                    new_orgs.append(f"{org[0][:3]}{org[1][:3]}") # Musmus, only for names consisting of two words
                elif (len_org > 2 or len_org == 1) and organism in [1,2,3]: # exceptions: long species/strain names or only genus name, save only the genus name
                    new_orgs.append(org[0])

        # detailed and additional info part

        elif line.startswith("DEFINITION"):
            definition = re.sub(r"^DEFINITION\s+", "", line).lower()
            collecting_definition = True  # definitions can be multi-line

        elif collecting_definition:
            if line.startswith("ACCESSION"):  # end of definition
                collecting_definition = False
                if d:
                    definitions.append(definition.strip())  # saving whole definition

                if a:  # addditional info
                    if "putative" in definition:
                        new_defs.append(f"{s}p")
                    elif "predicted" in definition:
                        new_defs.append(f"{s}P")
                    elif "hypothetical" in definition:
                        new_defs.append(f"{s}h")
                    elif "unnamed" in definition:
                        new_defs.append(f"{s}u")
                    elif "novel" in definition:
                        new_defs.append(f"{s}n")
                    elif "open" in definition:
                        new_defs.append(f"{s}o")
                    else:
                        new_defs.append("")
            else:
                definition += " " + line.strip()  # continue obtaining definition info
        
        # sequence part

        elif line.startswith("ORIGIN"):
            is_origin = True
            sequence_lines = []
            continue
        
        elif is_origin:
            if line == "//": # end of the entry
                sequences.append("".join(sequence_lines).upper())
                is_origin = False
            else: # still reading the sequence
                sequence_lines.append("".join(re.findall(r"[a-zA-Z]+", line)))
    

    for i in range(len(sequences)): 
        organism_part = new_orgs[i] if new_orgs and i < len(new_orgs) else "" 
        definition_part = f"{s}{definitions[i]}" if definitions and i < len(definitions) else ""
        gi_part = f"{s + gi_list[i]}" if i < len(gi_list) else ''
        new_defs_part = new_defs[i] if i < len(new_defs) else ''
        if not (organism_part or gi_part or new_defs_part or definition_part): # if no option was provided, save the entry as seq_i
            organism_part = f"seq_{i}"
        fasta_file.write(f">{organism_part}{gi_part}{new_defs_part}{definition_part}\n") # write the new entry to fasta file
        fasta_file.write(f"{sequences[i] if i < len(sequences) else ''}\n")
