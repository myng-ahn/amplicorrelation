import sys
import os
import argparse
import re
from subprocess import run

### made a change in CycleViz.py itself. Will not work without this

parser = argparse.ArgumentParser(
    prog="batchCV.py", description="Run CycleViz in batch fashion"
)
parser.add_argument("-s", "--sample_name", required=True, help="Name of sample")
parser.add_argument(
    "-a", "--amplicon_number", required=True, type=int, help="Number of amplicon"
)
parser.add_argument(
    "-c",
    "--cycle_numbers",
    required=False,
    type=lambda arg: [int(num) for num in arg.split(",")],
    help="Comma-separated list of which cycles to include in analysis.",
)
parser.add_argument("-o", "--outname", required=False, help="Prefix of output")
args = parser.parse_args()
sample_name = args.sample_name
amplicon_num = args.amplicon_number
prefix = f"{sample_name}_amplicon{amplicon_num}" if not args.outname else args.outname

CYCLES_DIR = "../results/other_files/ccle_hg38_ac/ccle_hg38_annotated_cycles_files/"
GRAPHS_DIR = "../results/other_files/ccle_hg38_ac/files/"
cycles_png = f"{GRAPHS_DIR}{sample_name}_amplicon{amplicon_num}.png"
cycles_file = f"{CYCLES_DIR}{sample_name}_amplicon{amplicon_num}_annotated_cycles.txt"
graphs_file = f"{GRAPHS_DIR}{sample_name}_amplicon{amplicon_num}_graph.txt"

# get number of cycles in amplicon
cycles = []
parse_string = r"^Cycle=(\d+).*CycleClass=ecDNA-like.*$"
with open(cycles_file, "r") as f:
    for l in f:
        # only run for cyclic paths ecDNA structures
        regex_match = re.search(parse_string, l)
        if regex_match:
            cycles.append(regex_match.group(1))
# if the user has not defined which cycles to run, do all cyclic paths in amplicon
cycles = cycles if not args.cycle_numbers else args.cycle_numbers

# if no cycles to run
if len(cycles) == 0:
    print("No ecDNA cycles in this amplicon. Exiting program.")
    exit(0)

# create directory to store all output
if not os.path.exists("out"):
    os.makedirs("out")
# create directory to sample output folder
if not os.path.exists(f"out/{prefix}"):
    os.makedirs(f"out/{prefix}")
# create nested subdirectory to cycles folder
for cycle in cycles:
    if not os.path.exists(f"out/{prefix}/cycle{cycle}"):
        os.makedirs(f"out/{prefix}/cycle{cycle}/")

# copy over cycles png
if os.name == "nt":
    process = run(
        ["copy", cycles_png.replace("/", "\\"), f"out\\{prefix}" + "\\"], shell=True
    )
elif os.name == "posix":
    process = run(["cp", cycles_png, f"{prefix}/"])

# run convert_cycles_file.py preprocessing step
process = run(
    [
        "python",
        "../CycleViz/convert_cycles_file.py",
        "-c",
        cycles_file,
        "-g",
        graphs_file,
        "-o",
        f"out/{prefix}/{prefix}_converted",
    ],
    capture_output=True,
    text=True,
)

# run CycleViz.py for every cycle in amplicon
for cycle in cycles:
    process = run(
        [
            "python",
            "../CycleViz/CycleViz.py",
            "--ref",
            "GRCh38",
            "--cycles_file",
            f"out/{prefix}/{prefix}_converted_cycles.txt",
            "--cycle",
            str(cycle),
            "-g",
            graphs_file,
            "--label_segs",
            "numbers",
            "--noPDF",
            "--outname",
            f"out/{prefix}/cycle{cycle}/{prefix}",
        ]
    )
