import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from database import Database
from printer import generate_html_label  # Importing your new module

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class LabelApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.title("Sell-X Shipping Label Generator")
        self.geometry("500x750")
        self.configure(padx=30, pady=20)

        self.suggestion_list = []
        self.selected_index = -1
        self.dropdown = None
        self.setup_ui()

    def setup_ui(self):
        # Header
        ctk.CTkLabel(self, text="Sell-X", font=("Segoe UI", 26, "bold"), text_color="#e60000").pack()
        ctk.CTkLabel(self, text="Customer Management & Shipping", font=("Segoe UI", 12)).pack(pady=(0, 20))

        # Form Card
        self.form_frame = ctk.CTkFrame(self, corner_radius=15)
        self.form_frame.pack(fill="both", expand=True, padx=2, pady=5)

        self.entries = {}
        fields = [("Customer Name", "Start typing..."), ("Address", "Street..."), 
                  ("City/Town", "City..."), ("Phone 1", "07..."), ("Phone 2", "07...")]

        for label, placeholder in fields:
            ctk.CTkLabel(self.form_frame, text=label, font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=25, pady=(12, 0))
            entry = ctk.CTkEntry(self.form_frame, placeholder_text=placeholder, height=40, corner_radius=8)
            entry.pack(fill="x", padx=25, pady=(2, 5))
            self.entries[label] = entry

        # Bindings
        name_ent = self.entries["Customer Name"]
        name_ent.bind("<KeyRelease>", self.on_key_release)
        name_ent.bind("<Down>", self.move_selection)
        name_ent.bind("<Up>", self.move_selection)
        name_ent.bind("<Return>", self.confirm_selection)

        # Buttons
        self.print_btn = ctk.CTkButton(self, text="GENERATE & PRINT LABEL", command=self.handle_print,
                                       height=55, font=("Segoe UI", 14, "bold"), fg_color="#e60000", corner_radius=10)
        self.print_btn.pack(fill="x", pady=(25, 10))

        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="x")
        ctk.CTkButton(btn_frame, text="Clear Form", command=self.clear_fields, fg_color="transparent", border_width=1, text_color="gray", width=150).pack(side="left", expand=True)
        ctk.CTkButton(btn_frame, text="Delete Record", command=self.handle_delete, fg_color="transparent", border_width=1, text_color="#cc0000", border_color="#cc0000", width=150).pack(side="right", expand=True)

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
        self.dropdown = tk.Listbox(self.form_frame, font=("Segoe UI", 11), bg="white", borderwidth=1, relief="flat")
        for item in results: self.dropdown.insert(tk.END, f"  {item}")
        self.dropdown.place(x=25, y=95, width=390, height=120)
        self.dropdown.bind("<<ListboxSelect>>", lambda e: self.confirm_selection())

    def hide_dropdown(self):
        if self.dropdown: self.dropdown.destroy(); self.dropdown = None

    def move_selection(self, event):
        if not self.dropdown: return
        self.selected_index = min(self.selected_index + 1, len(self.suggestion_list) - 1) if event.keysym == "Down" else max(self.selected_index - 1, 0)
        self.dropdown.selection_clear(0, tk.END); self.dropdown.selection_set(self.selected_index)

    def confirm_selection(self, event=None):
        if self.dropdown:
            try:
                name = self.suggestion_list[self.selected_index if self.selected_index != -1 else self.dropdown.curselection()[0]]
                data = self.db.get_customer(name)
                for i, key in enumerate(self.entries.keys()):
                    self.entries[key].delete(0, 'end'); self.entries[key].insert(0, data[i])
            except: pass
            self.hide_dropdown()
        elif event: self.handle_print()

    def handle_print(self):
        data = [self.entries[k].get().strip() for k in self.entries]
        if not data[0]: return
        self.db.save_customer(data)
        generate_html_label(data) # Calling the module function

    def handle_delete(self):
        name = self.entries["Customer Name"].get().strip()
        if name and self.db.get_customer(name) and messagebox.askyesno("Confirm", f"Delete {name}?"):
            self.db.delete_customer(name); self.clear_fields()

    def clear_fields(self):
        for entry in self.entries.values(): entry.delete(0, 'end')
        self.hide_dropdown()

if __name__ == "__main__":
    app = LabelApp()
    app.mainloop()