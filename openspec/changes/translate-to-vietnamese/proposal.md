# Change: Translate to Vietnamese

## Why
To provide actual Vietnamese language support to users, improving the user experience for Vietnamese speakers and expanding the application's reach. The previous change established the infrastructure for Vietnamese language files, and this change focuses on filling those files with translated content.

## What Changes
- Translate the content of various files within the `Language/Vi` directory from Thai (placeholder) to Vietnamese. This primarily includes text strings, UI elements, and game-specific content.

## Impact
- **Affected specs**: 
    - `config-xml-modification`: The content of `Language/Config.xml` will be updated with actual Vietnamese entries (if needed, or just validated).
    - `directory-duplication`: The content within the `Language/Vi` directory will be modified through translation.
- **Affected code**: Files under `Language/Vi/` (e.g., `UIText.xml`, `CodeDictionary.txt`, `MapStoryDictionary.txt`, and various XML files under `Settings/`).
