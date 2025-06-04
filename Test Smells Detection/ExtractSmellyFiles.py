import os
import shutil
from pathlib import Path
import sys

def find_test_smell_files(source_dir, dest_base_dir):
    """
    Find and copy test smell files from a project directory to its corresponding destination folder.
    
    Args:
        source_dir (str): Source project directory path
        dest_base_dir (str): Base destination directory where project folders will be created
    """
    test_smells = [
        "AssertionRoulette",
        "ConditionalTestLogic",
        "ConstructorInitialization",
        "DefaultTest",
        "DuplicateAssertion",
        "EmptyTest",
        "ExceptionHandling",
        "GeneralFixture",
        "IgnoredTest",
        "LackOfCohesionOfTestCases",
        "MagicNumberTest",
        "ObscureInLineSetup",
        "RedundantAssertion",
        "RedundantPrint",
        "SleepyTest",
        "SuboptimalAssert",
        "TestMaverick",
        "UnknownTest"
    ]
    
    try:
        project_name = os.path.basename(os.path.normpath(source_dir))
        dest_dir = os.path.join(dest_base_dir, project_name)
        os.makedirs(dest_dir, exist_ok=True)
        
        found_files = 0
        
        for root, _, files in os.walk(source_dir):
            for file in files:
                if any(smell in file for smell in test_smells):
                    try:
                        source_file = os.path.join(root, file)
                        dest_file = os.path.join(dest_dir, file)
                        
                        if os.path.abspath(source_file) != os.path.abspath(dest_file):
                            shutil.copy2(source_file, dest_file)
                            found_files += 1
                            print(f"Copied: {file} -> {project_name}")
                    except shutil.SameFileError:
                        print(f"Warning: Skipping {file} as it's the same file")
                    except PermissionError:
                        print(f"Error: Permission denied when copying {file}")
                    except Exception as e:
                        print(f"Error copying {file}: {str(e)}")
        
        if found_files > 0:
            print(f"\nProject: {project_name}")
            print(f"Total files found and copied: {found_files}")
            print(f"Files have been copied to: {dest_dir}")
            print("-" * 50)
        return found_files
    
    except Exception as e:
        print(f"Error processing project {os.path.basename(source_dir)}: {str(e)}")
        return 0

def process_multiple_projects(base_source_dir, base_dest_dir):
    """
    Process multiple projects in the source directory.
    
    Args:
        base_source_dir (str): Base directory containing all project folders
        base_dest_dir (str): Base directory where test smell files will be organized
    """
    try:
        os.makedirs(base_dest_dir, exist_ok=True)
        
        # Get list of project directories
        project_dirs = [d for d in os.listdir(base_source_dir) 
                       if os.path.isdir(os.path.join(base_source_dir, d))]
        
        total_projects = len(project_dirs)
        total_files = 0
        processed_projects = 0
        
        print(f"Found {total_projects} projects to process")
        print("=" * 50)
        
        for project in project_dirs:
            try:
                source_dir = os.path.join(base_source_dir, project)
                files_found = find_test_smell_files(source_dir, base_dest_dir)
                total_files += files_found
                if files_found > 0:
                    processed_projects += 1
            except Exception as e:
                print(f"Error processing project {project}: {str(e)}")
        
        print("\nFinal Summary:")
        print(f"Total projects found: {total_projects}")
        print(f"Projects with smell files: {processed_projects}")
        print(f"Total smell files found: {total_files}")
        print(f"Results stored in: {base_dest_dir}")
        
    except Exception as e:
        print(f"Critical error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    # Base directory containing all projects
    base_source_directory = "/home/iit/Downloads/Thesis/Smells_Dataset"
    
    # Updated destination directory path
    base_destination_directory = "/home/iit/Downloads/Thesis/TEST_SMELL_EXTRACT"
    
    process_multiple_projects(base_source_directory, base_destination_directory)