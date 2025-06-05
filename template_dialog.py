import tkinter as tk
from tkinter import ttk, messagebox
import copy
import re

class TemplateDialog:
    def __init__(self, parent, title, template_data=None):
        self.parent = parent
        self.result = None
        
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("1400x900")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (700)
        y = (self.dialog.winfo_screenheight() // 2) - (450)
        self.dialog.geometry(f"1400x900+{x}+{y}")
        
        # Initialize data
        self.template_data = template_data if template_data else {
            "name": "",
            "description": "",
            "actuators": []
        }
        
        # All available fields for actuators
        self.actuator_fields = [
            ("name", "Name"),
            ("index", "Index"),
            ("datatype", "DataType"),
            ("prefix", "Prefix"),
            ("output", "Output"),
            ("out_descr", "Out.Descr."),
            ("input", "Input"),
            ("inp_descr", "Inp.Descr."),
            ("alm0", "Alm 0"),
            ("alm1", "Alm 1"),
            ("alm0_descr_lang1", "Alm 0 Descr. Language1"),
            ("alm0_descr_lang2", "Alm 0 Descr. Language2"),
            ("alm0_descr_lang3", "Alm 0 Descr. Language3"),
            ("alm1_descr_lang1", "Alm 1 Descr.Language1"),
            ("alm1_descr_lang2", "Alm 1 Descr.Language2"),
            ("alm1_descr_lang3", "Alm 1 Descr.Language3"),
            ("alm0_procedure", "Alm0 Procedure"),
            ("alm1_procedure", "Alm1 Procedure"),
            ("alm0_bad", "Alm0 BAD"),
            ("alm1_bad", "Alm1 BAD"),
            ("alm0_cause", "Alm0 Cause"),
            ("alm1_cause", "Alm1 Cause"),
            ("alm0_action", "Alm0 Action"),
            ("alm1_action", "Alm1 Action")
        ]
        
        self.create_widgets()
        self.load_template_data()
        
        # Wait for dialog to close
        self.dialog.wait_window()
    
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.dialog)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Template info section
        info_frame = ttk.LabelFrame(main_frame, text="Template Information", padding="10")
        info_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Template name
        ttk.Label(info_frame, text="Template Name:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.name_var = tk.StringVar(value=self.template_data.get("name", ""))
        name_entry = ttk.Entry(info_frame, textvariable=self.name_var, width=30)
        name_entry.grid(row=0, column=1, sticky=tk.W)
        
        # Template description
        ttk.Label(info_frame, text="Description:").grid(row=1, column=0, sticky=tk.W, padx=(0, 10), pady=(10, 0))
        self.desc_var = tk.StringVar(value=self.template_data.get("description", ""))
        desc_entry = ttk.Entry(info_frame, textvariable=self.desc_var, width=50)
        desc_entry.grid(row=1, column=1, sticky=tk.W, pady=(10, 0))
        
        # Actuators section with notebook tabs
        actuators_frame = ttk.LabelFrame(main_frame, text="Actuators", padding="10")
        actuators_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Create notebook for different views
        self.notebook = ttk.Notebook(actuators_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # List view tab
        list_tab = ttk.Frame(self.notebook)
        self.notebook.add(list_tab, text="📋 List View")
        
        # Paste import tab
        paste_tab = ttk.Frame(self.notebook)
        self.notebook.add(paste_tab, text="📥 Import from Paste")
        
        # Setup views
        self.setup_list_view(list_tab)
        self.setup_paste_view(paste_tab)
        
        # Dialog buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        ttk.Button(button_frame, text="Save Template", 
                  command=self.save_template).pack(side=tk.RIGHT, padx=(10, 0))
        ttk.Button(button_frame, text="Cancel", 
                  command=self.cancel).pack(side=tk.RIGHT)
        
    def setup_list_view(self, parent):
        """Setup the list view tab"""
        list_frame = ttk.Frame(parent)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Actuators listbox
        list_container = ttk.Frame(list_frame)
        list_container.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        ttk.Label(list_container, text="Actuators in Template:").pack(anchor=tk.W)
        
        self.actuators_listbox = tk.Listbox(list_container, width=35, height=15)
        self.actuators_listbox.pack(fill=tk.Y, expand=True)
        self.actuators_listbox.bind('<<ListboxSelect>>', self.on_actuator_select)
        
        # Actuator buttons
        buttons_frame = ttk.Frame(list_container)
        buttons_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(buttons_frame, text="Add New Actuator", 
                  command=self.add_actuator).pack(fill=tk.X, pady=(0, 5))
        ttk.Button(buttons_frame, text="Copy Selected", 
                  command=self.copy_actuator).pack(fill=tk.X, pady=(0, 5))
        ttk.Button(buttons_frame, text="Delete Selected", 
                  command=self.delete_actuator).pack(fill=tk.X, pady=(0, 5))
        ttk.Button(buttons_frame, text="Move Up", 
                  command=self.move_up).pack(fill=tk.X, pady=(0, 5))
        ttk.Button(buttons_frame, text="Move Down", 
                  command=self.move_down).pack(fill=tk.X)
        
        # Actuator details frame
        details_frame = ttk.LabelFrame(list_frame, text="Actuator Details", padding="10")
        details_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Create scrollable frame for actuator fields
        canvas = tk.Canvas(details_frame, height=400)
        scrollbar_details = ttk.Scrollbar(details_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar_details.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar_details.pack(side="right", fill="y")
        
        # Create entry fields for all actuator properties
        self.field_vars = {}
        row = 0
        
        for field_key, field_label in self.actuator_fields:
            ttk.Label(scrollable_frame, text=f"{field_label}:").grid(
                row=row, column=0, sticky=tk.W, padx=(0, 10), pady=(2, 2)
            )
            
            if field_key in ["alm0_cause", "alm1_cause", "alm0_action", "alm1_action"]:
                # Multi-line text for cause and action fields
                var = tk.StringVar()
                text_widget = tk.Text(scrollable_frame, height=3, width=40, wrap=tk.WORD)
                text_widget.grid(row=row, column=1, sticky=tk.W, pady=(2, 2))
                
                # Store reference to text widget for later access
                self.field_vars[field_key] = {
                    'var': var,
                    'widget': text_widget,
                    'type': 'text'
                }
            else:
                # Regular entry field
                var = tk.StringVar()
                entry = ttk.Entry(scrollable_frame, textvariable=var, width=40)
                entry.grid(row=row, column=1, sticky=tk.W, pady=(2, 2))
                
                self.field_vars[field_key] = {
                    'var': var,
                    'widget': entry,
                    'type': 'entry'
                }
            
            row += 1
        
        # Add save button for actuator changes
        save_actuator_btn = ttk.Button(scrollable_frame, text="Save Actuator Changes", 
                                      command=self.save_actuator_changes)
        save_actuator_btn.grid(row=row, column=0, columnspan=2, pady=(20, 0))
        
        # Initialize with empty actuator details
        self.clear_actuator_fields()
    
    def setup_paste_view(self, parent):
        """Setup the paste import view"""
        paste_frame = ttk.Frame(parent)
        paste_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Instructions
        instructions = """Instructions for Import from Paste:
1. Copy your actuator data from Excel or any text source
2. Paste it in the text area below
3. The data should be tab-separated (like copying from Excel)
4. Each line represents one actuator component
5. Click 'Parse and Import' to convert to template format
6. You can then edit the imported data and add placeholders like {ActuatorName}
        
Expected format: *ActuatorNum Name Index DataType Prefix Output Out.Descr Input Inp.Descr Alm0 Alm1 ..."""
        
        inst_label = ttk.Label(paste_frame, text=instructions, justify=tk.LEFT, foreground="blue")
        inst_label.pack(anchor=tk.W, pady=(0, 10))
        
        # Text area for pasting
        ttk.Label(paste_frame, text="Paste your actuator data here:").pack(anchor=tk.W)
        
        # Create frame for text area and scrollbars
        text_container = ttk.Frame(paste_frame)
        text_container.pack(fill=tk.BOTH, expand=True, pady=(5, 10))
        
        self.paste_text = tk.Text(text_container, height=15, width=100, wrap=tk.NONE)
        paste_scroll_y = ttk.Scrollbar(text_container, orient="vertical", command=self.paste_text.yview)
        paste_scroll_x = ttk.Scrollbar(text_container, orient="horizontal", command=self.paste_text.xview)
        self.paste_text.configure(yscrollcommand=paste_scroll_y.set, xscrollcommand=paste_scroll_x.set)
        
        # Pack text area and scrollbars (using pack consistently)
        self.paste_text.pack(side="left", fill="both", expand=True)
        paste_scroll_y.pack(side="right", fill="y")
        paste_scroll_x.pack(side="bottom", fill="x")
        
        # Parse button
        parse_button = ttk.Button(paste_frame, text="📥 Parse and Import", 
                                command=self.parse_and_import)
        parse_button.pack(pady=(0, 10))
        
        # Sample data button
        sample_button = ttk.Button(paste_frame, text="📝 Show Sample Format", 
                                 command=self.show_sample_format)
        sample_button.pack()
    
    def show_sample_format(self):
        """Show sample format in the paste text area"""
        sample_data = """*138	AxisRy1	0	Act_Stepper_OM			Alm1	Alms.L2.	Alms.L2.	AxisRy Drive Error	AxisRy Drive Error	AxisRy Drive Error	AxisRy Position Error	AxisRy Position Error	AxisRy Position Error	P200	P201	x	x	*Linmot safety contactor not activated *Linmot drive faulted or not ready *Can happen after aborted fault	*Homing timeout or error *Movement timeout or error *Overtorque/Position error during movement *Motor overheat	*Acknowledge the fault and execute a reset sequence *Check contactor wiring *If the problem persists contact maintenance	*Inspect the station, check for blockage *Acknowledge the fault and execute a reset sequence *If the problem persists contact maintenance
*138	AxisRy1_MotionCfg	1	Typ_AxLinearMotionOM																				
*138	AxisRy1_SafeJogCfg	2	Typ_AxSafeJogMotion																				
*138	AxisRy1_NotHomed	3	Alias			Alm2		Alms.L2.			AxisRy Not Homed	AxisRy Not Homed	AxisRy Not Homed		P203		x		*Axis homing not reached		*Reset the fault and execute a homing function    In case the problem persists contact maintenance *Check sensor functionality
*138	AxisRy1_SysHMi	4	Typ_AxSiHMi																				
*138	AxisRy1_Interlock	5	Alias			Alm3		Alms.L1.			AxisRy Interlock Error	AxisRy Interlock Error	AxisRy Interlock Error		P202		x		*Position not as per expected    Can happen if axis moved manually    Can happen after an aborted fault		*Reset the fault and execute a reset sequence    In case the problem persists contact maintenance"""
        
        self.paste_text.delete(1.0, tk.END)
        self.paste_text.insert(1.0, sample_data)
    
    def parse_and_import(self):
        """Parse pasted data and import as actuators"""
        try:
            pasted_data = self.paste_text.get(1.0, tk.END).strip()
            if not pasted_data:
                messagebox.showwarning("Warning", "Please paste some data first.")
                return
            
            # Split into lines
            raw_lines = pasted_data.split('\n')
            
            # Reconstruct lines: only lines starting with _XXX are new rows
            # Everything else gets appended to the previous line
            reconstructed_lines = []
            current_line = ""
            
            for line in raw_lines:
                line = line.strip()
                if not line:  # Skip empty lines
                    continue
                
                # Check if line starts with _XXX pattern (underscore + digits)
                if re.match(r'^_\d+', line):
                    # This is a new actuator line
                    if current_line:  # Save previous line if exists
                        reconstructed_lines.append(current_line)
                    current_line = line  # Start new line
                else:
                    # This is a continuation of the previous line
                    if current_line:
                        current_line += " " + line  # Add to current line with space
                    else:
                        current_line = line  # First line doesn't start with _XXX
            
            # Add the last line
            if current_line:
                reconstructed_lines.append(current_line)
            
            if not reconstructed_lines:
                messagebox.showwarning("Warning", "No valid actuator data found. Please check the format.")
                return
            
            imported_actuators = []
            
            for line in reconstructed_lines:
                if not line.strip():
                    continue
                
                # Split by multiple spaces or tabs
                # First normalize multiple spaces to single tabs
                line = re.sub(r'\s{2,}', '\t', line)
                
                # Split by tabs
                if '\t' in line:
                    parts = line.split('\t')
                else:
                    # Fallback: split by single space
                    parts = line.split(' ')
                
                # Clean empty parts and strip whitespace
                parts = [p.strip() for p in parts if p.strip()]
                
                if not parts:
                    continue
                
                # Remove _ from actuator number if present (first part should be _XXX)
                if parts[0].startswith('_'):
                    parts[0] = parts[0][1:]  # Remove the underscore
                
                # Create actuator data mapping to our fields
                actuator = {}
                parts = parts[1:]  # Skip the first column (actuator number)
                for i, (field_key, _) in enumerate(self.actuator_fields):
                        if i < len(parts):
                                value = parts[i].strip()
                                
                                # Apply smart placeholder replacement
                                if field_key == "name" and i == 0:  # Name is now first field
                                        # Replace specific axis names with placeholder
                                        if re.search(r'Axis[A-Z][a-z0-9]*', value):
                                                # Keep suffixes like _MotionCfg, _NotHomed etc.
                                                if '_' in value:
                                                        base_name = value.split('_')[0]
                                                        suffix = value[len(base_name):]
                                                        value = f"{{ActuatorName}}{suffix}"
                                                else:
                                                        value = "{ActuatorName}"
                                
                                # Handle alarm descriptions - replace axis names with placeholder
                                elif field_key in ["alm0_descr_lang1", "alm0_descr_lang2", "alm0_descr_lang3", 
                                                                    "alm1_descr_lang1", "alm1_descr_lang2", "alm1_descr_lang3"]:
                                        # Replace specific axis names in descriptions
                                        value = re.sub(r'Axis[A-Z][a-z0-9]*', '{ActuatorName}', value)
                                
                                actuator[field_key] = value
                        else:
                                actuator[field_key] = ""
                
                # Only add if we have both actuator number and name
                if actuator.get('name', '').strip() and len(parts) > 1:
                    imported_actuators.append(actuator)
            
            if not imported_actuators:
                messagebox.showwarning("Warning", "No valid actuator data found. Please check the format.\n\nMake sure your data has lines starting with _XXX (like _138, _30, etc.)")
                return
            
            # Add imported actuators to template
            self.template_data["actuators"].extend(imported_actuators)
            
            # Refresh views
            self.refresh_actuators_list()
            
            messagebox.showinfo("Success", f"Imported {len(imported_actuators)} actuator components!\n\nSwitching to List View to review the imported data.")
            
            # Switch to list view to show imported data
            self.notebook.select(0)  # Select list view tab
            
        except Exception as e:
            messagebox.showerror("Import Error", f"Error parsing data: {str(e)}\n\nPlease check that your data format is correct.")
    
    def load_template_data(self):
        """Load existing template data into the dialog"""
        # Load actuators into listbox
        self.refresh_actuators_list()
        
    def refresh_actuators_list(self):
        """Refresh the actuators listbox"""
        self.actuators_listbox.delete(0, tk.END)
        
        for i, actuator in enumerate(self.template_data["actuators"]):
            display_text = f"{i+1}. {actuator.get('name', 'Unnamed')} (Index: {actuator.get('index', 'N/A')})"
            self.actuators_listbox.insert(tk.END, display_text)
    
    def on_actuator_select(self, event):
        """Handle actuator selection"""
        selection = self.actuators_listbox.curselection()
        if selection:
            index = selection[0]
            actuator = self.template_data["actuators"][index]
            self.load_actuator_into_fields(actuator)
    
    def load_actuator_into_fields(self, actuator):
        """Load actuator data into the detail fields"""
        for field_key, field_data in self.field_vars.items():
            value = actuator.get(field_key, "")
            
            if field_data['type'] == 'text':
                # Text widget
                text_widget = field_data['widget']
                text_widget.delete(1.0, tk.END)
                text_widget.insert(1.0, value)
            else:
                # Entry widget
                field_data['var'].set(value)
    
    def clear_actuator_fields(self):
        """Clear all actuator detail fields"""
        for field_key, field_data in self.field_vars.items():
            if field_data['type'] == 'text':
                field_data['widget'].delete(1.0, tk.END)
            else:
                field_data['var'].set("")
    
    def save_actuator_changes(self):
        """Save changes to the currently selected actuator"""
        selection = self.actuators_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an actuator to save changes.")
            return
        
        index = selection[0]
        actuator = self.template_data["actuators"][index]
        
        # Update actuator with field values
        for field_key, field_data in self.field_vars.items():
            if field_data['type'] == 'text':
                value = field_data['widget'].get(1.0, tk.END).strip()
            else:
                value = field_data['var'].get().strip()
            
            actuator[field_key] = value
        
        # Refresh the list display
        self.refresh_actuators_list()
        
        # Re-select the actuator
        self.actuators_listbox.selection_set(index)
        
        messagebox.showinfo("Success", "Actuator changes saved!")
    
    def add_actuator(self):
        """Add a new empty actuator"""
        new_actuator = {}
        for field_key, _ in self.actuator_fields:
            new_actuator[field_key] = ""
        
        self.template_data["actuators"].append(new_actuator)
        self.refresh_actuators_list()
        
        # Select the new actuator
        new_index = len(self.template_data["actuators"]) - 1
        self.actuators_listbox.selection_set(new_index)
        self.load_actuator_into_fields(new_actuator)
    
    def copy_actuator(self):
        """Copy the selected actuator"""
        selection = self.actuators_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an actuator to copy.")
            return
        
        index = selection[0]
        original_actuator = self.template_data["actuators"][index]
        
        # Create a deep copy
        copied_actuator = copy.deepcopy(original_actuator)
        
        # Modify the name to indicate it's a copy
        original_name = copied_actuator.get('name', '')
        if not original_name.endswith('_Copy'):
            copied_actuator['name'] = original_name + '_Copy'
        
        self.template_data["actuators"].append(copied_actuator)
        self.refresh_actuators_list()
        
        # Select the new copy
        new_index = len(self.template_data["actuators"]) - 1
        self.actuators_listbox.selection_set(new_index)
        self.load_actuator_into_fields(copied_actuator)
    
    def delete_actuator(self):
        """Delete the selected actuator"""
        selection = self.actuators_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an actuator to delete.")
            return
        
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this actuator?"):
            index = selection[0]
            del self.template_data["actuators"][index]
            self.refresh_actuators_list()
            self.clear_actuator_fields()
    
    def move_up(self):
        """Move selected actuator up in the list"""
        selection = self.actuators_listbox.curselection()
        if not selection or selection[0] == 0:
            return
        
        index = selection[0]
        # Swap with previous
        self.template_data["actuators"][index], self.template_data["actuators"][index-1] = \
            self.template_data["actuators"][index-1], self.template_data["actuators"][index]
        
        self.refresh_actuators_list()
        self.actuators_listbox.selection_set(index-1)
    
    def move_down(self):
        """Move selected actuator down in the list"""
        selection = self.actuators_listbox.curselection()
        if not selection or selection[0] >= len(self.template_data["actuators"]) - 1:
            return
        
        index = selection[0]
        # Swap with next
        self.template_data["actuators"][index], self.template_data["actuators"][index+1] = \
            self.template_data["actuators"][index+1], self.template_data["actuators"][index]
        
        self.refresh_actuators_list()
        self.actuators_listbox.selection_set(index+1)
    
    def save_template(self):
        """Save the template and close dialog"""
        name = self.name_var.get().strip()
        if not name:
            messagebox.showerror("Error", "Please enter a template name.")
            return
        
        description = self.desc_var.get().strip()
        
        self.result = {
            "name": name,
            "description": description,
            "actuators": self.template_data["actuators"]
        }
        
        self.dialog.destroy()
    
    def cancel(self):
        """Cancel and close dialog"""
        self.result = None
        self.dialog.destroy()
