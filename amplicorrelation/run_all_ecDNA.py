from subprocess import run

with open("ecDNA_only.csv", "r") as f:
    for l in f:
        fields = l.split(",")
        dataset = fields[1]
        aa_num = str(int(float(fields[2])))
        print(f"CycleVizing {dataset}_amplicon{aa_num}...")
        process = run(
            ["python", "batchCV.py", "-s", dataset, "-a", aa_num],
            capture_output=True,
            text=True,
        )
