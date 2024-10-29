#!/usr/bin/env python3

import argparse
import json
import os
import shutil
import sys
import yaml
import tempfile
import subprocess
import plistlib
import uuid

def write_info_plist(plist_file, prefix, suffix):
    # Dictionary containing the data to write in the plist file
    plist_content = {
        "snippetkeywordprefix": prefix,
        "snippetkeywordsuffix": suffix
    }
    
    # Writing the plist file
    try:
        with open(plist_file, 'wb') as file:
            plistlib.dump(plist_content, file)
    except Exception as e:
        print(f"Error writing the plist file: {e}")

def longest_common_suffix(strings):
    """
    Determines the longest common suffix for a list of strings
    """
    reversed_strings = [s[::-1] for s in strings]
    reversed_suffix = os.path.commonprefix(reversed_strings)
    return reversed_suffix[::-1] 

def convert_espanso_entry_to_json(entry, snippet_name, prefix, suffix, output_dir):
    """
    Converts a single espanso entry to a JSON file.
    """ 
    try:
        trigger = entry['trigger']
        snippet = entry['replace']
    except KeyError:
        print(f"Error: Invalid YAML format for entry: {entry}")
        return
    new_uid = str(uuid.uuid4()).upper()
    
    if prefix and trigger.startswith(prefix):
        trigger = trigger[len(prefix):]
    if suffix and trigger.endswith(suffix):
        trigger = trigger[:-len(suffix)]

    json_data = {
        "alfredsnippet": {
            "snippet": snippet,
            "uid": new_uid,
            "name": snippet_name,
            "keyword": trigger,
        }
    }

    try:
        json_file = os.path.join(output_dir, snippet_name)+ " [" + new_uid + "]" + ".json"
        with open(json_file, 'w', encoding='utf-8') as f:
            f.write(json.dumps(json_data, ensure_ascii=False, indent=4))
    except FileNotFoundError:
        print(f"Error: Could not create JSON file '{json_file}'.")

def convert_espanso_file_to_multiple_json(yaml_file, output_dir):
    """
    Converts an espanso with multiple entries into separate JSON files.
    """
    try:
        with open(yaml_file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Error: Could not read YAML file '{yaml_file}'.")
        sys.exit(1)

    os.makedirs(output_dir, exist_ok=True)

    data2 = data['matches']
    all_triggers = [d['trigger'] for d in data2]
    prefix = os.path.commonprefix(all_triggers)
    suffix = longest_common_suffix(all_triggers)
    plist_file = os.path.join(output_dir,"info.plist")
    write_info_plist(plist_file,prefix,suffix)

    try:
        for i, entry in enumerate(data['matches']):
            name = entry.get('label')
            if name:
                snippet_name = name
            else:
                snippet_name = entry.get('replace')[:15].replace(' ', '_').replace('\n', '_').replace('\r', '').strip(",.") +"…"
            convert_espanso_entry_to_json(entry, snippet_name, prefix, suffix, output_dir)
    except KeyError:
        print(f"Error: No 'matches' key found in '{yaml_file}'.")

def main():
    parser = argparse.ArgumentParser(
        description="Convert an espanso file to an Alfred Snippet .alfredsnippets archive."
    )
    parser.add_argument(
        'yaml_file', type=str, help="Path to the espanso file file"
    )
    parser.add_argument(
        '--icon', type=str, help="Path to a PNG file to include as 'icon.png' in the output directory"
    )

    args = parser.parse_args()

    with tempfile.TemporaryDirectory() as temp_dir: 

        convert_espanso_file_to_multiple_json(args.yaml_file, temp_dir)

        # If an icon file is provided, copy it to the temp directory as icon.png
        if args.icon:
            if not args.icon.lower().endswith('.png'):
                print("Error: The --icon file must have a .png extension.")
                sys.exit(1)
            else:
                try:
                    shutil.copy(args.icon, os.path.join(temp_dir, "icon.png"))
                except FileNotFoundError:
                    print(f"Error: Could not find the icon file '{args.icon}'.")
                except Exception as e:
                    print(f"Error: Could not copy icon file '{args.icon}': {e}")

        file_name = os.path.splitext(args.yaml_file)[0]
        output_file = f"{file_name}.alfredsnippets"
        short_name = os.path.split(output_file)[1]

        try:
            subprocess.run(['ditto', '-ck', '--rsrc', temp_dir, output_file], check=True)
            print(f"Created '{short_name}' file successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error: Failed to create .alfredsnippets archive: {e}")
            sys.exit(1)

if __name__ == "__main__":
    main()
