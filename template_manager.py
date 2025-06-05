import json
import os
from datetime import datetime
import tkinter.messagebox as messagebox

class TemplateManager:
    def __init__(self):
        self.templates_dir = "templates"
        self.templates_file = "templates.json"
        self.ensure_templates_directory()
        self.templates = self.load_templates()
    
    def ensure_templates_directory(self):
        """Ensure templates directory exists"""
        if not os.path.exists(self.templates_dir):
            os.makedirs(self.templates_dir)
    
    def load_templates(self):
        """Load templates from JSON file"""
        templates_path = os.path.join(self.templates_dir, self.templates_file)
        if os.path.exists(templates_path):
            try:
                with open(templates_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading templates: {e}")
                return {}
        return {}
    
    def save_templates(self):
        """Save templates to JSON file"""
        templates_path = os.path.join(self.templates_dir, self.templates_file)
        try:
            with open(templates_path, 'w', encoding='utf-8') as f:
                json.dump(self.templates, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving templates: {e}")
            return False
    
    def get_all_templates(self):
        """Get all templates"""
        return self.templates
    
    def get_template(self, template_name):
        """Get specific template by name"""
        return self.templates.get(template_name)
    
    def save_template(self, template_name, template_data):
        """Save or update a template"""
        try:
            template_data["last_modified"] = datetime.now().isoformat()
            self.templates[template_name] = template_data
            return self.save_templates()
        except Exception as e:
            print(f"Error saving template: {e}")
            return False
    
    def delete_template(self, template_name):
        """Delete a template"""
        try:
            if template_name in self.templates:
                del self.templates[template_name]
                return self.save_templates()
            return False
        except Exception as e:
            print(f"Error deleting template: {e}")
            return False
    
    def import_template(self, file_path):
        """Import template from JSON file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                imported_data = json.load(f)
            
            # Check if it's a single template or multiple templates
            if isinstance(imported_data, dict):
                if "name" in imported_data:
                    # Single template
                    template_name = imported_data["name"]
                    self.templates[template_name] = imported_data
                else:
                    # Multiple templates
                    self.templates.update(imported_data)
            
            return self.save_templates()
        except Exception as e:
            print(f"Error importing template: {e}")
            return False
    
    def export_template(self, template_name, file_path):
        """Export template to JSON file"""
        try:
            if template_name in self.templates:
                template_data = self.templates[template_name]
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(template_data, f, indent=2, ensure_ascii=False)
                return True
            return False
        except Exception as e:
            print(f"Error exporting template: {e}")
            return False
    
    def create_default_templates(self):
        """Create some default templates based on the provided data"""
        
        # Linear Axis Template
        linear_axis_template = {
            "name": "Linear Axis",
            "description": "Template for linear axis actuators (AxisX, AxisZ type)",
            "created": datetime.now().isoformat(),
            "actuators": [
                {
                    "name": "{ActuatorName}",
                    "index": 0,
                    "datatype": "Act_AxisLinear",
                    "prefix": "",
                    "output": "",
                    "out_descr": "",
                    "input": "",
                    "inp_descr": "",
                    "alm0": "Alm1",
                    "alm1": "Alms.L2.",
                    "alm0_descr_lang1": "{ActuatorName} Drive Error",
                    "alm0_descr_lang2": "{ActuatorName} Drive Error",
                    "alm0_descr_lang3": "{ActuatorName} Drive Error",
                    "alm1_descr_lang1": "{ActuatorName} Position Error",
                    "alm1_descr_lang2": "{ActuatorName} Position Error",
                    "alm1_descr_lang3": "{ActuatorName} Position Error",
                    "alm0_procedure": "P200",
                    "alm1_procedure": "P201",
                    "alm0_bad": "x",
                    "alm1_bad": "x",
                    "alm0_cause": "_Linmot safety contactor not activated\\n_Linmot drive faulted or not ready\\n_Can happen after aborted fault",
                    "alm1_cause": "_Homing timeout or error\\n_Movement timeout or error\\n_Overtorque/Position error during movement\\n_Motor overheat",
                    "alm0_action": "_Acknowledge the fault and execute a reset sequence\\n_Check contactor wiring\\n_If the problem persists contact maintenance",
                    "alm1_action": "_Inspect the station, check for blockage\\n_Acknowledge the fault and execute a reset sequence\\n_If the problem persists contact maintenance"
                },
                {
                    "name": "{ActuatorName}_AxAdm",
                    "index": 1,
                    "datatype": "Act_AxAdm",
                    "prefix": "",
                    "output": "",
                    "out_descr": "",
                    "input": "",
                    "inp_descr": "",
                    "alm0": "",
                    "alm1": "",
                    "alm0_descr_lang1": "",
                    "alm0_descr_lang2": "",
                    "alm0_descr_lang3": "",
                    "alm1_descr_lang1": "",
                    "alm1_descr_lang2": "",
                    "alm1_descr_lang3": "",
                    "alm0_procedure": "",
                    "alm1_procedure": "",
                    "alm0_bad": "",
                    "alm1_bad": "",
                    "alm0_cause": "",
                    "alm1_cause": "",
                    "alm0_action": "",
                    "alm1_action": ""
                },
                {
                    "name": "{ActuatorName}_AxRef",
                    "index": 2,
                    "datatype": "AXIS_CIP_DRIVE",
                    "prefix": "",
                    "output": "",
                    "out_descr": "",
                    "input": "",
                    "inp_descr": "",
                    "alm0": "",
                    "alm1": "",
                    "alm0_descr_lang1": "",
                    "alm0_descr_lang2": "",
                    "alm0_descr_lang3": "",
                    "alm1_descr_lang1": "",
                    "alm1_descr_lang2": "",
                    "alm1_descr_lang3": "",
                    "alm0_procedure": "",
                    "alm1_procedure": "",
                    "alm0_bad": "",
                    "alm1_bad": "",
                    "alm0_cause": "",
                    "alm1_cause": "",
                    "alm0_action": "",
                    "alm1_action": ""
                },
                {
                    "name": "{ActuatorName}_NotHomed",
                    "index": 6,
                    "datatype": "Alias",
                    "prefix": "",
                    "output": "",
                    "out_descr": "",
                    "input": "",
                    "inp_descr": "",
                    "alm0": "",
                    "alm1": "Alm2",
                    "alm0_descr_lang1": "",
                    "alm0_descr_lang2": "",
                    "alm0_descr_lang3": "",
                    "alm1_descr_lang1": "{ActuatorName} Not Homed",
                    "alm1_descr_lang2": "{ActuatorName} Not Homed",
                    "alm1_descr_lang3": "{ActuatorName} Not Homed",
                    "alm0_procedure": "",
                    "alm1_procedure": "P203",
                    "alm0_bad": "",
                    "alm1_bad": "x",
                    "alm0_cause": "",
                    "alm1_cause": "_Axis homing not reached",
                    "alm0_action": "",
                    "alm1_action": "_Reset the fault and execute a homing function\\n   In case the problem persists contact maintenance\\n_Check sensor functionality"
                },
                {
                    "name": "{ActuatorName}_Interlock",
                    "index": 7,
                    "datatype": "Alias",
                    "prefix": "",
                    "output": "",
                    "out_descr": "",
                    "input": "",
                    "inp_descr": "",
                    "alm0": "",
                    "alm1": "Alm3",
                    "alm0_descr_lang1": "",
                    "alm0_descr_lang2": "",
                    "alm0_descr_lang3": "",
                    "alm1_descr_lang1": "{ActuatorName} Interlock Error",
                    "alm1_descr_lang2": "{ActuatorName} Interlock Error",
                    "alm1_descr_lang3": "{ActuatorName} Interlock Error",
                    "alm0_procedure": "",
                    "alm1_procedure": "P202",
                    "alm0_bad": "",
                    "alm1_bad": "x",
                    "alm0_cause": "",
                    "alm1_cause": "_Position not as per expected\\n   Can happen if axis moved manually\\n   Can happen after an aborted fault",
                    "alm0_action": "",
                    "alm1_action": "_Reset the fault and execute a reset sequence\\n   In case the problem persists contact maintenance"
                }
            ]
        }
        
        # Presence Sensor Template
        presence_sensor_template = {
            "name": "Presence Sensor",
            "description": "Template for presence sensor actuators",
            "created": datetime.now().isoformat(),
            "actuators": [
                {
                    "name": "{ActuatorName}",
                    "index": 0,
                    "datatype": "Act_Prs",
                    "prefix": "",
                    "output": "",
                    "out_descr": "",
                    "input": "Murr_IO:I.Data[44].{InputBit}",
                    "inp_descr": "I{InputNumber}",
                    "alm0": "",
                    "alm1": "Alms.L2.",
                    "alm0_descr_lang1": "",
                    "alm0_descr_lang2": "",
                    "alm0_descr_lang3": "",
                    "alm1_descr_lang1": "{ActuatorName} Not Present",
                    "alm1_descr_lang2": "{ActuatorName} Not Present",
                    "alm1_descr_lang3": "{ActuatorName} Not Present",
                    "alm0_procedure": "1",
                    "alm1_procedure": "0",
                    "alm0_bad": "",
                    "alm1_bad": "",
                    "alm0_cause": "_Sensor broken",
                    "alm1_cause": "_Sensor broken\\n_Part not fallen in the bin",
                    "alm0_action": "_Check sensor functionality",
                    "alm1_action": "_Check sensor functionality\\n_Inspect the station"
                }
            ]
        }
        
        # Stepper Motor Template
        stepper_template = {
            "name": "Stepper Motor",
            "description": "Template for stepper motor actuators (AxisRy type)",
            "created": datetime.now().isoformat(),
            "actuators": [
                {
                    "name": "{ActuatorName}",
                    "index": 0,
                    "datatype": "Act_Stepper_OM",
                    "prefix": "",
                    "output": "",
                    "out_descr": "",
                    "input": "",
                    "inp_descr": "",
                    "alm0": "",
                    "alm1": "Alm1",
                    "alm0_descr_lang1": "",
                    "alm0_descr_lang2": "",
                    "alm0_descr_lang3": "",
                    "alm1_descr_lang1": "{ActuatorName} Drive Error",
                    "alm1_descr_lang2": "{ActuatorName} Drive Error",
                    "alm1_descr_lang3": "{ActuatorName} Drive Error",
                    "alm0_procedure": "",
                    "alm1_procedure": "P200",
                    "alm0_bad": "",
                    "alm1_bad": "x",
                    "alm0_cause": "",
                    "alm1_cause": "_Linmot safety contactor not activated\\n_Linmot drive faulted or not ready\\n_Can happen after aborted fault",
                    "alm0_action": "",
                    "alm1_action": "_Acknowledge the fault and execute a reset sequence\\n_Check contactor wiring\\n_If the problem persists contact maintenance"
                }
            ]
        }
        
        # Save default templates
        self.save_template("Linear Axis", linear_axis_template)
        self.save_template("Presence Sensor", presence_sensor_template)
        self.save_template("Stepper Motor", stepper_template)
        
        return True
