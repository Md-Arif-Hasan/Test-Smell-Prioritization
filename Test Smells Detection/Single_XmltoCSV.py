import os
import xml.etree.ElementTree as ET
import csv

def convert_xml_to_csv(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    
    for filename in os.listdir(input_dir):
        if filename.endswith('.xml'):
            file_path = os.path.join(input_dir, filename)
            
            try:
                tree = ET.parse(file_path)
                root = tree.getroot()
                
                output_csv_filename = os.path.splitext(filename)[0] + '.csv'
                output_csv_path = os.path.join(output_dir, output_csv_filename)
                
                with open(output_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
                    fieldnames = [
                        'Project Name', 
                        'Module', 
                        'File Path', 
                        'Line',
                        'File Name', 
                        'Test Smell', 
                        'Severity', 
                        'Description', 
                        'Highlighted Element', 
                        'Language', 
                        'Offset', 
                        'Length'
                    ]
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    
                    for problem in root.findall('.//problem'):
                        writer.writerow({
                            'Project Name': os.path.basename(input_dir),
                            'Module': problem.find('module').text if problem.find('module') is not None else 'N/A',
                            'File Path': problem.find('file').text if problem.find('file') is not None else 'N/A',
                            'Line': problem.find('line').text if problem.find('line') is not None else 'N/A',
                            'File Name': problem.find('problem_class').get('id', 'N/A') if problem.find('problem_class') is not None else 'N/A',
                            'Test Smell': problem.find('problem_class').text if problem.find('problem_class') is not None else 'N/A',
                            'Severity': problem.find('problem_class').get('severity', 'N/A') if problem.find('problem_class') is not None else 'N/A',
                            'Description': problem.find('description').text if problem.find('description') is not None else 'N/A',
                            'Highlighted Element': problem.find('highlighted_element').text if problem.find('highlighted_element') is not None else 'N/A',
                            'Language': problem.find('language').text if problem.find('language') is not None else 'N/A',
                            'Offset': problem.find('offset').text if problem.find('offset') is not None else 'N/A',
                            'Length': problem.find('length').text if problem.find('length') is not None else 'N/A'
                        })
                
                print(f"Converted {filename} to {output_csv_filename}")
            
            except Exception as e:
                print(f"Error processing {filename}: {e}")

# Paths
input_dir = '.../aerospike-client-python'
output_dir = '.../aerospike-client-python_csv'

# Run conversion
convert_xml_to_csv(input_dir, output_dir)