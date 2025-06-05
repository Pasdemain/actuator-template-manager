# Actuator Template Manager

A Python application with GUI interface for managing and generating actuator templates for Excel files. This tool helps automate the creation of actuator configuration data by using reusable templates.

## Features

- **Template Management**: Create, edit, import, and export actuator templates
- **Complete Field Support**: All actuator fields supported (Name, Index, DataType, Prefix, Output, Input, Alarms, etc.)
- **Copy Functionality**: Copy existing actuators within templates and modify them
- **Multiple Output Options**:
  - 📋 Copy to clipboard (tab-separated for Excel paste)
  - 📊 Insert directly into open Excel files
  - 💾 Generate new Excel files
- **Multi-Component Actuators**: Each template can define multiple rows/components per actuator
- **Placeholder System**: Use `{ActuatorName}` placeholder for dynamic name replacement

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Pasdemain/actuator-template-manager.git
   cd actuator-template-manager
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python main.py
   ```

## Usage

### Creating Templates

1. Click **"Create New Template"**
2. Fill in template name and description
3. Add actuator components:
   - Click **"Add New Actuator"** to add components
   - Fill in all required fields (Name, Index, DataType, etc.)
   - Use `{ActuatorName}` placeholder where the actuator name should be substituted
   - Click **"Copy Selected"** to duplicate existing components and modify them
   - Use **"Move Up"/"Move Down"** to reorder components

### Using Templates

1. Select a template from the list
2. Click **"Use Template"** or double-click the template
3. Enter actuator details:
   - **Actuator Number**: Just the number (e.g., 30, 138) - underscore added automatically
   - **Actuator Name**: Name to replace placeholders (e.g., AxisX, AxisZ)
4. Click **"Generate"**

### Output Options

After generating actuator data, you can:

- **📋 Copy to Clipboard**: Copy tab-separated data for pasting into Excel
- **📊 Insert into Excel**: Directly insert into open Excel file (finds "Actuator" marker)
- **💾 Generate Excel File**: Create new Excel file with the data
- **🔍 Detect Excel Files**: See which Excel files are currently open

## Template Structure

Templates are stored as JSON files with this structure:

```json
{
  "name": "Linear Axis",
  "description": "Template for linear axis actuators",
  "actuators": [
    {
      "name": "{ActuatorName}",
      "index": 0,
      "datatype": "Act_AxisLinear",
      "alm1_descr_lang1": "{ActuatorName} Drive Error",
      // ... all other fields
    },
    {
      "name": "{ActuatorName}_AxAdm",
      "index": 1,
      "datatype": "Act_AxAdm",
      // ... more components
    }
  ]
}
```

## Example

Using the "Linear Axis" template with:
- **Actuator Number**: 30
- **Actuator Name**: AxisX

Generates 8 rows:
```
_30  AxisX               0  Act_AxisLinear     ...
_30  AxisX_AxAdm         1  Act_AxAdm         ...
_30  AxisX_AxRef         2  AXIS_CIP_DRIVE    ...
_30  AxisX_MotionCfg     3  Typ_AxLinearMotion ...
_30  AxisX_SafeJogCfg    4  Typ_AxSafeJogMotion ...
_30  AxisX_SysHMi        5  Typ_AxSiHMi       ...
_30  AxisX_NotHomed      6  Alias             ...
_30  AxisX_Interlock     7  Alias             ...
```

## Default Templates

The application comes with 3 pre-built templates:

1. **Linear Axis**: For AxisX, AxisZ type actuators (8 components)
2. **Presence Sensor**: For sensor actuators (1 component)
3. **Stepper Motor**: For AxisRy type actuators (5 components)

## Supported Fields

All Excel columns are supported:

- Actuator (auto-generated with underscore prefix)
- Name, Index, DataType, Prefix
- Output, Out.Descr., Input, Inp.Descr.
- Alm 0, Alm 1
- Alarm descriptions (3 languages each)
- Procedures, BAD flags
- Causes and Actions

## Excel Integration

### Direct Excel Insertion
- Automatically detects open Excel files
- Finds "Actuator" marker in first column
- Inserts data below the marker
- Preserves existing formatting

### Clipboard Integration
- Copies data in tab-separated format
- Ready for direct paste into Excel
- Maintains proper column alignment

## File Structure

```
actuator-template-manager/
├── main.py                 # Main application
├── template_manager.py     # Template management logic
├── template_dialog.py      # Template creation/editing GUI
├── actuator_dialog.py      # Actuator input GUI
├── excel_generator.py      # Excel generation and integration
├── requirements.txt        # Python dependencies
├── templates/             # Template storage directory
│   └── templates.json     # Templates database
└── README.md             # This file
```

## Requirements

- Python 3.7+
- tkinter (usually included with Python)
- pandas
- openpyxl
- pyperclip
- pywin32 (for Excel integration on Windows)

## Platform Support

- **Windows**: Full functionality including direct Excel integration
- **macOS/Linux**: All features except direct Excel insertion (clipboard works)

## Troubleshooting

### Excel Integration Issues
- Ensure Excel is open before using "Insert into Excel"
- Make sure your Excel file has "Actuator" in the first column
- Try "Detect Excel Files" to verify Excel is accessible

### Clipboard Issues
- If clipboard doesn't work, try the "Generate Excel File" option
- Ensure no other applications are blocking clipboard access

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

If you encounter any issues or have questions, please open an issue on GitHub.
