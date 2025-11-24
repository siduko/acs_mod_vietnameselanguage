## ADDED Requirements

### Requirement: Duplicate Language Directory Structure and Content
This requirement MUST ensure that the full directory structure and all files from the existing Thai language pack (`Language/Th`) are accurately replicated for the new Vietnamese language pack (`Language/Vi`).

#### Scenario: Duplicate Language Directory
- **Given** the existence of the `Language/Th` directory and its contents.
- **When** the "Add Vietnamese Language" feature is implemented.
- **Then** a new directory `Language/Vi` MUST be created.
- **And** all files and subdirectories from `Language/Th` MUST be copied recursively to `Language/Vi`.
- **And** the content of all copied files MUST be identical to their `Language/Th` counterparts.