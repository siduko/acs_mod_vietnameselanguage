
import xml.etree.ElementTree as ET
import sys
import time
import re
import subprocess
import json
import os

# --- Checkpoint Setup ---
CHECKPOINT_FILE = 'translation_checkpoint.json'
CHUNK_SIZE = 10  # Number of translations per chunk

def load_checkpoint():
    if os.path.exists(CHECKPOINT_FILE):
        with open(CHECKPOINT_FILE, 'r') as f:
            return json.load(f)
    return {'last_processed_file': None, 'last_processed_index': -1}

def save_checkpoint(filepath, index):
    with open(CHECKPOINT_FILE, 'w') as f:
        json.dump({'last_processed_file': filepath, 'last_processed_index': index}, f)

# Function to detect if a string contains Thai characters
def is_thai(text):
    if not text:
        return False
    # Thai script Unicode range
    return bool(re.search(r'[\u0E00-\u0E7F]', text))

def translate_text(text, url="http://127.0.0.1:5000/translate"):
    if not is_thai(text):
        return text, False # Return original text and a flag indicating no translation was made

    # Do not translate strings that look like placeholders
    if 'xxx' in text.lower():
        return text, False

    payload = {
        "q": text,
        "source": "th",
        "target": "vi",
        "format": "text"
    }
    try:
        cmd = [
            "curl",
            "-s",
            "-X",
            "POST",
            url,
            "-H",
            "Content-Type: application/json",
            "-d",
            json.dumps(payload)
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        translated_text = json.loads(result.stdout)["translatedText"]
        print(f"Translated '{text}' to '{translated_text}'")
        return translated_text, True
    except (subprocess.CalledProcessError, json.JSONDecodeError) as e:
        print(f"Error translating '{text}': {e}", file=sys.stderr)
        return text, False # Return original text on error

def translate_xml_file(filepath, start_index=0):
    try:
        tree = ET.parse(filepath)
        root = tree.getroot()
        
        string_tags = root.findall('string')
        total_tags = len(string_tags)

        for i in range(start_index, total_tags):
            original_text = string_tags[i].text
            if original_text:
                translated_text, translated = translate_text(original_text)
                if translated:
                    string_tags[i].text = translated_text
                    time.sleep(0.1) # small delay to not overwhelm the server

                if (i + 1) % CHUNK_SIZE == 0:
                    tree.write(filepath, encoding='utf-8', xml_declaration=True)
                    save_checkpoint(filepath, i)
                    print(f"Checkpoint saved for {filepath} at index {i}")

        # Write the final changes and clear the checkpoint for this file
        tree.write(filepath, encoding='utf-8', xml_declaration=True)
        print(f"Finished translating {filepath}")

    except ET.ParseError as e:
        print(f"Error parsing XML file {filepath}: {e}", file=sys.stderr)
    except Exception as e:
        print(f"An error occurred with {filepath}: {e}", file=sys.stderr)


def translate_txt_file(filepath, start_index=0):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        total_lines = len(lines)
        translated_lines = lines[:start_index]

        for i in range(start_index, total_lines):
            line = lines[i]
            if line.strip():
                parts = line.split('\t', 1)
                if len(parts) == 2:
                    key, value = parts
                    translated_value, translated = translate_text(value.strip())
                    if translated:
                        translated_lines.append(f"{key}\t{translated_value}\n")
                        time.sleep(0.1) # small delay
                    else:
                        translated_lines.append(line)
                else:
                    translated_lines.append(line)
            else:
                translated_lines.append(line)
            
            if (i + 1) % CHUNK_SIZE == 0:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.writelines(translated_lines)
                save_checkpoint(filepath, i)
                print(f"Checkpoint saved for {filepath} at index {i}")


        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(translated_lines)
        print(f"Finished translating {filepath}")

    except Exception as e:
        print(f"An error occurred with {filepath}: {e}", file=sys.stderr)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python translate.py <file1> <file2> ...", file=sys.stderr)
        sys.exit(1)

    files_to_translate = sys.argv[1:]
    checkpoint = load_checkpoint()
    last_file = checkpoint.get('last_processed_file')
    last_index = checkpoint.get('last_processed_index', -1)
    
    start_processing = not last_file

    for file in files_to_translate:
        if not start_processing and file == last_file:
            start_processing = True
        
        if start_processing:
            start_index = last_index + 1 if file == last_file else 0
            
            if file.endswith('.xml'):
                print(f"Translating XML file: {file}")
                translate_xml_file(file, start_index)
            elif file.endswith('.txt'):
                print(f"Translating TXT file: {file}")
                translate_txt_file(file, start_index)
            else:
                print(f"Skipping unsupported file type: {file}", file=sys.stderr)
            
            # Reset checkpoint for the next file
            last_index = -1
            save_checkpoint(file, -1) 
    
    # Clear checkpoint after all files are processed
    if os.path.exists(CHECKPOINT_FILE):
        os.remove(CHECKPOINT_FILE)
    print("All files processed.")
