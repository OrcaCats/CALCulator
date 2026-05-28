import customtkinter as ctk

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class Calculator(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Simple Calculator Preview")
        self.geometry("350x550")
        self.resizable(False, False)

        # Lavender Purple accent colors
        self.accent_color = "#B39DDB"
        self.accent_hover_color = "#9575CD"
        self.op_color = "#7E57C2"
        self.op_hover_color = "#5E35B1"
        
        self.is_dark_mode = True

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Top Frame for theme toggle
        self.top_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.top_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 0))
        self.top_frame.grid_columnconfigure(0, weight=1)

        self.theme_switch = ctk.CTkSwitch(self.top_frame, text="Dark Mode", 
                                          command=self.toggle_theme, 
                                          progress_color=self.op_color,
                                          button_color=self.accent_color,
                                          button_hover_color=self.accent_hover_color)
        self.theme_switch.select()
        self.theme_switch.grid(row=0, column=0, sticky="e")

        # Display
        self.display_var = ctk.StringVar(value="0")
        self.display = ctk.CTkEntry(self, textvariable=self.display_var, 
                                    font=("Helvetica", 40), 
                                    justify="right", 
                                    height=80, 
                                    border_width=0,
                                    corner_radius=10,
                                    fg_color=("gray85", "gray20"))
        self.display.grid(row=1, column=0, sticky="nsew", padx=15, pady=(10, 15))

        # Buttons Frame
        self.buttons_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.buttons_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=(0, 10))

        for i in range(4):
            self.buttons_frame.grid_columnconfigure(i, weight=1)
        for i in range(5):
            self.buttons_frame.grid_rowconfigure(i, weight=1)

        buttons = [
            ('C', 0, 0, 2), ('DEL', 0, 2, 1), ('/', 0, 3, 1),
            ('7', 1, 0, 1), ('8', 1, 1, 1), ('9', 1, 2, 1), ('*', 1, 3, 1),
            ('4', 2, 0, 1), ('5', 2, 1, 1), ('6', 2, 2, 1), ('-', 2, 3, 1),
            ('1', 3, 0, 1), ('2', 3, 1, 1), ('3', 3, 2, 1), ('+', 3, 3, 1),
            ('0', 4, 0, 2), ('.', 4, 2, 1), ('=', 4, 3, 1)
        ]

        for btn in buttons:
            text = btn[0]
            row = btn[1]
            col = btn[2]
            colspan = btn[3] if len(btn) > 3 else 1
            
            if text in ['/', '*', '-', '+', '=']:
                fg = self.op_color
                hover = self.op_hover_color
                text_color = "white"
            elif text in ['C', 'DEL']:
                fg = self.accent_color
                hover = self.accent_hover_color
                text_color = "black"
            else:
                fg = ("gray75", "gray25")
                hover = ("gray60", "gray35")
                text_color = ("black", "white")

            b = ctk.CTkButton(self.buttons_frame, text=text, 
                              font=("Helvetica", 24),
                              fg_color=fg, hover_color=hover, text_color=text_color,
                              command=lambda t=text: self.on_button_click(t))
            b.grid(row=row, column=col, columnspan=colspan, sticky="nsew", padx=5, pady=5)

        self.bind("<Key>", self.on_key_press)

    def toggle_theme(self):
        self.is_dark_mode = not self.is_dark_mode
        if self.is_dark_mode:
            ctk.set_appearance_mode("Dark")
            self.theme_switch.configure(text="Dark Mode")
        else:
            ctk.set_appearance_mode("Light")
            self.theme_switch.configure(text="Light Mode")

    def on_key_press(self, event):
        if event.keysym == 'Return':
            self.on_button_click('=')
        elif event.keysym == 'BackSpace':
            self.on_button_click('DEL')
        elif event.keysym == 'Escape':
            self.on_button_click('C')
        elif event.char in '0123456789+-*/.':
            self.on_button_click(event.char)

    def on_button_click(self, char):
        current = self.display_var.get()
        if current == "Error":
            current = "0"
            self.display_var.set(current)

        if char == 'C':
            self.display_var.set("0")
        elif char == 'DEL':
            if len(current) > 1:
                self.display_var.set(current[:-1])
            else:
                self.display_var.set("0")
        elif char == '=':
            try:
                result = str(eval(current))
                self.display_var.set(result)
            except Exception:
                self.display_var.set("Error")
        else:
            if current == "0" and char not in ['.', '/', '*', '+', '-']:
                self.display_var.set(char)
            else:
                self.display_var.set(current + char)

if __name__ == "__main__":
    app = Calculator()
    app.mainloop()
