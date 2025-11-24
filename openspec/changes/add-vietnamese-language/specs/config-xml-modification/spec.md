## MODIFIED Requirements

### Requirement: Vietnamese Language Entry in Config.xml
This requirement MUST detail the expected state of the `Language/Config.xml` file after the addition of the Vietnamese language, ensuring the 'Vi' entry is correctly defined.

#### Scenario: Ensure Vietnamese Language Entry in Config.xml
- **Given** the `Language/Config.xml` file exists.
- **When** the "Add Vietnamese Language" feature is implemented.
- **Then** the `Config.xml` file MUST contain a `<Language>` entry with `Name="Vi"`.
- **And** this `Vi` entry MUST have `<DisplayName>Tiếng Việt</DisplayName>`.
- **And** this `Vi` entry MUST have `<Icon>viflag.png</Icon>`.
- **And** this `Vi` entry MUST have `<UIMode>1</UIMode>`.
- **And** this `Vi` entry MUST have `<Desc>Vietnamese Language</Desc>`.
- **And** this `Vi` entry MUST have `<SpaceConnect>true</SpaceConnect>`.
- **And** this `Vi` entry MUST have `<FamilyPostposition>false</FamilyPostposition>`.
- **And** this `Vi` entry MUST have the same `<Labels>` section as the `Th` entry.