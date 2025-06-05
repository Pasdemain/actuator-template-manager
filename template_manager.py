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
        """Create comprehensive default templates"""
        return True
