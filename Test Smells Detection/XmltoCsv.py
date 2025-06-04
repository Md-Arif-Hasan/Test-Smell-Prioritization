

import xml.etree.ElementTree as ET
import csv
import os
import glob
from pathlib import Path

def convert_xml_to_csv(input_file, output_file):
    """
    Convert a single XML file containing test smell data to CSV format.
    
    Args:
        input_file (str): Path to input XML file
        output_file (str): Path for output CSV file
    """
    try:
        # Parse XML file
        tree = ET.parse(input_file)
        root = tree.getroot()
        
        # Define CSV headers
        headers = ['file', 'line', 'module', 'problem_class_id', 'severity', 
                  'description', 'highlighted_element', 'language', 'offset', 'length']
        
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        # Open CSV file for writing
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            writer.writeheader()
            
            # Process each problem in the XML
            for problem in root.findall('.//problem'):
                row = {
                    'file': problem.find('file').text.replace('file://$PROJECT_DIR$/', ''),
                    'line': problem.find('line').text,
                    'module': problem.find('module').text,
                    'problem_class_id': problem.find('problem_class').get('id'),
                    'severity': problem.find('problem_class').get('severity'),
                    'description': problem.find('description').text,
                    'highlighted_element': problem.find('highlighted_element').text,
                    'language': problem.find('language').text,
                    'offset': problem.find('offset').text,
                    'length': problem.find('length').text
                }
                writer.writerow(row)
        
        return True, None
    except Exception as e:
        return False, str(e)

def process_folder_structure(base_input_dir, base_output_dir):
    """
    Process all folders and XML files in the input directory structure and create
    corresponding CSV files in the output directory structure.
    
    Args:
        base_input_dir (str): Base directory containing folders with XML files
        base_output_dir (str): Base directory for output CSV folder structure
    """
    # Convert paths to Path objects
    base_input_path = Path(base_input_dir)
    base_output_path = Path(base_output_dir)
    
    # Create base output directory if it doesn't exist
    os.makedirs(base_output_path, exist_ok=True)
    
    # Keep track of statistics
    total_files = 0
    successful_conversions = 0
    failed_conversions = 0
    processed_folders = 0
    
    print(f"Starting conversion process...")
    print(f"Input directory: {base_input_path}")
    print(f"Output directory: {base_output_path}")
    
    # Walk through all subdirectories
    for folder_path, _, files in os.walk(base_input_path):
        xml_files = [f for f in files if f.endswith('.xml')]
        
        if xml_files:
            processed_folders += 1
            relative_path = Path(folder_path).relative_to(base_input_path)
            output_folder = base_output_path / relative_path
            
            print(f"\nProcessing folder: {relative_path}")
            
            # Process each XML file in the current folder
            for xml_file in xml_files:
                total_files += 1
                input_file = Path(folder_path) / xml_file
                output_file = output_folder / f"{xml_file[:-4]}.csv"
                
                print(f"Converting: {xml_file}")
                success, error = convert_xml_to_csv(input_file, output_file)
                
                if success:
                    successful_conversions += 1
                else:
                    failed_conversions += 1
                    print(f"Error converting {xml_file}: {error}")
    
    # Print summary
    print("\nConversion Summary:")
    print(f"Processed folders: {processed_folders}")
    print(f"Total files processed: {total_files}")
    print(f"Successful conversions: {successful_conversions}")
    print(f"Failed conversions: {failed_conversions}")

if __name__ == "__main__":
    input_dir = ".../TEST_SMELL_EXTRACT"
    output_dir = ".../TEST_SMELL_EXTRACT_CSV"
    
    process_folder_structure(input_dir, output_dir)