# Copilot Instructions - Kontrollzentrum Modules

## Project Overview
This is the `modules/` directory of the Kontrollzentrum (Control Center) project. Each Python file in this directory represents a standalone module that can be loaded and executed by the main control center system.

## Module Architecture
- **Location**: All modules reside in `c:\Users\Laptop\Kontrollzentrum-1\modules\`
- **Naming**: Modules follow the pattern `*_modul.py` (e.g., `beispiel_modul.py`)
- **Language**: Python-based modules

## Development Conventions

### Module Structure
Each module should follow a consistent structure:
- Define clear entry points for the control center to invoke
- Keep modules self-contained with minimal cross-dependencies
- Use descriptive names ending in `_modul.py`

### Building & Testing
- The workspace includes a .NET build task (`dotnet build`) - verify if Python modules integrate with .NET components
- Test modules independently before integration with the main Kontrollzentrum system

### File Organization
```
modules/
├── beispiel_modul.py    # Example/template module
└── [other]_modul.py     # Additional modules
```

## Key Considerations for AI Agents

1. **Module Independence**: Modules should be designed to work independently
2. **Shell Environment**: Default shell is PowerShell (pwsh.exe) - use PowerShell syntax for commands
3. **Mixed Stack**: Note the presence of both Python modules and .NET build configuration
4. **German Context**: Project name is German ("Kontrollzentrum", "beispiel") - expect German naming conventions

## Questions to Clarify
- What is the expected interface/API for modules to implement?
- How does the main Kontrollzentrum system load and interact with these modules?
- Are there shared utilities or base classes modules should inherit from?
- What is the relationship between Python modules and the .NET build system?
