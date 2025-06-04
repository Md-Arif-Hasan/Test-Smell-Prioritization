
# Test Smell Prioritization based on Change Proneness and Fault Proneness

This repository contains a set of Python scripts and shell tools designed for analyzing and prioritizing test smells based on Change Proneness (CP) and Fault Proneness (FP) metrics in Python-based software systems. The goal of this study is to help developers identify test smells that are more likely to affect the maintainability of the system, enabling them to prioritize refactoring efforts.

## Repository Contents

The repository includes various Python scripts and shell scripts that assist in the extraction and analysis of test smells and the computation of CP and FP metrics. Key functionalities include:

- **Test Smell Extraction**: Identifying various test smells in Python-based software.
- **Change Proneness (CP) Analysis**: Calculating CP metrics to measure the likelihood of code changes.
- **Fault Proneness (FP) Analysis**: Assessing FP metrics to determine the probability of faults occurring.
- **Prioritization Algorithms**: Using CP and FP metrics to prioritize the test smells that need attention first.
- **Data Aggregation**: Aggregating test smell and CP/FP results for easier analysis.
- **File Format Conversion**: Converting data between XML, CSV, and other formats for compatibility.

## Prerequisites

To run the code, make sure you have the following installed:

- Python 3.x (preferably the latest version)
- Required Python packages (listed below)
- Shell environment (for `.sh` scripts)

### Install Dependencies

You can install the necessary Python packages by running the following command:

```bash
pip install -r requirements.txt
```

If `requirements.txt` is not present, you can manually install the commonly used packages:

- pandas
- numpy
- matplotlib
- xml.etree.ElementTree (for XML parsing)

### Shell Script Dependencies

The shell scripts (`.sh` files) require a Unix-like shell environment (Linux, macOS, or Windows with WSL).

## Usage

### Step 1: Clone the Repository

Clone the repository to your local machine:

```bash
git clone https://github.com/Md-Arif-Hasan/Test-Smell-Research.git
cd Test-Smell-Research
```

### Step 2: Running Python Scripts

Run the Python scripts to extract test smells and analyze CP and FP metrics. For example, to run the **FaultProneness.py** script:

```bash
python FaultProneness.py
```

Feel free to replace the script name with the one that fits your needs.

### Step 3: Running Shell Scripts

For Unix-like environments, you can run the shell scripts as follows:

```bash
bash extract_contributors.sh
```

These shell scripts are typically used for extracting specific metrics or performing analysis on the dataset.

### Step 4: Analyzing Data

The results are typically stored in CSV or other formats. You can use Python (e.g., with pandas) or other tools to analyze the output. For example, the **SmellsSummary.py** script aggregates the results for an overview of test smells and their impact on CP/FP metrics.

## Reproducing Results

To reproduce the results from this repository, follow these steps:

1. Clone the repository and install the necessary dependencies.
2. Execute the Python scripts for extracting test smells and analyzing CP/FP metrics.
3. Aggregate the results using the provided aggregation scripts (e.g., `SmellsSummary.py` or `SmellsPlusCPaggregated.py`).
4. Review the output files for a summary of the test smells and their associated CP/FP scores.

## Contributing

Contributions to this repository are welcome! If you'd like to contribute, please fork the repository, make your changes, and submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
