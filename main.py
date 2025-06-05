import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
from datetime import datetime
import pandas as pd
from template_manager import TemplateManager
from excel_generator import ExcelGenerator

class ActuatorTemplateApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Actuator Template Manager")
        self.root.geometry("800x600")
        
        # Initialize managers
        self.template_manager = TemplateManager()
        self.excel_generator = ExcelGenerator()
        
        # Create GUI
        self.create_widgets()
        self.load_templates()
        
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Actuator Template Manager", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Template management section
        template_frame = ttk.LabelFrame(main_frame, text="Template Management", padding="10")
        template_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        template_frame.columnconfigure(1, weight=1)
        
        # New template button
        ttk.Button(template_frame, text="Create New Template", 
                  command=self.create_new_template).grid(row=0, column=0, padx=(0, 10))
        
        # Import template button
        ttk.Button(template_frame, text="Import Template", 
                  command=self.import_template).grid(row=0, column=1, padx=(0, 10))
        
        # Export template button
        ttk.Button(template_frame, text="Export Template", 
                  command=self.export_template).grid(row=0, column=2)
        
        # Templates list
        list_frame = ttk.LabelFrame(main_frame, text="Available Templates", padding="10")
        list_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        # Treeview for templates
        self.templates_tree = ttk.Treeview(list_frame, columns=("description", "actuators"), show="tree headings")
        self.templates_tree.heading("#0", text="Template Name")
        self.templates_tree.heading("description", text="Description")
        self.templates_tree.heading("actuators", text="Actuators Count")
        
        # Scrollbar for treeview
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.templates_tree.yview)
        self.templates_tree.configure(yscrollcommand=scrollbar.set)
        
        self.templates_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Bind double click to template
        self.templates_tree.bind("<Double-1>", self.on_template_double_click)
        
        # Action buttons
        action_frame = ttk.Frame(main_frame)
        action_frame.grid(row=3, column=0, columnspan=3, pady=(0, 10))
        
        ttk.Button(action_frame, text="Use Template", 
                  command=self.use_template).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(action_frame, text="Edit Template", 
                  command=self.edit_template).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(action_frame, text="Delete Template", 
                  command=self.delete_template).pack(side=tk.LEFT, padx=(0, 10))
        
        # Generate Excel button
        generate_frame = ttk.Frame(main_frame)
        generate_frame.grid(row=4, column=0, columnspan=3)
        
        ttk.Button(generate_frame, text="Generate Excel File", 
                  command=self.generate_excel, 
                  style="Accent.TButton").pack()
        
    def load_templates(self):
        """Load templates into the treeview"""
        # Clear existing items
        for item in self.templates_tree.get_children():
            self.templates_tree.delete(item)
            
        # Load templates from manager
        templates = self.template_manager.get_all_templates()
        
        for template_name, template_data in templates.items():
            description = template_data.get("description", "No description")
            actuator_count = len(template_data.get("actuators", []))
            
            self.templates_tree.insert("", "end", iid=template_name, text=template_name,
                                     values=(description, actuator_count))
    
    def create_new_template(self):
        """Open dialog to create a new template"""
        from template_dialog import TemplateDialog
        
        dialog = TemplateDialog(self.root, "Create New Template")
        if dialog.result:
            template_name = dialog.result["name"]
            if self.template_manager.save_template(template_name, dialog.result):
                self.load_templates()
                messagebox.showinfo("Success", f"Template '{template_name}' created successfully!")
            else:
                messagebox.showerror("Error", "Failed to create template")
    
    def import_template(self):
        """Import template from JSON file"""
        file_path = filedialog.askopenfilename(
            title="Import Template",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if file_path:
            if self.template_manager.import_template(file_path):
                self.load_templates()
                messagebox.showinfo("Success", "Template imported successfully!")
            else:
                messagebox.showerror("Error", "Failed to import template")
    
    def export_template(self):
        """Export selected template to JSON file"""
        selected = self.templates_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a template to export")
            return
            
        template_name = selected[0]
        file_path = filedialog.asksaveasfilename(
            title="Export Template",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if file_path:
            if self.template_manager.export_template(template_name, file_path):
                messagebox.showinfo("Success", "Template exported successfully!")
            else:
                messagebox.showerror("Error", "Failed to export template")
    
    def on_template_double_click(self, event):
        """Handle double click on template"""
        self.use_template()
    
    def use_template(self):
        """Use selected template to generate actuators"""
        selected = self.templates_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a template to use")
            return
            
        template_name = selected[0]
        from actuator_dialog import ActuatorDialog
        
        dialog = ActuatorDialog(self.root, template_name, self.template_manager)
        if dialog.result:
            # Store generated actuators for Excel generation
            self.generated_actuators = dialog.result
            messagebox.showinfo("Success", f"Generated {len(dialog.result)} actuators from template!")
    
    def edit_template(self):
        """Edit selected template"""
        selected = self.templates_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a template to edit")
            return
            
        template_name = selected[0]
        template_data = self.template_manager.get_template(template_name)
        
        from template_dialog import TemplateDialog
        
        dialog = TemplateDialog(self.root, "Edit Template", template_data)
        if dialog.result:
            if self.template_manager.save_template(template_name, dialog.result):
                self.load_templates()
                messagebox.showinfo("Success", f"Template '{template_name}' updated successfully!")
            else:
                messagebox.showerror("Error", "Failed to update template")
    
    def delete_template(self):
        """Delete selected template"""
        selected = self.templates_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a template to delete")
            return
            
        template_name = selected[0]
        
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete template '{template_name}'?"):
            if self.template_manager.delete_template(template_name):
                self.load_templates()
                messagebox.showinfo("Success", f"Template '{template_name}' deleted successfully!")
            else:
                messagebox.showerror("Error", "Failed to delete template")
    
    def generate_excel(self):
        """Generate Excel file from generated actuators"""
        if not hasattr(self, 'generated_actuators') or not self.generated_actuators:
            messagebox.showwarning("Warning", "No actuators generated. Please use a template first.")
            return
            
        file_path = filedialog.asksaveasfilename(
            title="Save Excel File",
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
        )
        
        if file_path:
            if self.excel_generator.generate_excel(self.generated_actuators, file_path):
                messagebox.showinfo("Success", f"Excel file generated successfully!\nSaved to: {file_path}")
            else:
                messagebox.showerror("Error", "Failed to generate Excel file")

if __name__ == "__main__":
    root = tk.Tk()
    app = ActuatorTemplateApp(root)
    root.mainloop()
