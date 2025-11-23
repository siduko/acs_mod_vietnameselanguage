## MODIFIED Requirements

### Requirement: Vietnamese language files MUST contain only Vietnamese text.

**Reasoning:** The language files for the Vietnamese localization (`Language/Vi`) are intended to provide a complete and accurate translation of the game's text into Vietnamese. Some files currently contain untranslated Thai text, which breaks the user experience for Vietnamese-speaking players. This change ensures that all text within the Vietnamese language pack is consistently and correctly translated.

**Stakeholders:**
*   Vietnamese-speaking players

#### Scenario: A user playing the game in Vietnamese encounters text.

*   **Given** a player has set the game's language to Vietnamese.
*   **When** the player encounters any text in the game.
*   **Then** all displayed text should be in Vietnamese.
