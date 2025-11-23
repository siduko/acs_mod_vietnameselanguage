The project structure is organized as follows:

-   `.gemini/`: Contains configurations specific to the Gemini CLI.
-   `.git/`: Git version control metadata.
-   `.github/`: GitHub-related workflows or configurations.
-   `.idx/`: Indexing configurations (e.g., for development environments).
-   `Language/`: The core directory for language-related files.
    -   `Config.xml`: Global language configuration, defining available languages and their properties.
    -   `Vi/`: This directory currently holds all Vietnamese localization assets. It contains:
        -   `CodeDictionary.txt`: Text mappings for code-related terms.
        -   `MapStoryDictionary.txt`: Text mappings for map story elements.
        -   `UIText.xml`: User interface text definitions.
        -   `Settings/`: A comprehensive directory containing various XML and text files for specific game features, categories, and UI elements (e.g., achievements, combat, NPCs, quests, etc.). This sub-structure is highly detailed and feature-specific.
        -   `SL/`: Contains Assets and Settings, likely related to specific UI or game components.
-   `openspec/`: Documentation and tools related to change proposals and specifications for the project, including `AGENTS.md`, `project.md`, and directories for changes and specs.
-   `Resources/`: Contains supplementary resources, such as images (e.g., `viflag.png`).

The main area of focus for this project will be the `Language/Vi/` directory and `Language/Config.xml`, as these will need to be adapted for the Thai language.