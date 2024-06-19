import tkinter as tk
from tkinter import filedialog, messagebox

class RoundedCanvas(tk.Canvas):
    def __init__(self, master=None, **kwargs):
        tk.Canvas.__init__(self, master, **kwargs)
    def create_rounded_rectangle(self, x1, y1, x2, y2, radius, **kwargs):
        outline_color = kwargs.pop('outline', 'black')
        points = [x1 + radius, y1,
                  x1 + radius, y1,
                  x2 - radius, y1,
                  x2 - radius, y1,
                  x2, y1,
                  x2, y1 + radius,
                  x2, y2 - radius,
                  x2, y2 - radius,
                  x2, y2,
                  x2 - radius, y2,
                  x2 - radius, y2,
                  x1 + radius, y2,
                  x1 + radius, y2,
                  x1, y2,
                  x1, y2 - radius,
                  x1, y2 - radius,
                  x1, y1 + radius,
                  x1, y1 + radius,
                  x1, y1]
        self.create_polygon(points, **kwargs)
        self.create_polygon(points, outline=outline_color)

class CodeMasterSuiteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Code Master Suite")
        self.root.geometry("600x400")  # Adjusted height and width
        self.root.resizable(False, False)  # Disable resizing
        # Remove the window's title bar
        self.root.overrideredirect(True)
        self.create_widgets()
        self.add_dragging_functionality()
        self.code_injected = False  # Track if code is injected
    def create_widgets(self):
        self.title_label = tk.Label(self.root, text="Code Master Suite", font=("Helvetica", 20, "bold"), bg="black",
                                    fg="white")
        self.title_label.pack(fill="x", pady=10)
        self.text_frame = tk.Frame(self.root, bg="black", bd=2, relief="solid", highlightbackground="red",
                                   highlightthickness=2)
        self.text_frame.pack(expand=True, fill='both', pady=5, padx=10)
        self.text_area = tk.Text(self.text_frame, wrap='word', height=10, width=40, bg="black", fg="white",
                                 insertbackground="white")
        self.text_area.pack(expand=True, fill='both', pady=5, padx=5)
        self.button_frame = tk.Frame(self.root, bg="black")
        self.button_frame.pack(pady=5)
        # Function to create rounded buttons
        def rounded_button(parent, text, command, width=180, height=50):
            button = RoundedCanvas(parent, width=width, height=height, bg="black", highlightthickness=0)
            button.pack(side="left", padx=5, pady=5)
            button.bind("<Button-1>", lambda event, c=command: c())
            # Draw rounded rectangle
            button.create_rounded_rectangle(0, 0, width, height, radius=10, fill="black", outline="red")
            button.create_text(width // 2, height // 2, text=text, font=("Helvetica", 12), fill="white")
            button.bind("<Enter>", lambda event, b=button: b.itemconfig(1, fill="darkgray"))  # Change color on hover
            button.bind("<Leave>",
                        lambda event, b=button: b.itemconfig(1, fill="black"))  # Restore color when not hovered
            return button
        self.inject_button = rounded_button(self.button_frame, "Inject", self.inject_code)
        self.execute_button = rounded_button(self.button_frame, "Execute", self.execute_code, state="disabled")  # Disabled initially
        self.button_frame2 = tk.Frame(self.root, bg="black")
        self.button_frame2.pack(pady=5)
        self.load_button = rounded_button(self.button_frame2, "Load From Files", self.load_file)
        self.close_button = rounded_button(self.button_frame2, "Close", self.close_app)
    def load_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py")])
        if self.file_path:
            try:
                with open(self.file_path, 'r') as file:
                    self.code = file.read()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {e}")
    def execute_code(self):
        code = self.text_area.get(1.0, tk.END)
        try:
            exec(code, globals())
        except Exception as e:
            messagebox.showerror("Error", f"Failed to execute code: {e}")
    def inject_code(self):
        if hasattr(self, 'code'):
            self.text_area.delete(1.0, tk.END)  # Clear the text area
            self.text_area.insert(tk.END, self.code)  # Insert the loaded code
            self.code_injected = True  # Set code_injected to True
            self.execute_button.config(state="normal")  # Enable the execute button
        else:
            messagebox.showwarning("Warning", "No code to inject! Please load a file first.")
    def close_app(self):
        self.root.destroy()  # Properly close the application
    def add_dragging_functionality(self):
        self.root.bind("<Button-1>", self.start_move)
        self.root.bind("<ButtonRelease-1>", self.stop_move)
        self.root.bind("<B1-Motion>", self.on_motion)
    def start_move(self, event):
        self.x = event.x
        self.y = event.y
    def stop_move(self, event):
        self.x = None
        self.y = None
    def on_motion(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CodeMasterSuiteApp(root)
    root.configure(bg="black")
    root.mainloop()
