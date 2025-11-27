import xml.etree.ElementTree as ET
import sys
import time
import re
import subprocess
import json
import os
import multiprocessing

# --- Checkpoint Setup ---
BATCH_SIZE = 100  # Number of translations per chunk
CHECKPOINT_DIR = 'tmp/.checkpoints'

def get_checkpoint_path(filepath):
    if not os.path.exists(CHECKPOINT_DIR):
        try:
            os.makedirs(CHECKPOINT_DIR, exist_ok=True)
        except OSError:
            pass

    # Generate a unique safe filename based on the absolute path
    safe_name = re.sub(r'[\\/:]', '_', os.path.abspath(filepath)).lstrip('_')
    return os.path.join(CHECKPOINT_DIR, f"{safe_name}.checkpoint.json")

def load_checkpoint(filepath):
    ckpt_path = get_checkpoint_path(filepath)
    if os.path.exists(ckpt_path):
        try:
            with open(ckpt_path, 'r') as f:
                data = json.load(f)
                return data.get('last_index', -1)
        except Exception as e:
            print(f"Error loading checkpoint for {filepath}: {e}", file=sys.stderr)
    return -1

def save_checkpoint(filepath, index):
    ckpt_path = get_checkpoint_path(filepath)
    try:
        with open(ckpt_path, 'w') as f:
            json.dump({'last_index': index}, f)
    except Exception as e:
        print(f"Error saving checkpoint for {filepath}: {e}", file=sys.stderr)

def remove_checkpoint(filepath):
    ckpt_path = get_checkpoint_path(filepath)
    if os.path.exists(ckpt_path):
        try:
            os.remove(ckpt_path)
        except OSError as e:
            print(f"Error removing checkpoint {ckpt_path}: {e}", file=sys.stderr)

# Function to detect if a string contains Thai characters
def is_thai(text):
    if not text:
        return False
    # Thai script Unicode range
    return bool(re.search(r'[\u0E00-\u0E7F]', text))

def should_translate(text):
    if not is_thai(text):
        return False
    # Do not translate strings that look like placeholders
    if 'xxx' in text.lower():
        return False
    return True

def translate_batch(texts, url="http://127.0.0.1:5000/translate"):
    if not texts:
        return []

    payload = {
        "q": texts,
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
        response = json.loads(result.stdout)
        
        # Handle various response formats
        if "translatedText" in response:
            translated = response["translatedText"]
            if isinstance(translated, list):
                return translated
            else:
                return [translated]
        elif isinstance(response, list):
             return [item.get("translatedText", "") for item in response]
        else:
            print(f"Unexpected response format: {response}", file=sys.stderr)
            return texts # Fallback

    except (subprocess.CalledProcessError, json.JSONDecodeError) as e:
        print(f"Error translating batch: {e}", file=sys.stderr)
        return texts # Return original texts on error

def translate_xml_file(filepath, start_index=0):
    try:
        tree = ET.parse(filepath)
        root = tree.getroot()
        
        string_tags = root.findall('string')
        total_tags = len(string_tags)
        
        pending_batch = [] # List of (index, text)

        for i in range(start_index, total_tags):
            original_text = string_tags[i].text
            if original_text and should_translate(original_text):
                pending_batch.append((i, original_text))

            # Process batch if full or last item
            is_last = (i == total_tags - 1)
            if len(pending_batch) >= BATCH_SIZE or (is_last and pending_batch):
                texts = [t for _, t in pending_batch]
                translated_texts = translate_batch(texts)
                
                if len(translated_texts) == len(pending_batch):
                    for idx, (tag_index, _) in enumerate(pending_batch):
                        string_tags[tag_index].text = translated_texts[idx]
                    print(f"[{filepath}] Translated batch of {len(texts)} items")
                else:
                    print(f"[{filepath}] Warning: Batch size mismatch. Expected {len(pending_batch)}, got {len(translated_texts)}", file=sys.stderr)

                pending_batch = []
                time.sleep(0.1) # small delay

            if (i + 1) % BATCH_SIZE == 0 or is_last:
                tree.write(filepath, encoding='utf-8', xml_declaration=True)
                save_checkpoint(filepath, i)
                # print(f"[{filepath}] Checkpoint saved at index {i}")

        # Final write
        tree.write(filepath, encoding='utf-8', xml_declaration=True)
        print(f"Finished translating {filepath}")
        remove_checkpoint(filepath)

    except ET.ParseError as e:
        print(f"Error parsing XML file {filepath}: {e}", file=sys.stderr)
    except Exception as e:
        print(f"An error occurred with {filepath}: {e}", file=sys.stderr)


def translate_txt_file(filepath, start_index=0):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        total_lines = len(lines)
        pending_batch = [] # List of (line_index, value_text)

        for i in range(start_index, total_lines):
            line = lines[i]
            if line.strip():
                parts = line.split('\t', 1)
                if len(parts) == 2:
                    key, value = parts
                    value_stripped = value.strip()
                    if should_translate(value_stripped):
                        pending_batch.append((i, value_stripped))
            
            is_last = (i == total_lines - 1)
            if len(pending_batch) >= BATCH_SIZE or (is_last and pending_batch):
                texts = [t for _, t in pending_batch]
                translated_texts = translate_batch(texts)

                if len(translated_texts) == len(pending_batch):
                    for idx, (line_index, _) in enumerate(pending_batch):
                        original_line = lines[line_index]
                        key = original_line.split('\t', 1)[0]
                        lines[line_index] = f"{key}\t{translated_texts[idx]}\n"
                    print(f"[{filepath}] Translated batch of {len(texts)} items")
                else:
                    print(f"[{filepath}] Warning: Batch size mismatch", file=sys.stderr)
                
                pending_batch = []
                time.sleep(0.1)
            
            if (i + 1) % BATCH_SIZE == 0 or is_last:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.writelines(lines)
                save_checkpoint(filepath, i)
                # print(f"[{filepath}] Checkpoint saved at index {i}")

        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        print(f"Finished translating {filepath}")
        remove_checkpoint(filepath)

    except Exception as e:
        print(f"An error occurred with {filepath}: {e}", file=sys.stderr)

def process_file(filepath):
    print(f"Starting process for: {filepath}")
    start_index = load_checkpoint(filepath) + 1
    
    if start_index > 0:
        print(f"Resuming {filepath} from index {start_index}")

    if filepath.endswith('.xml'):
        translate_xml_file(filepath, start_index)
    elif filepath.endswith('.txt'):
        translate_txt_file(filepath, start_index)
    else:
        print(f"Skipping unsupported file type: {filepath}", file=sys.stderr)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python translate.py <file1> <file2> ...", file=sys.stderr)
        sys.exit(1)

    files_to_translate = sys.argv[1:]
    print(f"Files to translate: {files_to_translate}")
    
    # Determine number of processes, cap at 8 or CPU count
    num_processes = min(len(files_to_translate), os.cpu_count() or 1, 8)
    print(f"Starting translation with {num_processes} processes...")

    with multiprocessing.Pool(processes=num_processes) as pool:
        pool.map(process_file, files_to_translate)
    
    print("All files processed.")