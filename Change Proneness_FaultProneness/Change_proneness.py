# Python script (analyze_projects.py)
import os
import pandas as pd

# Path to the directory containing Python projects
projects_path = "/home/iit/Downloads/Thesis/Pynose_Projects"

def analyze_projects():
    # Get absolute path for output directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(current_dir, "ChangeProneness_analysis_results")
    
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")

    # Iterate through each project in the directory
    for project in os.listdir(projects_path):
        project_path = os.path.join(projects_path, project)
        
        # Skip if not a directory
        if not os.path.isdir(project_path):
            continue
            
        print(f"Analyzing project: {project}")
        
        # Generate CSV filename with absolute path
        csv_filename = f"{project}_analysis.csv"
        csv_path = os.path.join(output_dir, csv_filename)
        
        # Run the bash script for analysis
        command = f"bash CP.sh '{project}' '{project_path}' '{csv_path}'"
        os.system(command)

if __name__ == "__main__":
    analyze_projects()

