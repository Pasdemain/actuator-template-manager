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
        self.root.geometry("900x700")
        
        # Initialize managers
        self.template_manager = TemplateManager()
        self.excel_generator = ExcelGenerator()
        
        # Generated actuators storage
        self.generated_actuators = None
        
        # Create GUI
        self.create_widgets()
        self.load_templates()
        
        # Create default templates if none exist
        if not self.template_manager.get_all_templates():
            self.template_manager.create_default_templates()
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
                  command=self.export_template).grid(row=0, column=2, padx=(0, 10))
        
        # Export Excel template button
        ttk.Button(template_frame, text="Export Excel Template", 
                  command=self.export_excel_template).grid(row=0, column=3)
        
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
        
        # Configure column widths
        self.templates_tree.column("#0", width=200)
        self.templates_tree.column("description", width=300)
        self.templates_tree.column("actuators", width=150)
        
        # Scrollbar for treeview
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.templates_tree.yview)
        self.templates_tree.configure(yscrollcommand=scrollbar.set)
        
        self.templates_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Bind double click to template
        self.templates_tree.bind("<Double-1>", self.on_template_double_click)
        
        # Template action buttons
        template_action_frame = ttk.Frame(main_frame)
        template_action_frame.grid(row=3, column=0, columnspan=3, pady=(0, 10))
        
        ttk.Button(template_action_frame, text="Use Template", 
                  command=self.use_template).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(template_action_frame, text="Edit Template", 
                  command=self.edit_template).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(template_action_frame, text="Delete Template", 
                  command=self.delete_template).pack(side=tk.LEFT, padx=(0, 10))
        
        # Generated data section
        self.generated_frame = ttk.LabelFrame(main_frame, text="Generated Actuator Data", padding="10")
        self.generated_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Info label for generated data
        self.generated_info_label = ttk.Label(self.generated_frame, 
                                            text="No actuator data generated yet. Use a template first.",
                                            foreground="gray")
        self.generated_info_label.grid(row=0, column=0, columnspan=4, pady=(0, 10))
        
        # Action buttons for generated data (initially hidden)
        self.copy_clipboard_btn = ttk.Button(self.generated_frame, text="📋 Copy to Clipboard", 
                                           command=self.copy_to_clipboard, state=tk.DISABLED)
        self.copy_clipboard_btn.grid(row=1, column=0, padx=(0, 10))
        
        self.insert_excel_btn = ttk.Button(self.generated_frame, text="📊 Insert into Excel", 
                                         command=self.insert_into_excel, state=tk.DISABLED)
        self.insert_excel_btn.grid(row=1, column=1, padx=(0, 10))
        
        self.generate_excel_btn = ttk.Button(self.generated_frame, text="💾 Generate Excel File", 
                                           command=self.generate_excel_file, state=tk.DISABLED)
        self.generate_excel_btn.grid(row=1, column=2, padx=(0, 10))
        
        self.detect_excel_btn = ttk.Button(self.generated_frame, text="🔍 Detect Excel Files", 
                                         command=self.detect_excel_files, state=tk.DISABLED)
        self.detect_excel_btn.grid(row=1, column=3)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
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
                self.status_var.set(f"Template '{template_name}' created successfully!")
                messagebox.showinfo("Success", f"Template '{template_name}' created successfully!")
            else:
                self.status_var.set("Failed to create template")
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
                self.status_var.set("Template imported successfully!")
                messagebox.showinfo("Success", "Template imported successfully!")
            else:
                self.status_var.set("Failed to import template")
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
                self.status_var.set("Template exported successfully!")
                messagebox.showinfo("Success", "Template exported successfully!")
            else:
                self.status_var.set("Failed to export template")
                messagebox.showerror("Error", "Failed to export template")
    
    def export_excel_template(self):
        """Export Excel template file"""
        file_path = filedialog.asksaveasfilename(
            title="Export Excel Template",
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
        )
        
        if file_path:
            if self.excel_generator.export_template_excel(file_path):
                self.status_var.set("Excel template exported successfully!")
                messagebox.showinfo("Success", "Excel template exported successfully!")
            else:
                self.status_var.set("Failed to export Excel template")
                messagebox.showerror("Error", "Failed to export Excel template")
    
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
            
            # Update UI to show generated data options
            self.update_generated_data_ui()
            
            rows_count = sum(len(actuator['actuators']) for actuator in dialog.result)
            self.status_var.set(f"Generated {rows_count} rows from {len(dialog.result)} actuator(s)")
            messagebox.showinfo("Success", f"Generated {rows_count} rows from template '{template_name}'!")
    
    def update_generated_data_ui(self):
        """Update UI to show options for generated data"""
        if self.generated_actuators:
            rows_count = sum(len(actuator['actuators']) for actuator in self.generated_actuators)
            actuators_count = len(self.generated_actuators)
            
            self.generated_info_label.config(
                text=f"Generated {rows_count} rows from {actuators_count} actuator(s). Ready to export.",
                foreground="green"
            )
            
            # Enable action buttons
            self.copy_clipboard_btn.config(state=tk.NORMAL)
            self.insert_excel_btn.config(state=tk.NORMAL)
            self.generate_excel_btn.config(state=tk.NORMAL)
            self.detect_excel_btn.config(state=tk.NORMAL)
        else:
            self.generated_info_label.config(
                text="No actuator data generated yet. Use a template first.",
                foreground="gray"
            )
            
            # Disable action buttons
            self.copy_clipboard_btn.config(state=tk.DISABLED)
            self.insert_excel_btn.config(state=tk.DISABLED)
            self.generate_excel_btn.config(state=tk.DISABLED)
            self.detect_excel_btn.config(state=tk.DISABLED)
    
    def copy_to_clipboard(self):
        """Copy generated data to clipboard"""
        if not self.generated_actuators:
            messagebox.showwarning("Warning", "No data to copy. Generate actuators first.")
            return
        
        success, message = self.excel_generator.copy_to_clipboard(self.generated_actuators)
        
        if success:
            self.status_var.set("Data copied to clipboard!")
            messagebox.showinfo("Success", message)
        else:
            self.status_var.set("Failed to copy to clipboard")
            messagebox.showerror("Error", message)
    
    def insert_into_excel(self):
        """Insert generated data into open Excel file"""
        if not self.generated_actuators:
            messagebox.showwarning("Warning", "No data to insert. Generate actuators first.")
            return
        
        success, message = self.excel_generator.insert_into_excel(self.generated_actuators)
        
        if success:
            self.status_var.set("Data inserted into Excel!")
            messagebox.showinfo("Success", message)
        else:
            self.status_var.set("Failed to insert into Excel")
            messagebox.showerror("Error", message)
    
    def generate_excel_file(self):
        """Generate new Excel file with generated data"""
        if not self.generated_actuators:
            messagebox.showwarning("Warning", "No data to export. Generate actuators first.")
            return
            
        file_path = filedialog.asksaveasfilename(
            title="Save Excel File",
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
        )
        
        if file_path:
            if self.excel_generator.generate_excel_file(self.generated_actuators, file_path):
                self.status_var.set(f"Excel file saved to {file_path}")
                messagebox.showinfo("Success", f"Excel file generated successfully!\nSaved to: {file_path}")
            else:
                self.status_var.set("Failed to generate Excel file")
                messagebox.showerror("Error", "Failed to generate Excel file")
    
    def detect_excel_files(self):
        """Detect and show open Excel files"""
        success, result = self.excel_generator.detect_excel_files()
        
        if success:
            if result:
                info_text = "Open Excel files:\n\n"
                for workbook in result:
                    info_text += f"📁 {workbook['name']}\n"
                    info_text += f"   Path: {workbook['path']}\n"
                    info_text += f"   Sheets: {', '.join(workbook['sheets'])}\n\n"
                
                messagebox.showinfo("Excel Files Detected", info_text)
            else:
                messagebox.showinfo("No Excel Files", "No open Excel files detected.")
        else:
            messagebox.showerror("Error", result)
    
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
                self.status_var.set(f"Template '{template_name}' updated successfully!")
                messagebox.showinfo("Success", f"Template '{template_name}' updated successfully!")
            else:
                self.status_var.set("Failed to update template")
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
                self.status_var.set(f"Template '{template_name}' deleted successfully!")
                messagebox.showinfo("Success", f"Template '{template_name}' deleted successfully!")
            else:
                self.status_var.set("Failed to delete template")
                messagebox.showerror("Error", "Failed to delete template")

if __name__ == "__main__":
    root = tk.Tk()
    app = ActuatorTemplateApp(root)
    root.mainloop()
