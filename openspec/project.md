# Project Context

## Purpose
This project is a mod for **Amazing Cultivation Simulator (ACS)** that provides a **Vietnamese language translation**. 
It was originally based on a Thai language mod, and the goal is to translate the content from Thai (or the original Chinese/English placeholders) into Vietnamese.

## Tech Stack
- **XML**: The primary format for game data and language strings (e.g., `UIText.xml`, `Settings/**/*.xml`).
- **Python**: Used for automation scripts, specifically `translate.py` for batch translation of XML and TXT files.
- **Text Files**: Key-value pair files like `CodeDictionary.txt` and `MapStoryDictionary.txt`.

## Project Conventions

### Directory Structure
- `Language/Th`: Contains the Thai language files (serving as a reference or source for the current translation effort).
- `Language/Vi`: Contains the Vietnamese language files being developed.
- `Info.json`: Mod metadata (Name, Author, Description).

### Translation Workflow
1.  **Source**: The `Language/Vi` directory was initially duplicated from `Language/Th`.
2.  **Process**: Use `translate.py` (or manual editing) to translate content in `Language/Vi` from Thai to Vietnamese.
3.  **Verification**: Ensure XML structure remains valid and game keys are preserved.

## Active Changes
- **`translate-to-vietnamese`**: Currently working on translating all files in `Language/Vi` from Thai to Vietnamese.

## External Dependencies
- **Amazing Cultivation Simulator**: The game for which this mod is built.
- **Google Translate API** (via `translate.py`): Used for initial machine translation.