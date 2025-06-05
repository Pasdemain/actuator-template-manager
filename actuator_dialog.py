import tkinter as tk
from tkinter import ttk, messagebox
import copy

class ActuatorDialog:
    def __init__(self, parent, template_name, template_manager):
        self.parent = parent
        self.template_name = template_name
        self.template_manager = template_manager
        self.result = None
        
        # Get template data
        self.template_data = template_manager.get_template(template_name)
        if not self.template_data:
            messagebox.showerror("Error", f"Template '{template_name}' not found!")
            return
        
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(f"Use Template: {template_name}")
        self.dialog.geometry("600x500")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (600 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (500 // 2)
        self.dialog.geometry(f"600x500+{x}+{y}")
        
        # Store actuator inputs
        self.actuator_inputs = []
        
        self.create_widgets()
        
        # Wait for dialog to close
        self.dialog.wait_window()
    
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.dialog, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Template info
        info_frame = ttk.LabelFrame(main_frame, text="Template Information", padding="10")
        info_frame.pack(fill=tk.X, pady=(0, 15))
        
        template_info = f"Template: {self.template_name}\n"
        template_info += f"Description: {self.template_data.get('description', 'No description')}\n"
        template_info += f"Components per actuator: {len(self.template_data.get('actuators', []))}"
        
        ttk.Label(info_frame, text=template_info, justify=tk.LEFT).pack(anchor=tk.W)
        
        # Actuators input section
        input_frame = ttk.LabelFrame(main_frame, text="Actuator Configuration", padding="10")
        input_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # Instructions
        instructions = """Instructions:
• Each actuator will generate multiple rows (components) based on the template
• Actuator Number: Just the number (e.g., 30, 138) - the underscore will be added automatically
• Actuator Name: The name to replace {ActuatorName} placeholders (e.g., AxisX, AxisZ)
• You can add multiple actuators using the same template"""
        
        ttk.Label(input_frame, text=instructions, justify=tk.LEFT, 
                 foreground="blue").pack(anchor=tk.W, pady=(0, 10))
        
        # Scrollable frame for actuator inputs
        canvas = tk.Canvas(input_frame, height=200)
        scrollbar = ttk.Scrollbar(input_frame, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind mousewheel to canvas
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", on_mousewheel)
        
        # Add first actuator input
        self.add_actuator_input()
        
        # Buttons for managing actuators
        actuator_btn_frame = ttk.Frame(input_frame)
        actuator_btn_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(actuator_btn_frame, text="+ Add Another Actuator", 
                  command=self.add_actuator_input).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(actuator_btn_frame, text="- Remove Last", 
                  command=self.remove_last_actuator).pack(side=tk.LEFT)
        
        # Preview section
        preview_frame = ttk.LabelFrame(main_frame, text="Preview", padding="10")
        preview_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.preview_text = tk.Text(preview_frame, height=6, width=70, 
                                   wrap=tk.WORD, state=tk.DISABLED)
        preview_scrollbar = ttk.Scrollbar(preview_frame, orient="vertical", 
                                        command=self.preview_text.yview)
        self.preview_text.configure(yscrollcommand=preview_scrollbar.set)
        
        self.preview_text.pack(side="left", fill="both", expand=True)
        preview_scrollbar.pack(side="right", fill="y")
        
        ttk.Button(preview_frame, text="Update Preview", 
                  command=self.update_preview).pack(pady=(10, 0))
        
        # Dialog buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        ttk.Button(button_frame, text="Generate", 
                  command=self.generate_actuators).pack(side=tk.RIGHT, padx=(10, 0))
        ttk.Button(button_frame, text="Cancel", 
                  command=self.cancel).pack(side=tk.RIGHT)
        
    def add_actuator_input(self):
        """Add input fields for a new actuator"""
        row = len(self.actuator_inputs)
        
        # Create frame for this actuator
        actuator_frame = ttk.Frame(self.scrollable_frame)
        actuator_frame.grid(row=row, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Configure grid
        actuator_frame.columnconfigure(1, weight=1)
        actuator_frame.columnconfigure(3, weight=1)
        
        # Actuator number
        ttk.Label(actuator_frame, text=f"Actuator {row + 1} Number:").grid(
            row=0, column=0, sticky=tk.W, padx=(0, 10))
        
        number_var = tk.StringVar()
        number_entry = ttk.Entry(actuator_frame, textvariable=number_var, width=15)
        number_entry.grid(row=0, column=1, sticky=tk.W, padx=(0, 20))
        
        # Actuator name
        ttk.Label(actuator_frame, text="Name:").grid(
            row=0, column=2, sticky=tk.W, padx=(0, 10))
        
        name_var = tk.StringVar()
        name_entry = ttk.Entry(actuator_frame, textvariable=name_var, width=20)
        name_entry.grid(row=0, column=3, sticky=tk.W)
        
        # Additional parameters section (for future expansion)
        params_frame = ttk.Frame(actuator_frame)
        params_frame.grid(row=1, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=(5, 0))
        
        # Store the input data
        input_data = {
            'frame': actuator_frame,
            'number_var': number_var,
            'name_var': name_var,
            'number_entry': number_entry,
            'name_entry': name_entry,
            'params_frame': params_frame,
            'additional_params': {}
        }
        
        self.actuator_inputs.append(input_data)
        
        # Focus on the number entry for the first actuator
        if row == 0:
            number_entry.focus()
        
        # Update scrollable region
        self.scrollable_frame.update_idletasks()
    
    def remove_last_actuator(self):
        """Remove the last actuator input"""
        if len(self.actuator_inputs) > 1:
            last_input = self.actuator_inputs.pop()
            last_input['frame'].destroy()
            
            # Update scrollable region
            self.scrollable_frame.update_idletasks()
    
    def update_preview(self):
        """Update the preview text with generated data"""
        try:
            generated_data = self.get_generated_data()
            if not generated_data:
                return
            
            # Create preview text
            preview_text = "Generated Rows Preview:\n\n"
            
            for actuator_data in generated_data:
                actuator_number = actuator_data['actuator_number']
                actuator_name = actuator_data['actuator_name']
                
                preview_text += f"=== Actuator _{actuator_number} ({actuator_name}) ===\n"
                
                for i, actuator in enumerate(actuator_data['actuators']):
                    name = actuator.get('name', '').replace('{ActuatorName}', actuator_name)
                    datatype = actuator.get('datatype', '')
                    index = actuator.get('index', '')
                    
                    preview_text += f"  {i+1}. _{actuator_number} {name} {index} {datatype}\n"
                
                preview_text += "\n"
            
            # Update preview text widget
            self.preview_text.config(state=tk.NORMAL)
            self.preview_text.delete(1.0, tk.END)
            self.preview_text.insert(1.0, preview_text)
            self.preview_text.config(state=tk.DISABLED)
            
        except Exception as e:
            messagebox.showerror("Preview Error", f"Error generating preview: {str(e)}")
    
    def get_generated_data(self):
        """Get the generated actuator data based on inputs"""
        generated_data = []
        
        for i, input_data in enumerate(self.actuator_inputs):
            number = input_data['number_var'].get().strip()
            name = input_data['name_var'].get().strip()
            
            if not number or not name:
                continue  # Skip incomplete entries
            
            # Validate number
            if not number.isdigit():
                raise ValueError(f"Actuator {i+1} number must be numeric")
            
            # Create actuator data
            actuator_data = {
                'actuator_number': number,
                'actuator_name': name,
                'actuators': copy.deepcopy(self.template_data['actuators'])
            }
            
            generated_data.append(actuator_data)
        
        return generated_data
    
    def validate_inputs(self):
        """Validate all inputs"""
        errors = []
        
        for i, input_data in enumerate(self.actuator_inputs):
            number = input_data['number_var'].get().strip()
            name = input_data['name_var'].get().strip()
            
            if not number and not name:
                continue  # Skip empty rows
            
            if not number:
                errors.append(f"Actuator {i+1}: Number is required")
            elif not number.isdigit():
                errors.append(f"Actuator {i+1}: Number must be numeric")
            
            if not name:
                errors.append(f"Actuator {i+1}: Name is required")
            elif not name.replace('_', '').replace('-', '').isalnum():
                errors.append(f"Actuator {i+1}: Name should contain only alphanumeric characters, underscores, and hyphens")
        
        # Check for duplicate numbers
        numbers = []
        for input_data in self.actuator_inputs:
            number = input_data['number_var'].get().strip()
            if number:
                if number in numbers:
                    errors.append(f"Duplicate actuator number: {number}")
                numbers.append(number)
        
        return errors
    
    def generate_actuators(self):
        """Generate actuators and close dialog"""
        # Validate inputs
        errors = self.validate_inputs()
        if errors:
            error_message = "Please fix the following errors:\n\n" + "\n".join(errors)
            messagebox.showerror("Validation Error", error_message)
            return
        
        try:
            generated_data = self.get_generated_data()
            
            if not generated_data:
                messagebox.showwarning("Warning", "Please enter at least one actuator.")
                return
            
            self.result = generated_data
            self.dialog.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error generating actuators: {str(e)}")
    
    def cancel(self):
        """Cancel and close dialog"""
        self.result = None
        self.dialog.destroy()
