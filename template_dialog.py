import tkinter as tk
from tkinter import ttk, messagebox
import copy

class TemplateDialog:
    def __init__(self, parent, title, template_data=None):
        self.parent = parent
        self.result = None
        
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("1200x800")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (1200 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (800 // 2)
        self.dialog.geometry(f"1200x800+{x}+{y}")
        
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
        # Main frame with scrollbar
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
        
        # Actuators section
        actuators_frame = ttk.LabelFrame(main_frame, text="Actuators", padding="10")
        actuators_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Actuators list and buttons
        list_frame = ttk.Frame(actuators_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # Actuators listbox
        list_container = ttk.Frame(list_frame)
        list_container.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        ttk.Label(list_container, text="Actuators in Template:").pack(anchor=tk.W)
        
        self.actuators_listbox = tk.Listbox(list_container, width=30, height=15)
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
        
        # Dialog buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        ttk.Button(button_frame, text="Save Template", 
                  command=self.save_template).pack(side=tk.RIGHT, padx=(10, 0))
        ttk.Button(button_frame, text="Cancel", 
                  command=self.cancel).pack(side=tk.RIGHT)
        
        # Initialize with empty actuator details
        self.clear_actuator_fields()
        
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
