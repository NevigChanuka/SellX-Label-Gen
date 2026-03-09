import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from database import Database
from printer import generate_html_label

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class LabelApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.title("Sell-X Shipping Label Generator")
        self.geometry("550x750")
        self.configure(padx=20, pady=15)

        self.suggestion_list = []
        self.selected_index = -1
        self.dropdown = None
        self.setup_ui()

    def setup_ui(self):
        # --- FIXED HEADER ---
        self.header = ctk.CTkLabel(self, text="Sell-X", font=("Segoe UI", 28, "bold"), text_color="#e60000")
        self.header.pack(pady=(5, 0))
        self.sub_header = ctk.CTkLabel(self, text="Customer Management & Shipping", font=("Segoe UI", 12))
        self.sub_header.pack(pady=(0, 15))

        # --- SCROLLABLE FORM AREA ---
        # This frame will allow scrolling if the screen resolution is low
        self.scroll_canvas = ctk.CTkScrollableFrame(self, corner_radius=15, fg_color="transparent")
        self.scroll_canvas.pack(fill="both", expand=True, padx=5, pady=5)

        self.entries = {}
        fields = [
            ("Customer Name", "Start typing..."), 
            ("Address", "Street..."), 
            ("City/Town", "City..."), 
            ("Phone 1", "07..."), 
            ("Phone 2", "07...")
        ]

        for label, placeholder in fields:
            lbl = ctk.CTkLabel(self.scroll_canvas, text=label, font=("Segoe UI", 12, "bold"))
            lbl.pack(anchor="w", padx=25, pady=(12, 0))
            
            entry = ctk.CTkEntry(self.scroll_canvas, placeholder_text=placeholder, height=42, corner_radius=8)
            entry.pack(fill="x", padx=25, pady=(2, 5))
            self.entries[label] = entry

        # Quantity Selector inside the scrollable area
        ctk.CTkLabel(self.scroll_canvas, text="Labels per Page (Max 3)", font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=25, pady=(15, 0))
        self.qty_var = ctk.StringVar(value="3")
        self.qty_selector = ctk.CTkSegmentedButton(self.scroll_canvas, values=["1", "2", "3"], variable=self.qty_var, height=38)
        self.qty_selector.pack(fill="x", padx=25, pady=(5, 25))

        # Bindings for the Name field
        name_ent = self.entries["Customer Name"]
        name_ent.bind("<KeyRelease>", self.on_key_release)
        name_ent.bind("<Down>", self.move_selection)
        name_ent.bind("<Up>", self.move_selection)
        name_ent.bind("<Return>", self.confirm_selection)

        # --- FIXED FOOTER (Always Visible) ---
        footer_frame = ctk.CTkFrame(self, fg_color="transparent")
        footer_frame.pack(fill="x", pady=(10, 0))

        self.print_btn = ctk.CTkButton(footer_frame, text="GENERATE & PRINT LABEL", command=self.handle_print,
                                       height=55, font=("Segoe UI", 14, "bold"), fg_color="#e60000", 
                                       hover_color="#b30000", corner_radius=10)
        self.print_btn.pack(fill="x", pady=(5, 10))

        btn_row = ctk.CTkFrame(footer_frame, fg_color="transparent")
        btn_row.pack(fill="x")
        
        ctk.CTkButton(btn_row, text="Clear Form", command=self.clear_fields, fg_color="transparent", 
                      border_width=1, text_color="gray", width=140).pack(side="left", expand=True, padx=(0, 5))
        
        ctk.CTkButton(btn_row, text="Delete Record", command=self.handle_delete, fg_color="transparent", 
                      border_width=1, text_color="#cc0000", border_color="#cc0000", width=140).pack(side="right", expand=True, padx=(5, 0))

    # --- LOGIC ---
    def on_key_release(self, event):
        if event.keysym in ["Up", "Down", "Return"]: return
        val = self.entries["Customer Name"].get().strip()
        if len(val) >= 2:
            self.show_dropdown(self.db.get_suggestions(val))
        else:
            self.hide_dropdown()

    def show_dropdown(self, results):
        self.hide_dropdown()
        if not results: return
        self.suggestion_list = results
        self.selected_index = -1
        
        # We place the dropdown inside the scroll_canvas so it moves with the entry
        self.dropdown = tk.Listbox(self.scroll_canvas, font=("Segoe UI", 11), bg="white", borderwidth=1, relief="flat")
        for item in results: self.dropdown.insert(tk.END, f"  {item}")
        
        # Absolute positioning relative to the scroll_canvas
        self.dropdown.place(x=25, y=98, width=420, height=120)
        self.dropdown.bind("<<ListboxSelect>>", lambda e: self.confirm_selection())

    def hide_dropdown(self):
        if self.dropdown:
            self.dropdown.destroy()
            self.dropdown = None

    def move_selection(self, event):
        if not self.dropdown: return
        if event.keysym == "Down":
            self.selected_index = min(self.selected_index + 1, len(self.suggestion_list) - 1)
        else:
            self.selected_index = max(self.selected_index - 1, 0)
        self.dropdown.selection_clear(0, tk.END)
        self.dropdown.selection_set(self.selected_index)

    def confirm_selection(self, event=None):
        if self.dropdown:
            try:
                idx = self.selected_index if self.selected_index != -1 else self.dropdown.curselection()[0]
                name = self.suggestion_list[idx]
                data = self.db.get_customer(name)
                for i, key in enumerate(self.entries.keys()):
                    self.entries[key].delete(0, 'end')
                    self.entries[key].insert(0, data[i])
            except: pass
            self.hide_dropdown()
        elif event:
            self.handle_print()

    def handle_print(self):
        data = [self.entries[k].get().strip() for k in self.entries]
        if not data[0]:
            messagebox.showwarning("Empty Name", "Please enter a customer name.")
            return
        
        try:
            qty = int(self.qty_var.get())
        except:
            qty = 1
            
        self.db.save_customer(data)
        generate_html_label(data, qty)

    def handle_delete(self):
        name = self.entries["Customer Name"].get().strip()
        if name and self.db.get_customer(name):
            if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {name}?"):
                self.db.delete_customer(name)
                self.clear_fields()
        else:
            messagebox.showwarning("Error", "No customer selected to delete.")

    def clear_fields(self):
        for entry in self.entries.values():
            entry.delete(0, 'end')
        self.hide_dropdown()

if __name__ == "__main__":
    app = LabelApp()
    app.mainloop()