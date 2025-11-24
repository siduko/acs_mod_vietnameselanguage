# Design for Adding Vietnamese Language (Vi)

## Goal

The primary goal is to integrate Vietnamese (Vi) language support into the application by leveraging the existing Thai (Th) language resources as a base. This design focuses on the structural changes required for this integration, assuming that actual translation will occur in a separate effort.

## Current State Analysis

The existing language structure is organized under the `Language/` directory, with `Th/` containing all Thai-specific language files and configurations. A top-level `Config.xml` likely orchestrates which languages are available and how they are loaded. The `Info.json` file at the root of the project also appears to be a global configuration file that may need updating to announce the presence of the new language.

## Proposed Architecture for Language Integration

The approach will be to mirror the existing `Language/Th` directory structure for `Language/Vi`. This ensures consistency with the current localization pattern and minimizes disruption to existing language-loading mechanisms.

```
Language/
├───Config.xml        <-- To be updated with 'Vi' entry
└───Th/
│   └───... (existing Thai language files)
└───Vi/               <-- New directory, copy of 'Th'
    └───... (copied Thai language files, serving as placeholders for Vietnamese)
```

## Key Changes and Considerations

### 1. Directory Duplication

- **Action**: A direct copy of the `Language/Th` directory to `Language/Vi` will be performed. This includes all subdirectories and files.
- **Rationale**: This is the most straightforward way to establish the necessary file structure and provides a complete set of placeholder files that can be translated later.

### 2. `Language/Config.xml` Modification

- **Action**: An entry for the 'Vi' language will be added to `Language/Config.xml`. This entry will define the language code, display name, and potentially other language-specific metadata. The exact structure of this entry will be determined by examining the existing 'Th' entry.
- **Rationale**: This file is critical for the application to recognize and load the newly added language.

### 3. `Info.json` Modification

- **Action**: `Info.json` will be updated to include 'Vi' in its list of supported languages, if such a list exists within this file.
- **Rationale**: `Info.json` often serves as a manifest or global configuration for the application, and updating it ensures the new language is discoverable at a higher level.

### 4. CodeDictionary.txt and MapStoryDictionary.txt

- **Action**: These files will be copied as part of the directory duplication. Their content will initially be identical to the Thai versions.
- **Rationale**: These files likely contain key-value pairs for string localization or mapping, and their presence is necessary for the language system to function.

### 5. UIText.xml

- **Action**: Copied as is.
- **Rationale**: This file probably holds the majority of the UI text strings, which will serve as direct placeholders for Vietnamese until translated.

### 6. Settings Subdirectory

- **Action**: The entire `Settings` subdirectory, containing various XML and text files, will be duplicated.
- **Rationale**: These files likely contain configuration for different aspects of the game/application that are language-specific (e.g., font settings, achievement descriptions, command definitions). Duplicating them ensures all language-related settings are available for 'Vi'.

## Future Considerations (Out of Scope for this Proposal)

- **Actual Translation**: The current proposal focuses on infrastructure. Actual translation of the placeholder Thai text to Vietnamese is a separate effort.
- **Language Selection UI**: Assuming the application has a language selection interface, changes to that UI to present "Vietnamese" as an option are implied but not detailed in this design.
- **Dynamic Loading/Fallback**: If the application supports dynamic loading of language packs or has fallback mechanisms, these will need to be tested with the new 'Vi' integration.
- **Right-to-Left (RTL) Support**: If Vietnamese were an RTL language (it's not), additional UI/UX considerations would be necessary.
