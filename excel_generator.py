import pandas as pd
import pyperclip
import win32com.client
import os
from tkinter import messagebox
import re

class ExcelGenerator:
    def __init__(self):
        self.column_headers = [
            "Actuator", "Name", "Index", "DataType", "Prefix", "Output", "Out.Descr.", 
            "Input", "Inp.Descr.", "Alm 0", "Alm 1", "Alm 0 Descr. Language1", 
            "Alm 0 Descr. Language2", "Alm 0 Descr. Language3", "Alm 1 Descr.Language1", 
            "Alm 1 Descr.Language2", "Alm 1 Descr.Language3", "Alm0 Procedure", 
            "Alm1 Procedure", "Alm0 BAD", "Alm1 BAD", "Alm0 Cause", "Alm1 Cause", 
            "Alm0 Action", "Alm1 Action"
        ]
    
    def generate_excel_rows(self, actuators_data):
        """Generate Excel rows from actuators data"""
        rows = []
        
        for actuator_data in actuators_data:
            actuator_number = actuator_data['actuator_number']
            actuator_name = actuator_data['actuator_name']
            
            for actuator in actuator_data['actuators']:
                # Replace placeholders with actual values
                row = self._process_actuator_row(actuator, actuator_number, actuator_name)
                rows.append(row)
        
        return rows
    
    def _process_actuator_row(self, actuator, actuator_number, actuator_name):
        """Process a single actuator row, replacing placeholders"""
        row = [
            f"_{actuator_number}",  # Actuator column with underscore prefix
            self._replace_placeholders(actuator.get('name', ''), actuator_name),
            actuator.get('index', ''),
            actuator.get('datatype', ''),
            actuator.get('prefix', ''),
            actuator.get('output', ''),
            actuator.get('out_descr', ''),
            self._replace_placeholders(actuator.get('input', ''), actuator_name),
            self._replace_placeholders(actuator.get('inp_descr', ''), actuator_name),
            actuator.get('alm0', ''),
            actuator.get('alm1', ''),
            self._replace_placeholders(actuator.get('alm0_descr_lang1', ''), actuator_name),
            self._replace_placeholders(actuator.get('alm0_descr_lang2', ''), actuator_name),
            self._replace_placeholders(actuator.get('alm0_descr_lang3', ''), actuator_name),
            self._replace_placeholders(actuator.get('alm1_descr_lang1', ''), actuator_name),
            self._replace_placeholders(actuator.get('alm1_descr_lang2', ''), actuator_name),
            self._replace_placeholders(actuator.get('alm1_descr_lang3', ''), actuator_name),
            actuator.get('alm0_procedure', ''),
            actuator.get('alm1_procedure', ''),
            actuator.get('alm0_bad', ''),
            actuator.get('alm1_bad', ''),
            actuator.get('alm0_cause', ''),
            actuator.get('alm1_cause', ''),
            actuator.get('alm0_action', ''),
            actuator.get('alm1_action', '')
        ]
        return row
    
    def _replace_placeholders(self, text, actuator_name):
        """Replace placeholders in text with actual values"""
        if not text:
            return text
        
        # Replace {ActuatorName} placeholder
        text = text.replace('{ActuatorName}', actuator_name)
        
        return text
    
    def copy_to_clipboard(self, actuators_data):
        """Copy generated rows to clipboard in tab-separated format"""
        try:
            rows = self.generate_excel_rows(actuators_data)
            
            # Convert to tab-separated format
            clipboard_text = ""
            for row in rows:
                # Convert each cell to string and join with tabs
                row_text = "\t".join(str(cell) for cell in row)
                clipboard_text += row_text + "\n"
            
            # Copy to clipboard
            pyperclip.copy(clipboard_text)
            
            return True, f"Copied {len(rows)} rows to clipboard. You can now paste them into Excel."
            
        except Exception as e:
            return False, f"Error copying to clipboard: {str(e)}"
    
    def insert_into_excel(self, actuators_data):
        """Insert rows directly into open Excel file"""
        try:
            # Try to connect to Excel application
            xl_app = win32com.client.GetActiveObject("Excel.Application")
            
            if not xl_app:
                return False, "No Excel application found. Please open Excel first."
            
            # Get active workbook and worksheet
            workbook = xl_app.ActiveWorkbook
            if not workbook:
                return False, "No active workbook found. Please open an Excel file."
            
            worksheet = xl_app.ActiveSheet
            if not worksheet:
                return False, "No active worksheet found."
            
            # Find "Actuator" in the first column
            actuator_row = self._find_actuator_row(worksheet)
            if actuator_row is None:
                return False, "Could not find 'Actuator' in the first column. Please make sure your Excel file has the correct format."
            
            # Generate rows to insert
            rows = self.generate_excel_rows(actuators_data)
            
            # Insert rows below the Actuator row
            insert_row = actuator_row + 1
            
            for i, row in enumerate(rows):
                current_row = insert_row + i
                
                # Insert row data
                for j, cell_value in enumerate(row):
                    worksheet.Cells(current_row, j + 1).Value = cell_value
            
            return True, f"Successfully inserted {len(rows)} rows into Excel at row {insert_row}."
            
        except Exception as e:
            return False, f"Error inserting into Excel: {str(e)}"
    
    def _find_actuator_row(self, worksheet):
        """Find the row containing 'Actuator' in the first column"""
        try:
            # Search in first column (up to row 100 to be safe)
            for row in range(1, 101):
                cell_value = str(worksheet.Cells(row, 1).Value).strip()
                if cell_value.lower() == "actuator":
                    return row
            return None
        except Exception:
            return None
    
    def detect_excel_files(self):
        """Detect open Excel files and their sheets"""
        try:
            xl_app = win32com.client.GetActiveObject("Excel.Application")
            
            if not xl_app:
                return False, "No Excel application found."
            
            workbooks_info = []
            
            for i in range(1, xl_app.Workbooks.Count + 1):
                workbook = xl_app.Workbooks(i)
                workbook_info = {
                    'name': workbook.Name,
                    'path': workbook.FullName if workbook.Saved else "Unsaved",
                    'sheets': []
                }
                
                # Get sheet names
                for j in range(1, workbook.Worksheets.Count + 1):
                    sheet = workbook.Worksheets(j)
                    workbook_info['sheets'].append(sheet.Name)
                
                workbooks_info.append(workbook_info)
            
            return True, workbooks_info
            
        except Exception as e:
            return False, f"Error detecting Excel files: {str(e)}"
    
    def generate_excel_file(self, actuators_data, file_path):
        """Generate a new Excel file with the actuator data"""
        try:
            # Create DataFrame with headers
            rows = self.generate_excel_rows(actuators_data)
            
            # Create DataFrame
            df = pd.DataFrame(rows, columns=self.column_headers)
            
            # Save to Excel
            with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Actuators', index=False)
            
            return True
            
        except Exception as e:
            print(f"Error generating Excel file: {e}")
            return False
    
    def validate_excel_format(self, file_path):
        """Validate that the Excel file has the correct format"""
        try:
            # Read Excel file
            df = pd.read_excel(file_path, sheet_name=0)
            
            # Check if first column contains "Actuator"
            first_column = df.iloc[:, 0].astype(str).str.strip().str.lower()
            
            if "actuator" in first_column.values:
                return True, "Excel file format is valid."
            else:
                return False, "Excel file does not contain 'Actuator' in the first column."
                
        except Exception as e:
            return False, f"Error validating Excel file: {str(e)}"
    
    def get_excel_template(self):
        """Generate an Excel template with proper headers"""
        try:
            # Create template with headers
            template_data = [self.column_headers]
            
            # Add "Actuator End" row as marker
            end_row = ["Actuator End"] + [""] * (len(self.column_headers) - 1)
            template_data.append(end_row)
            
            df = pd.DataFrame(template_data[1:], columns=template_data[0])
            
            return df
            
        except Exception as e:
            print(f"Error creating Excel template: {e}")
            return None
    
    def export_template_excel(self, file_path):
        """Export Excel template to file"""
        try:
            df = self.get_excel_template()
            if df is not None:
                with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                    df.to_excel(writer, sheet_name='Template', index=False)
                return True
            return False
        except Exception as e:
            print(f"Error exporting Excel template: {e}")
            return False
