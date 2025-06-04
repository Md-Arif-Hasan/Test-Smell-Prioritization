
import os
import git
from pathlib import Path
from typing import List, Tuple, Dict
import argparse
import csv
import re
import subprocess

class LocalFaultDetector:
    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)
        try:
            self.repo = git.Repo(self.repo_path)
            self.remote_url = self.repo.remotes.origin.url if self.repo.remotes else str(self.repo_path)
        except git.exc.InvalidGitRepositoryError:
            raise ValueError(f"'{repo_path}' is not a valid Git repository")

    def is_bug_fix_commit(self, commit) -> bool:
        bug_keywords = {'bug', 'fix', 'defect', 'fault', 'issue', 'error'}
        return any(keyword in commit.message.lower() for keyword in bug_keywords)

    def calculate_file_changes(self, file_path: str) -> Dict[str, int]:
        try:
            total_insertions = 0
            total_deletions = 0
            commits = list(self.repo.iter_commits(paths=file_path))
            total_commits = len(commits)

            for i in range(len(commits) - 1):
                current_commit = commits[i]
                parent_commit = commits[i+1]

                try:
                    diff_command = [
                        'git', 
                        '-C', 
                        str(self.repo_path), 
                        'diff', 
                        '--numstat', 
                        parent_commit.hexsha, 
                        current_commit.hexsha, 
                        '--', 
                        file_path
                    ]
                    diff_output = subprocess.check_output(diff_command, universal_newlines=True).strip()

                    if diff_output:
                        match = re.match(r'(\d+)\s+(\d+)\s+', diff_output)
                        if match:
                            insertions = int(match.group(1))
                            deletions = int(match.group(2))
                            total_insertions += insertions
                            total_deletions += deletions

                except subprocess.CalledProcessError:
                    continue

            return {
                'TotalCommits': total_commits,
                'Insertions': total_insertions,
                'Deletions': total_deletions
            }
        except Exception as e:
            print(f"Error calculating changes for {file_path}: {e}")
            return {'TotalCommits': 0, 'Insertions': 0, 'Deletions': 0}

    def get_file_versions(self, file_path: str) -> List[Tuple[git.Commit, bool]]:
        try:
            commits = list(self.repo.iter_commits(paths=file_path))
            versions = []
            fault_count = 0
            
            for i in range(len(commits) - 1):
                is_faulty = self.is_bug_fix_commit(commits[i])
                if is_faulty:
                    fault_count += 1
                versions.append((commits[i+1], is_faulty, fault_count))
                
            return versions
            
        except git.exc.GitCommandError:
            return []

    def analyze_file_history(self, file_path: str) -> Tuple[bool, Dict[str, int], int]:
        versions = self.get_file_versions(file_path)
        is_faulty = any(is_faulty for _, is_faulty, _ in versions)
        fault_count = versions[-1][2] if versions else 0
        changes = self.calculate_file_changes(file_path)
        return is_faulty, changes, fault_count

    def get_python_files(self) -> List[str]:
        python_files = []
        for root, _, files in os.walk(self.repo_path):
            for file in files:
                if file.endswith('.py'):
                    rel_path = os.path.relpath(os.path.join(root, file), self.repo_path)
                    python_files.append(rel_path)
        return python_files

    def analyze_repository(self) -> List[Tuple[str, str, int, int, int, int, int]]:
        results = []
        python_files = self.get_python_files()
        
        for file_path in python_files:
            is_faulty, changes, fault_count = self.analyze_file_history(file_path)
            results.append((
                self.remote_url, 
                file_path, 
                int(is_faulty),
                changes['TotalCommits'],
                changes['Insertions'],
                changes['Deletions'],
                fault_count
            ))
            
        return results

def process_project(project_path: str, output_dir: str):
    os.makedirs(output_dir, exist_ok=True)
    project_name = os.path.basename(project_path)
    output_file = os.path.join(output_dir, f'{project_name}_fault_proneness.csv')
    
    try:
        detector = LocalFaultDetector(project_path)
        results = detector.analyze_repository()
        
        with open(output_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Repository', 'File', 'Is_Faulty', 'TotalCommits', 'Insertions', 'Deletions', 'FaultCount'])
            for repo_url, file_path, is_faulty, total_commits, insertions, deletions, fault_count in results:
                writer.writerow([repo_url, file_path, is_faulty, total_commits, insertions, deletions, fault_count])
        
        print(f"Analysis complete for {project_name}. Processed {len(results)} files.")
        print(f"Results written to: {output_file}")
    
    except Exception as e:
        print(f"Error analyzing project {project_name}: {str(e)}")

def main():
    default_input = '.../PynoseProjects'
    default_output = '.../Fault_proneness/All_Faults'

    parser = argparse.ArgumentParser(description='Detect fault-prone files in Git repositories')
    parser.add_argument('--input_dir', 
                      help='Directory containing Git repositories',
                      default=default_input)
    parser.add_argument('--output_dir', 
                      help='Output directory path',
                      default=default_output)
    
    args = parser.parse_args()
    
    os.makedirs(args.output_dir, exist_ok=True)
    
    for project_name in os.listdir(args.input_dir):
        project_path = os.path.join(args.input_dir, project_name)
        
        if not os.path.isdir(project_path):
            continue
        
        process_project(project_path, args.output_dir)

if __name__ == "__main__":
    main()