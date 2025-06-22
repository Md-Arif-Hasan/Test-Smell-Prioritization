import os
import ast

def count_loc(file_path):
    """
    Count lines of code (LOC) in a Python test file.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            non_blank_lines = [line for line in lines if line.strip() != '']
            return len(non_blank_lines)
    except UnicodeDecodeError:
        # Try opening with a different encoding
        try:
            with open(file_path, 'r', encoding='latin-1') as f:
                lines = f.readlines()
                non_blank_lines = [line for line in lines if line.strip() != '']
                return len(non_blank_lines)
        except UnicodeDecodeError as e:
            print(f"Skipping file {file_path} due to encoding issues: {e}")
            return 0

def count_classes_and_methods(file_path):
    """
    Count classes (NOC), methods (NOM), and extract their names from a Python test file using AST.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read(), filename=file_path)
       
        class_count = 0
        method_count = 0
        function_count = 0

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                class_count += 1
                # For each class, get the methods
                method_names_in_class = [
                    sub_node.name for sub_node in node.body if isinstance(sub_node, ast.FunctionDef)
                ]
                method_count += len(method_names_in_class)
            elif isinstance(node, ast.FunctionDef):  # Capture standalone functions (outside of classes)
                function_count += 1

        # Combine method and standalone function counts
        total_methods = method_count + function_count

        return class_count, total_methods

    except (SyntaxError, UnicodeDecodeError) as e:
        print(f"Skipping file {file_path} due to {type(e).__name__}: {e}")
        return 0, 0

def is_test_file(file_name):
    """
    Check if the file is a test file based on common test file naming conventions.
    """
    return file_name.startswith('test_') or file_name.endswith('_test.py')

def calculate_test_metrics(project_path):
    """
    Traverse the project directory and calculate metrics for test files only.
    """
    total_test_loc = 0
    total_test_classes = 0
    total_test_methods = 0
    total_test_files = 0

    for root, _, files in os.walk(project_path):
        for file in files:
            if file.endswith('.py') and is_test_file(file):
                total_test_files += 1
                file_path = os.path.join(root, file)
               
                # Count LOC for the test file
                test_loc = count_loc(file_path)
                total_test_loc += test_loc
               
                # Count classes and methods in the test file
                test_classes, test_methods = count_classes_and_methods(file_path)
                total_test_classes += test_classes
                total_test_methods += test_methods
   
    kloc = total_test_loc / 1000  # Thousands of lines of code (Test KLOC)
   
    # Calculate averages for test files
    if total_test_files > 0:
        avg_test_loc_per_file = total_test_loc / total_test_files
        avg_test_classes_per_file = total_test_classes / total_test_files
        avg_test_methods_per_file = total_test_methods / total_test_files
    else:
        avg_test_loc_per_file = avg_test_classes_per_file = avg_test_methods_per_file = 0

    # Print the metrics
    print(f"Total Test Files: {total_test_files}")
    print(f"Total Test Lines of Code (TestLOC): {total_test_loc}")
    print(f"Total Test KLOC (Thousands of Lines of Code): {kloc:.2f}")
    print(f"Total Number of Test Classes (Test NOC): {total_test_classes}")
    print(f"Total Number of Test Methods (Test NOM): {total_test_methods}")
    print(f"Average Test LOC per file: {avg_test_loc_per_file:.2f}")
    print(f"Average Test NOC per file: {avg_test_classes_per_file:.2f}")
    print(f"Average Test NOM per file: {avg_test_methods_per_file:.2f}")

# Example usage

project_path = r'F:\\MS\\Thesis\\PyNose_projects\\PyNose Open Source Projects\\aiida-core'
calculate_test_metrics(project_path)
