ruleorder: finalize_hawaii > finalize

rule add_labels:
    message: "Remove extraneous colorings for main build and move frequencies"
    input:
        auspice_json = rules.incorporate_travel_history.output.auspice_json,
        tree = rules.refine.output.tree,
        clades = rules.clades.output.clade_data,
        mutations = rules.ancestral.output.node_data
    output:
        auspice_json = "results/{build_name}/ncov_with_accessions_and_travel_branches_and_labels.json",
    log:
        "logs/add_labels_{build_name}.txt"
    conda: config["conda_environment"]
    shell:
        """
        python3 scripts/add_labels.py \
            --input {input.auspice_json} \
            --tree {input.tree} \
            --mutations {input.mutations} \
            --clades {input.clades} \
            --output {output.auspice_json} 2>&1 | tee {log}
        """

rule finalize_hawaii:
    message: "Remove extraneous colorings for main build and move frequencies"
    input:
        auspice_json = rules.add_labels.output.auspice_json,
        frequencies = rules.tip_frequencies.output.tip_frequencies_json,
        root_sequence_json = rules.export.output.root_sequence_json
    output:
        auspice_json = "auspice/ncov_{build_name}.json",
        tip_frequency_json = "auspice/ncov_{build_name}_tip-frequencies.json",
        root_sequence_json = "auspice/ncov_{build_name}_root-sequence.json"
    log:
        "logs/fix_colorings_{build_name}.txt"
    conda: config["conda_environment"]
    shell:
        """
        python3 scripts/fix-colorings.py \
            --input {input.auspice_json} \
            --output {output.auspice_json} 2>&1 | tee {log} &&
        cp {input.frequencies} {output.tip_frequency_json} &&
        cp {input.root_sequence_json} {output.root_sequence_json}
        """

rule dated_json:
    message: "Copying dated Auspice JSON"
    input:
        auspice_json = rules.finalize_hawaii.output.auspice_json,
        tip_frequencies_json = rules.tip_frequencies.output.tip_frequencies_json,
        root_sequence_json = rules.export.output.root_sequence_json
    output:
        dated_auspice_json = "auspice/ncov_{build_name}_{date}.json",
        dated_tip_frequencies_json = "auspice/ncov_{build_name}_{date}_tip-frequencies.json",
        dated_root_sequence_json = "auspice/ncov_{build_name}_{date}_root-sequence.json"
    benchmark:
        "benchmarks/dated_json_{build_name}_{date}.txt"
    conda: config["conda_environment"]
    shell:
        """
        cp {input.auspice_json} {output.dated_auspice_json}
        cp {input.tip_frequencies_json} {output.dated_tip_frequencies_json}
        cp {input.root_sequence_json} {output.dated_root_sequence_json}
        """

def get_todays_date():
    from datetime import datetime
    date = datetime.today().strftime('%Y-%m-%d')
    return date

rule all_regions:
    input:
        auspice_json = expand("auspice/ncov_{build_name}.json", build_name=BUILD_NAMES),
        tip_frequencies_json = expand("auspice/ncov_{build_name}_tip-frequencies.json", build_name=BUILD_NAMES),
        root_sequence_json = expand("auspice/ncov_{build_name}_root-sequence.json", build_name=BUILD_NAMES),
        dated_auspice_json = expand("auspice/ncov_{build_name}_{date}.json", build_name=BUILD_NAMES, date=get_todays_date()),
        dated_tip_frequencies_json = expand("auspice/ncov_{build_name}_{date}_tip-frequencies.json", build_name=BUILD_NAMES, date=get_todays_date()),
        dated_root_sequence_json = expand("auspice/ncov_{build_name}_{date}_root-sequence.json", build_name=BUILD_NAMES, date=get_todays_date())

