import tkinter as tk
from tkinter import filedialog, messagebox, ttk, font
import threading
import os
from core import parse_clippings_file, write_output

def run_gui():
    class OrganizerApp:
        def __init__(self, root):
            self.root = root
            self.root.title("Kindle Highlights Organizer")
            self.root.geometry("700x550")
            self.root.configure(bg="#f5f7fa")
            
            # Fonts
            self.header_font = font.Font(family="Helvetica", size=16, weight="bold")
            self.label_font = font.Font(family="Helvetica", size=10)
            self.button_font = font.Font(family="Helvetica", size=10, weight="bold")
            
            # Styles
            style = ttk.Style()
            style.theme_use('clam')
            
            # Colors
            bg_color = "#f5f7fa"
            primary_color = "#4a90e2"
            text_color = "#333333"
            white = "#ffffff"
            
            # Configure Styles
            style.configure("TFrame", background=bg_color)
            style.configure("Card.TFrame", background=white, relief="flat")
            
            style.configure("TLabel", background=bg_color, foreground=text_color, font=("Helvetica", 10))
            style.configure("Header.TLabel", font=("Helvetica", 18, "bold"), foreground="#2c3e50")
            style.configure("CardLabel.TLabel", background=white, foreground=text_color, font=("Helvetica", 10, "bold"))
            
            style.configure("TButton", 
                            font=("Helvetica", 10), 
                            padding=10, 
                            background=primary_color, 
                            foreground=white, 
                            borderwidth=0)
            style.map("TButton", 
                      background=[('active', '#357abd'), ('disabled', '#bdc3c7')],
                      foreground=[('disabled', '#ecf0f1')])
            
            style.configure("TEntry", padding=8, relief="flat", borderwidth=1)
            
            # Main Container with Padding
            main_container = ttk.Frame(root, padding="30")
            main_container.pack(fill=tk.BOTH, expand=True)
            
            # Header
            header_frame = ttk.Frame(main_container)
            header_frame.pack(fill=tk.X, pady=(0, 20))
            ttk.Label(header_frame, text="Kindle Highlights Organizer", style="Header.TLabel").pack(anchor=tk.W)
            ttk.Label(header_frame, text="Transform your clippings into structured notes.", font=("Helvetica", 11), foreground="#7f8c8d").pack(anchor=tk.W)
            
            # Input Card
            self.create_file_card(main_container, "Input Source", "Select your 'My Clippings.txt' file", "input", "Browse File")
            
            # Output Card
            self.create_file_card(main_container, "Output Destination", "Choose where to save the organized file", "output", "Save As...")
            
            # Action Area
            action_frame = ttk.Frame(main_container)
            action_frame.pack(fill=tk.X, pady=20)
            
            self.run_btn = ttk.Button(action_frame, text="START ORGANIZING", command=self.start_processing, cursor="hand2")
            self.run_btn.pack(fill=tk.X, ipady=5)
            
            # Log Area
            log_frame = ttk.Frame(main_container)
            log_frame.pack(fill=tk.BOTH, expand=True)
            
            ttk.Label(log_frame, text="Status Log", font=("Helvetica", 9, "bold"), foreground="#95a5a6").pack(anchor=tk.W, pady=(0, 5))
            
            self.log_text = tk.Text(log_frame, height=8, width=50, 
                                    font=("Consolas", 9), 
                                    relief="flat", 
                                    bg="#2c3e50", 
                                    fg="#ecf0f1",
                                    padx=10, pady=10)
            self.log_text.pack(fill=tk.BOTH, expand=True)
            self.log_text.configure(state='disabled')

        def create_file_card(self, parent, title, subtitle, var_type, btn_text):
            card = ttk.Frame(parent, style="Card.TFrame", padding="15")
            card.pack(fill=tk.X, pady=(0, 15))
            
            # Title
            ttk.Label(card, text=title, style="CardLabel.TLabel").pack(anchor=tk.W)
            ttk.Label(card, text=subtitle, background="#ffffff", foreground="#7f8c8d", font=("Helvetica", 9)).pack(anchor=tk.W, pady=(0, 10))
            
            # Input Row
            row = ttk.Frame(card, style="Card.TFrame")
            row.pack(fill=tk.X)
            
            var = tk.StringVar()
            entry = ttk.Entry(row, textvariable=var)
            entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
            
            cmd = self.browse_input if var_type == "input" else self.browse_output
            btn = ttk.Button(row, text=btn_text, command=cmd, style="TButton", width=12)
            btn.pack(side=tk.RIGHT)
            
            if var_type == "input":
                self.input_var = var
            else:
                self.output_var = var

        def log(self, message):
            self.log_text.configure(state='normal')
            self.log_text.insert(tk.END, f"> {message}\n")
            self.log_text.see(tk.END)
            self.log_text.configure(state='disabled')
            self.root.update_idletasks()

        def browse_input(self):
            filename = filedialog.askopenfilename(
                title="Select My Clippings.txt",
                filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
            )
            if filename:
                self.input_var.set(filename)
                # Auto-suggest output name
                directory = os.path.dirname(filename)
                self.output_var.set(os.path.join(directory, "organized_highlights.txt"))

        def browse_output(self):
            filename = filedialog.asksaveasfilename(
                title="Save Organized Highlights As",
                defaultextension=".txt",
                initialfile="organized_highlights.txt",
                filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
            )
            if filename:
                self.output_var.set(filename)

        def start_processing(self):
            input_path = self.input_var.get()
            output_path = self.output_var.get()
            
            if not input_path:
                messagebox.showerror("Error", "Please select an input file.")
                return
            if not output_path:
                messagebox.showerror("Error", "Please select an output path.")
                return
            
            self.run_btn.configure(state='disabled', text="PROCESSING...")
            self.log("Starting process...")
            
            # Run in thread to not freeze UI
            threading.Thread(target=self.process, args=(input_path, output_path), daemon=True).start()

        def process(self, input_path, output_path):
            try:
                self.log(f"Reading file: {os.path.basename(input_path)}")
                clippings = parse_clippings_file(input_path)
                
                if not clippings:
                    self.log("No clippings found or file is empty.")
                    messagebox.showwarning("Warning", "No clippings found.")
                    return

                count = sum(len(c) for c in clippings.values())
                self.log(f"Found {count} highlights/notes in {len(clippings)} books.")
                
                self.log(f"Writing to output file...")
                write_output(clippings, output_path)
                
                self.log("Done! Highlights organized successfully.")
                messagebox.showinfo("Success", "Highlights have been successfully organized!")
                
            except Exception as e:
                self.log(f"Error: {str(e)}")
                messagebox.showerror("Error", f"An error occurred:\n{str(e)}")
            finally:
                self.root.after(0, lambda: self.run_btn.configure(state='normal', text="START ORGANIZING"))

    root = tk.Tk()
    app = OrganizerApp(root)
    root.mainloop()
