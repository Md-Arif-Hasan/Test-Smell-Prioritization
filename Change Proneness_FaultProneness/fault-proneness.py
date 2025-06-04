

import os
import git
import csv
from pathlib import Path
from typing import List, Tuple

class LocalFaultDetector:
    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)
        try:
            self.repo = git.Repo(self.repo_path)
        except git.exc.InvalidGitRepositoryError:
            raise ValueError(f"'{repo_path}' is not a valid Git repository")

    def is_bug_fix_commit(self, commit) -> bool:
        bug_keywords = {'bug', 'fix', 'defect', 'fault', 'issue', 'error'}
        return any(keyword in commit.message.lower() for keyword in bug_keywords)

    def get_previous_revision(self, file_path: str, bug_fix_commit) -> str:
        """
        Get the previous revision (commit hash) of the file before a bug-fix commit.
        """
        try:
            commits = list(self.repo.iter_commits(paths=file_path))
            for i, commit in enumerate(commits):
                if commit.hexsha == bug_fix_commit.hexsha and i + 1 < len(commits):
                    return commits[i + 1].hexsha  # Previous revision
        except git.exc.GitCommandError:
            pass
        return ""

    def analyze_file_history(self, file_path: str) -> Tuple[bool, str]:
        """
        Analyze a file's commit history to determine if it's fault-prone.
        Returns whether the file is faulty and the previous faulty revision hash.
        """
        try:
            commits = list(self.repo.iter_commits(paths=file_path))
            for commit in commits:
                if self.is_bug_fix_commit(commit):
                    prev_revision = self.get_previous_revision(file_path, commit)
                    return True, prev_revision
            return False, ""
        except git.exc.GitCommandError:
            return False, ""

    def get_python_files(self) -> List[str]:
        return [
            os.path.relpath(os.path.join(root, file), self.repo_path)
            for root, _, files in os.walk(self.repo_path)
            for file in files
            if file.endswith('.py')
        ]

    def analyze_repository(self) -> List[Tuple[str, str, int, str]]:
        return [
            (str(self.repo_path), file_path, int(is_faulty), prev_revision)
            for file_path in self.get_python_files()
            for is_faulty, prev_revision in [self.analyze_file_history(file_path)]
        ]

def process_directory(input_dir: str, output_dir: str):
    """
    Process each repository and create individual CSV files in the output directory.
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    for root, dirs, _ in os.walk(input_dir):
        for dir_name in dirs:
            repo_path = os.path.join(root, dir_name)
            try:
                # Create CSV file name based on repository name
                csv_filename = f"{dir_name}_fault_proneness.csv"
                output_file = os.path.join(output_dir, csv_filename)

                # Analyze repository
                detector = LocalFaultDetector(repo_path)
                results = detector.analyze_repository()

                # Write results to CSV
                with open(output_file, 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(['Repository', 'File', 'Is_Faulty', 'Previous_Faulty_Revision'])
                    writer.writerows(results)

                print(f"Successfully analyzed repository: {repo_path}")
                print(f"Results written to: {output_file}")

            except ValueError:
                print(f"Skipping non-Git directory: {repo_path}")
            except Exception as e:
                print(f"Error analyzing repository {repo_path}: {str(e)}")

def main():
    input_dir = ".../Pynose_Projects"
    output_dir = ".../Pynose_Projects/Fault_proneness"
    
    process_directory(input_dir, output_dir)
    print(f"Analysis complete. Results written to directory: {output_dir}")

if __name__ == "__main__":
    main()