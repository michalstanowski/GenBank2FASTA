# README

## GenBank to FASTA Converter

This script processes GenBank Pept (.gp) files and converts them into the FASTA format (.fas). You can customize the output by specifying the format of the organism name, ID type, and whether to include detailed or additional information in the header. 

If no options are provided, the header will default to `seq_i`, where `i` is the sequence index in the GenBank file.

---

## Features

- **Customizable Output**: 
  - You can select the format for the organism name (full name, abbreviation, or shortened form).
  - Choose the ID type to be included in the header (LOCUS, ACCESSION, or GI).
  - Optionally, include the full definition or additional information (such as putative, predicted, hypothetical, etc.) in the header.
  
- **Default Header**: 
  - If no options are specified, the header will default to `seq_i`, where `i` is the index of the sequence in the input file.

---

## Installation

To use this script, make sure you have Python installed (Python 3.x recommended).

### Dependencies

- `argparse` (standard Python library)
- `re` (standard Python library)
- `os` (standard Python library)

No external libraries are required.

---

## Usage

### Command Line Arguments

```
usage: script.py [-h] -f file [--id {LOCUS,ACCESSION,GI}] [--o {1,2,3}]
                 [--d] [--a] [--s separator]

This script processes a GenBank Pept (.gp) file and converts it into a FASTA format (.fas).
You can customize the output by specifying an organism format, ID type, detailed and additional entry information
to include in the header.
If no options are provided, the header will default to 'seq_i', where i is the sequence index in the .gb file.

optional arguments:
  -h, --help            show this help message and exit
  -f file               Input GenBank file (required)
  --id {LOCUS,ACCESSION,GI}
                        ACCESSION, LOCUS or GI (default: None, no ID searched)
  --o {1,2,3}           Type of organism string (e.g., 1 for Mus musculus, 2 for M. musculus, 3 for Musmus) (default: None, no organism)
  --d                   Include whole entry definition (default: disabled)
  --a                   Include additional information (default: disabled)
  --s separator         Separator (default: '-')
```

### Arguments:

- **`-f file` (required)**: The path to the input GenBank Pept (.gp) file you want to process.
- **`--id {LOCUS,ACCESSION,GI}`**: Choose the ID type to include in the header. 
  - `LOCUS`: Includes the LOCUS field.
  - `ACCESSION`: Includes the ACCESSION field.
  - `GI`: Includes the GI number.
  - If not specified, no ID will be added to the header.
  
- **`--o {1,2,3}`**: Specifies the format of the organism name in the header:
  - `1`: Full name (e.g., Mus musculus).
  - `2`: Abbreviated form (e.g., M. musculus).
  - `3`: Shortened form (e.g., Musmus).
  - If not specified, the organism name will be omitted.
  
- **`--d`**: Includes the full entry definition in the header (from the `DEFINITION` field in GenBank).
  - If not specified, no definition will be included.
  
- **`--a`**: Includes additional information in the header, such as the type of protein (e.g., `p` for putative, `h` for hypothetical, etc.).
  - If not specified, no additional information will be included.
  
- **`--s separator`**: Defines the separator to use between different parts of the header (default is `-`).
  - Example: `--s "_"` would separate parts of the header with an underscore (`_`).

---

## Example Commands

1. **Convert a GenBank file to FASTA with full organism name, LOCUS ID, and additional information**:

   ```bash
   python script.py -f input.gb --id LOCUS --o 1 --d --a --s "-"
   ```

2. **Convert a GenBank file to FASTA with abbreviated organism name and ACCESSION ID**:

   ```bash
   python script.py -f input.gb --id ACCESSION --o 2
   ```

3. **Convert a GenBank file to FASTA with no additional information or custom header**:

   ```bash
   python script.py -f input.gb
   ```

   (This will default to `seq_i` where `i` is the sequence index.)

---

## Output Format

The output will be a FASTA file with headers in the following format:

```
>organism_name[separator]id[separator]additional_info[separator]definition
```

Where:
- `organism_name`: The format specified for the organism (e.g., full name, abbreviated name, or short form).
- `id`: The ID type specified (LOCUS, ACCESSION, or GI).
- `additional_info`: Optional information like `p` (putative), `h` (hypothetical), etc.
- `definition`: The full entry definition from the GenBank file (if `--d` is specified).

---

## Example Output

For a GenBank file with an organism name "Mus musculus", a LOCUS ID "X12345", and a definition "putative protein":

```
>Mus musculus-X12345-p-putative protein
ATGCGT...
```

If no options are provided, the output will look like:

```
>seq_0
ATGCGT...
```

---

## Notes

- The input GenBank Pept file must be properly formatted.
- The script will handle multiple sequences in a single GenBank file.
- If the GenBank file contains no sequences or improperly formatted data, the script may not generate any output.

---

## License

This script is released under the MIT License. See the LICENSE file for more information.
