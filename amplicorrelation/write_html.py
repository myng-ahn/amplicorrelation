import argparse
import requests
import re
from subprocess import run

# database from which we get info
BASE_URL = "https://www.genenetwork.nl/api/v1/gene/"

parser = argparse.ArgumentParser(
    prog="write_html.py", description="Create gene description page"
)
parser.add_argument("-s", "--sample_name", required=True, help="Name of sample")
parser.add_argument(
    "-a", "--amplicon_number", required=True, type=int, help="Amplicon number"
)
parser.add_argument(
    "-c", "--cycle_number", required=True, type=int, help="Cycle number"
)

args = parser.parse_args()
sample_name = args.sample_name
amplicon_num = args.amplicon_number
cycle_num = args.cycle_number
output_dir = f"out/{sample_name}_amplicon{amplicon_num}/cycle{cycle_num}"
fname = f"{sample_name}_amplicon{amplicon_num}_cycle_{cycle_num}"

known_oncogenes = []
with open("oncogenes.txt", "r") as f:
    for l in f:
        known_oncogenes.append(l.strip())

gene_info = ""
genes = []
with open(f"{output_dir}/{sample_name}_amplicon{amplicon_num}_genes.txt", "r") as f:
    for l in f:
        genes.append(l.strip())
for gene in genes:
    print(f"Fetching information about {gene}...")
    res = requests.get(f"{BASE_URL}{gene}")
    if res.status_code == 200:
        data = res.json()
        biotype = data["gene"]["biotype"]
        description = data["gene"]["description"]
        # remove '[Source:HGNC Symbol;Acc:HGNC:31098]' line from description
        source_string = "\[Source:.*\]"
        description = re.sub(source_string, "", description)
        oncogene_class = "oncogeneBtn" if gene in known_oncogenes else ""
        ncRNA_class = (
            "ncRNABtn"
            if ("ncRNA" in biotype) or ("snoRNA" in biotype) or ("antisense" in biotype)
            else ""
        )
        gene_info += f"""
            <button class="geneInfoBtn {oncogene_class} {ncRNA_class}">{gene}</button>
            <div class="panel">
                <p>Biotype: {biotype}</p>
                <p>Description: {description}</p>
            </div>
        """
    else:
        print(f"Unable to get information for {gene}")
if gene_info == "":
    gene_info = "Unable to retrieve gene information"

script = r"""
    <script>
        var acc = document.getElementsByClassName("geneInfoBtn");
        var i;

        for (i = 0; i < acc.length; i++) {
            acc[i].addEventListener("click", function () {
                this.classList.toggle("active");
                var panel = this.nextElementSibling;
                if (panel.style.maxHeight) {
                panel.style.maxHeight = null;
                } else {
                panel.style.maxHeight = panel.scrollHeight + "px";
                }
            });
        }
    </script>
"""

html = f"""
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <meta http-equiv="X-UA-Compatible" content="ie=edge" />
        <title>{fname} gene description</title>
        <link rel="stylesheet" href="../../../style.css" />
    </head>

    <body>
        <div class="wrapper">
        <h1>{fname} genes description</h1>
        <div class="split">
            <div class="geneInfoWrapper">
                {gene_info}
            </div>
            <div><img class="cycleViz" src="{fname}.png" /></div>
            </div>
        </div>
        {script}
    </body>
</html>
"""
with open(f"{output_dir}/{fname}.html", "w") as f:
    f.write(html)
