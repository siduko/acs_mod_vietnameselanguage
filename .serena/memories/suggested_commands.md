**General Workflow Commands:**

*   `ls -F`: List files and directories in the current directory.
*   `ls -F <dir>`: List files and directories in a specified directory.
*   `cd <dir>`: Change the current directory.
*   `cd ..`: Move up one directory.
*   `grep -r "search_string" .`: Search for "search_string" recursively in the current directory. Useful for finding specific text within the localization files.
*   `find . -name "*.xml"`: Find all XML files in the current directory and its subdirectories.

**Git Commands:**

*   `git status`: Check the status of the Git repository.
*   `git diff`: Show changes between commits, commit and working tree, etc.
*   `git add <file>`: Stage changes for the next commit.
*   `git commit -m "Commit message"`: Commit staged changes.
*   `git log`: View commit history.

**Project-Specific Commands (Inferred):**

*   **No specific build, test, or run commands are identified** as this project is a language modification pack. The "testing" of changes will likely occur by loading the modified language pack into the target game.

**Important Considerations:**

*   When modifying language files, always ensure consistent text encoding (likely UTF-8).
*   Backup files before making significant changes.