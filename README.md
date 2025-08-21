# Test Smell Prioritization

This repository contains the artifact for the paper:  
**"Prioritizing Test Smells: An Empirical Evaluation of Quality Metrics and Developer Perceptions" (ICSME 2025, NIER Track)**  

The artifact provides Python scripts, datasets, and documentation to **detect and prioritize test smells** using Change Proneness (CP) and Fault Proneness (FP) metrics.  
It enables reproduction of all **tables, figures, and prioritization results** presented in the paper.

---

## 📂 Repository Structure

- **DatasetCollection/**  
  Preprocessed datasets from 52 open-source Python projects.  

- **Test Smells Detection/**  
  Scripts for detecting 15 types of test smells in Python-based projects.  
  - `extract_smells.py` → Extracts test smells.  

- **Change Proneness_FaultProneness/**  
  Scripts for CP and FP computation.  
  - `ChangeProneness.py` → Computes Change Proneness metrics.  
  - `FaultProneness.py` → Computes Fault Proneness metrics.  

- **Results/**  
  Contains intermediate CSV files and aggregated results used in the paper.  

- **SmellsSummary.py**  
  Aggregates smell, CP, and FP data to reproduce summary tables.  

- **SmellsPlusCPaggregated.py**  
  Generates combined prioritization results and quadrant visualizations.  

- **requirements.txt**  
  Dependency list for reproducing the experiments.  

- **LICENSE**  
  MIT open-source license.  

---

## ⚙️ Requirements

- **OS**: Linux/Ubuntu (preferred), macOS; Windows users can use WSL.  
- **Python**: Version 3.8+  
- **Hardware**: 8 GB RAM, ~2 GB disk space  
- **Dependencies**: Install with:  
  ```bash
  pip install -r requirements.txt


## Usage

### Step 1: Clone the Repository

Clone the repository to your local machine:

```bash
git clone https://github.com/<your-username>/Test-Smell-Research.git
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

Paper Link: https://github.com/Md-Arif-Hasan/Test-Smell-Prioritization/blob/main/TestSmellPrioritization%23311.pdf

## Contributing

Contributions to this repository are welcome! If you'd like to contribute, please fork the repository, make your changes, and submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
