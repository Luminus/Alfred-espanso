import os
import plistlib
import json
import yaml
import zipfile
import tempfile
import argparse

def extract_archive(archive_path):
    # Create a temporary directory for extraction
    temp_dir = tempfile.mkdtemp()
    with zipfile.ZipFile(archive_path, 'r') as zip_ref:
        zip_ref.extractall(temp_dir)
    return temp_dir

def extract_prefix_suffix(folder):
    # Full path to the info.plist file
    info_plist_path = os.path.join(folder, "info.plist")

    # Check if the info.plist file exists in the folder
    if not os.path.isfile(info_plist_path):
        return "", ""
    
    # Read the info.plist file to extract 'suffix' and 'prefix' keys
    try:
        with open(info_plist_path, 'rb') as file:
            # Load plist content
            plist_content = plistlib.load(file)
            
            # Extract values for 'suffix' and 'prefix' keys if they exist
            prefix = plist_content.get("snippetkeywordprefix", "")
            suffix = plist_content.get("snippetkeywordsuffix", "")
            return prefix, suffix
    except Exception as e:
        print(f"Error reading 'info.plist': {e}")
        return "", ""

def convert_json_to_yaml(input_file, output_file):

    # Check if the output file already exists
    if os.path.isfile(output_file):
        print(f"Error: {output_file} already exists.")
        return False

    # Extract files from the archive
    input_folder = extract_archive(input_file)
    matches = []
    prefix, suffix = extract_prefix_suffix(input_folder)

    # Loop through the files in the extracted folder
    for filename in os.listdir(input_folder):
        file_path = os.path.join(input_folder, filename)
        # Check if it is a JSON file
        if filename.endswith('.json') and os.path.isfile(file_path):
            with open(file_path, 'r', encoding='utf-8') as json_file:
                try:
                    data = json.load(json_file)
                    snippet_data = data.get("alfredsnippet")
                    if snippet_data:
                        # Transform the data
                        match = {
                            'replace': snippet_data.get("snippet").strip(),
                            "trigger": prefix + snippet_data.get("keyword").strip() + suffix,
                            "label": snippet_data.get("name")
                        }
                        matches.append(match)
                except json.JSONDecodeError as e:
                    print(f"Error loading {filename}: {e}")


    # Write the data to the YAML file with double quotes
    with open(output_file, 'w', encoding='utf-8') as yaml_file:
        yaml.dump({'matches': matches}, yaml_file, allow_unicode=True, default_flow_style=False, default_style='',  sort_keys=False)

    # Clean up: remove the temporary folder
    for filename in os.listdir(input_folder):
        file_path = os.path.join(input_folder, filename)
        os.remove(file_path)
    os.rmdir(input_folder)

    return True

if __name__ == "__main__":
    # Argument parser for command line arguments
    parser = argparse.ArgumentParser(description='Convert .alfredsnippet archive to YAML format.')
    parser.add_argument('input_file', type=str, help='Path of the .alfredsnippet file')
    
    args = parser.parse_args()    

    # Generate output file name
    file_name = os.path.splitext(args.input_file)[0]
    output_file = f"{file_name}.yml"
    short_name = os.path.split(output_file)[1]

    # Check if the input path is a file
    if not os.path.isfile(args.input_file) or not args.input_file.endswith('.alfredsnippets'):
        print(f"Error: the file \"{input_filename}\" is not a valid .alfredsnippets file.")
    else:
        if convert_json_to_yaml(args.input_file, output_file):
            print(f"Created '{short_name}' file successfully.")

