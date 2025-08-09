# Setup Instructions for ManimDemo Project

## Quick Start

Run the setup script to create your development environment:

```bash
./setup.sh
```

## What the Setup Script Does

1. **Dependency Check**: Verifies Python 3.8+ and Git are installed
2. **Virtual Environment**: Creates a `manimgl` virtual environment
3. **Personal Packages**: Clones and installs your personal package modifications in development mode
4. **Standard Packages**: Installs all required packages from `requirements.txt`
5. **Verification**: Tests that the installation is working correctly

## Setup Script Options

- `./setup.sh` - Normal setup
- `./setup.sh --clean` - Remove existing environment and start fresh
- `./setup.sh --help` - Show help information

## Personal Package Modifications

The script automatically handles your personal package modifications:

- **ManimPM**: Your personal fork at `https://github.com/dan0326/manimPM.git`
- Installed in development mode (`pip install -e .`) so changes are reflected immediately
- Source code available in `manimgl_lib_source/` for editing

## Adding More Personal Packages

To add more personal package modifications:

1. Edit the `PERSONAL_REPOS` array in `setup.sh`
2. Add your repository: `["package_name"]="https://github.com/youruser/package.git"`
3. Re-run the setup script

## Project Structure After Setup

```
manimdemo/
├── manimgl/                 # Virtual environment
├── manimgl_lib_source/      # Personal package sources
│   └── manimPM/            # Your ManimPM fork
├── setup.sh                # Setup script
├── requirements.txt        # Standard package dependencies
├── requirements-dev.txt    # Development tools (optional)
└── setup.config           # Setup configuration
```

## Usage After Setup

### Building is Not yet implemented!!
- Below is the actual build command that works
- This need to be run  **MANUALLY** in the lib source directory, the script is acting weird on this
```
python3 -m pip install build && python3 -m build && python3 -m pip install dist/*.whl
```

### Activate Environment
```bash
source manimgl/bin/activate
```

### Run Animations
```bash
./manimgl/bin/manimgl your_script.py YourSceneName
```

### Use VS Code Tasks
- Press `Ctrl+Shift+P`
- Type "Tasks: Run Task"
- Choose "Run ManimGL" or "Test ManimGL"

## Troubleshooting

### Environment Issues
If you encounter issues, try cleaning and recreating:
```bash
./setup.sh --clean
./setup.sh
```

### Personal Package Updates
To update your personal packages:
```bash
cd manimgl_lib_source/manimPM
git pull
```

### Package Conflicts
If you have package conflicts:
1. Check `requirements.txt` for version constraints
2. Consider pinning specific versions
3. Use `pip list` to see installed packages

## Development Workflow

1. **Make Changes**: Edit files in `manimgl_lib_source/manimPM/`
2. **Test Immediately**: Changes are reflected immediately (development mode)
3. **Commit Changes**: Use Git in the source directory
4. **Push to GitHub**: Push to your personal fork

## Configuration

You can customize the setup by editing `setup.config`:
- Change virtual environment name
- Add more personal repositories
- Modify Python version requirements
- Adjust backup settings
