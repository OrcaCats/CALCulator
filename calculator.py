import customtkinter as ctk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.ticker import MultipleLocator
import re

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class Calculator(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Graphing Calculator")
        self.geometry("1000x650")
        self.minsize(800, 500)

        # Lavender Purple accent colors
        self.accent_color = "#B39DDB"
        self.accent_hover_color = "#9575CD"
        self.op_color = "#7E57C2"
        self.op_hover_color = "#5E35B1"
        
        self.is_dark_mode = True

        # Main Layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1) # Left panel (equations)
        self.grid_columnconfigure(1, weight=3) # Right panel (graph)

        # --- Left Panel (Equations & Controls) ---
        self.left_panel = ctk.CTkFrame(self, fg_color=("gray95", "gray15"), corner_radius=0, width=300)
        self.left_panel.grid(row=0, column=0, sticky="nsew")
        self.left_panel.grid_rowconfigure(1, weight=1)
        self.left_panel.grid_columnconfigure(0, weight=1)

        # Top bar in left panel
        self.top_bar = ctk.CTkFrame(self.left_panel, fg_color="transparent")
        self.top_bar.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        self.top_bar.grid_columnconfigure(0, weight=1)

        self.theme_switch = ctk.CTkSwitch(self.top_bar, text="Dark Mode", 
                                          command=self.toggle_theme, 
                                          progress_color=self.op_color,
                                          button_color=self.accent_color,
                                          button_hover_color=self.accent_hover_color)
        self.theme_switch.select()
        self.theme_switch.grid(row=0, column=0, sticky="w")

        self.kb_button = ctk.CTkButton(self.top_bar, text="⌨", width=40,
                                       command=self.toggle_keyboard)
        self.kb_button.grid(row=0, column=1, sticky="e")

        # Equations List
        self.equations_frame = ctk.CTkScrollableFrame(self.left_panel, fg_color="transparent")
        self.equations_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)

        self.equations = []
        self.focused_entry = None
        
        # Focus out click handler
        self.bind("<Button-1>", self.on_click_anywhere)

        self.add_equation_entry()

        # Add equation button
        self.add_eq_btn = ctk.CTkButton(self.left_panel, text="+ Add Expression", 
                                        fg_color="transparent", text_color=self.accent_color,
                                        hover_color=("gray85", "gray25"),
                                        command=self.add_equation_entry)
        self.add_eq_btn.grid(row=2, column=0, sticky="ew", padx=10, pady=10)

        # Detail Slider Frame
        self.slider_frame = ctk.CTkFrame(self.left_panel, fg_color="transparent")
        self.slider_frame.grid(row=3, column=0, sticky="ew", padx=10, pady=5)
        
        self.slider_label = ctk.CTkLabel(self.slider_frame, text="Points: 400")
        self.slider_label.pack(side="top", pady=(0, 5))
        
        self.detail_slider = ctk.CTkSlider(self.slider_frame, from_=50, to=1000, 
                                           command=self.on_slider_change,
                                           progress_color=self.op_color,
                                           button_color=self.accent_color,
                                           button_hover_color=self.accent_hover_color)
        self.detail_slider.set(400)
        self.detail_slider.pack(side="top", fill="x")

        # Riemann Slider Frame
        self.riemann_slider_frame = ctk.CTkFrame(self.left_panel, fg_color="transparent")
        self.riemann_slider_frame.grid(row=4, column=0, sticky="ew", padx=10, pady=5)
        
        self.riemann_slider_label = ctk.CTkLabel(self.riemann_slider_frame, text="Riemann N: 10")
        self.riemann_slider_label.pack(side="top", pady=(0, 5))
        
        self.riemann_slider = ctk.CTkSlider(self.riemann_slider_frame, from_=1, to=1000, 
                                           command=self.on_riemann_slider_change,
                                           progress_color=self.op_color,
                                           button_color=self.accent_color,
                                           button_hover_color=self.accent_hover_color)
        self.riemann_slider.set(10)
        self.riemann_slider.pack(side="top", fill="x")

        # Rounded Value Toggle Frame
        self.toggle_frame = ctk.CTkFrame(self.left_panel, fg_color="transparent")
        self.toggle_frame.grid(row=5, column=0, sticky="ew", padx=10, pady=5)
        
        self.rounded_value_var = ctk.BooleanVar(value=False)
        self.rounded_value_switch = ctk.CTkSwitch(self.toggle_frame, text="Rounded Numerical Value", 
                                                  variable=self.rounded_value_var,
                                                  command=self.replot, 
                                                  progress_color=self.op_color,
                                                  button_color=self.accent_color,
                                                  button_hover_color=self.accent_hover_color)
        self.rounded_value_switch.pack(side="left", padx=5)

        # Deriv Slider Frame
        self.deriv_slider_frame = ctk.CTkFrame(self.left_panel, fg_color="transparent")
        self.deriv_slider_frame.grid(row=6, column=0, sticky="ew", padx=10, pady=5)
        
        self.deriv_slider_label = ctk.CTkLabel(self.deriv_slider_frame, text="Deriv Distance (h): 0.100")
        self.deriv_slider_label.pack(side="top", pady=(0, 5))
        
        self.deriv_slider = ctk.CTkSlider(self.deriv_slider_frame, from_=0.001, to=2.0, 
                                           command=self.on_deriv_slider_change,
                                           progress_color=self.op_color,
                                           button_color=self.accent_color,
                                           button_hover_color=self.accent_hover_color)
        self.deriv_slider.set(0.1)
        self.deriv_slider.pack(side="top", fill="x")

        # --- Hovering Keyboard ---
        self.keyboard_visible = False
        self.keyboard_frame = ctk.CTkFrame(self, fg_color=("gray90", "gray20"), corner_radius=10, border_width=1, border_color=("gray70", "gray30"))
        self.setup_keyboard()

        # --- Right Panel (Graph) ---
        self.right_panel = ctk.CTkFrame(self, fg_color=("white", "gray10"), corner_radius=0)
        self.right_panel.grid(row=0, column=1, sticky="nsew")
        self.right_panel.grid_rowconfigure(0, weight=1)
        self.right_panel.grid_columnconfigure(0, weight=1)

        self.figure, self.ax = plt.subplots(figsize=(6, 6), dpi=100)
        self.figure.subplots_adjust(left=0.05, right=0.95, bottom=0.05, top=0.95)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.right_panel)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

        # Panning and zooming state
        self.current_xlim = (-10, 10)
        self.current_ylim = (-10, 10)
        self.panning = False
        self.pan_start_x_px = None
        self.pan_start_y_px = None
        self.pan_start_xlim = None
        self.pan_start_ylim = None

        self.canvas.mpl_connect('scroll_event', self.on_scroll)
        self.canvas.mpl_connect('button_press_event', self.on_press)
        self.canvas.mpl_connect('button_release_event', self.on_release)
        self.canvas.mpl_connect('motion_notify_event', self.on_motion)

        # Setup plot style
        self.replot()

    def on_slider_change(self, value):
        self.slider_label.configure(text=f"Points: {int(value)}")
        self.replot()

    def on_riemann_slider_change(self, value):
        self.riemann_slider_label.configure(text=f"Riemann N: {int(value)}")
        self.replot()

    def on_deriv_slider_change(self, value):
        self.deriv_slider_label.configure(text=f"Deriv Distance (h): {value:.3f}")
        self.replot()

    def set_focused_entry(self, entry):
        self.focused_entry = entry

    def on_click_anywhere(self, event):
        # We don't necessarily clear focus, it's nice to keep the last focused entry for the keyboard
        pass

    def add_equation_entry(self):
        row = len(self.equations)
        frame = ctk.CTkFrame(self.equations_frame, fg_color=("gray90", "gray20"), corner_radius=8)
        frame.pack(fill="x", pady=5)
        
        color_idx = row % len(plt.rcParams['axes.prop_cycle'].by_key()['color'])
        colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
        line_color = colors[color_idx]
        
        color_lbl = ctk.CTkLabel(frame, text="~", text_color=line_color, font=("Helvetica", 24, "bold"), width=30)
        color_lbl.pack(side="left", padx=5)
        
        var = ctk.StringVar()
        entry = ctk.CTkEntry(frame, textvariable=var, font=("Helvetica", 18), 
                             border_width=0, fg_color="transparent")
                             
        def on_var_change(*args):
            text = var.get()
            new_text = re.sub(r'int\((.*?),\s*([^,]+?),\s*([^,)]+)\)', r'∫_\2^\3(\1)', text)
            new_text = re.sub(r'deriv\((.*?),\s*([^,)]+)\)', r'd/dx(\1)|_\2', new_text)
            if new_text != text:
                var.set(new_text)
                try:
                    entry.icursor("end")
                except:
                    pass
                return
            self.replot()
            
        var.trace_add("write", on_var_change)
        
        eq_dict = {}
        
        entry.bind("<FocusIn>", lambda e, en=entry: self.set_focused_entry(en))
        
        del_btn = ctk.CTkButton(frame, text="✕", width=20, height=20, 
                                fg_color="transparent", text_color="gray50",
                                hover_color=("gray80", "gray30"),
                                command=lambda eq=eq_dict: self.delete_equation(eq))
        del_btn.pack(side="right", padx=5)
        
        val_lbl = ctk.CTkLabel(frame, text="", font=("Helvetica", 12), text_color="gray60")
        val_lbl.pack(side="right", padx=5)
        
        entry.pack(side="left", fill="x", expand=True, padx=5, pady=5)
        
        eq_dict.update({'var': var, 'entry': entry, 'frame': frame, 'color': line_color, 'val_lbl': val_lbl})
        
        self.equations.append(eq_dict)
        self.set_focused_entry(entry)
        entry.focus()

    def delete_equation(self, eq_dict):
        eq_dict['frame'].destroy()
        if eq_dict in self.equations:
            self.equations.remove(eq_dict)
        if self.focused_entry == eq_dict['entry']:
            self.focused_entry = None
            if self.equations:
                self.set_focused_entry(self.equations[-1]['entry'])
        self.replot()

    def setup_keyboard(self):
        for i in range(5):
            self.keyboard_frame.grid_columnconfigure(i, weight=1)
        for i in range(6):
            self.keyboard_frame.grid_rowconfigure(i, weight=1)

        buttons = [
            ('x', 0, 0, 1), ('y', 0, 1, 1), ('sin', 0, 2, 1), ('cos', 0, 3, 1), ('tan', 0, 4, 1),
            ('7', 1, 0, 1), ('8', 1, 1, 1), ('9', 1, 2, 1), ('(', 1, 3, 1), (')', 1, 4, 1),
            ('4', 2, 0, 1), ('5', 2, 1, 1), ('6', 2, 2, 1), ('*', 2, 3, 1), ('/', 2, 4, 1),
            ('1', 3, 0, 1), ('2', 3, 1, 1), ('3', 3, 2, 1), ('+', 3, 3, 1), ('-', 3, 4, 1),
            ('0', 4, 0, 1), (',', 4, 1, 1), ('.', 4, 2, 1), ('^', 4, 3, 1), ('=', 4, 4, 1),
            ('C', 5, 0, 1), ('∫', 5, 1, 1), ('d/dx', 5, 2, 1), ('DEL', 5, 3, 2)
        ]

        for btn in buttons:
            text = btn[0]
            row = btn[1]
            col = btn[2]
            colspan = btn[3] if len(btn) > 3 else 1
            
            if text in ['/', '*', '-', '+', '^', 'sin', 'cos', 'tan', 'x', 'y', '(', ')', '=', '∫', 'd/dx', ',']:
                fg = self.op_color
                hover = self.op_hover_color
                text_color = "white"
            elif text in ['C', 'DEL']:
                fg = self.accent_color
                hover = self.accent_hover_color
                text_color = "black"
            else:
                fg = ("gray80", "gray30")
                hover = ("gray65", "gray40")
                text_color = ("black", "white")

            b = ctk.CTkButton(self.keyboard_frame, text=text, width=50, height=40,
                              font=("Helvetica", 16),
                              fg_color=fg, hover_color=hover, text_color=text_color,
                              command=lambda t=text: self.on_keyboard_click(t))
            b.grid(row=row, column=col, columnspan=colspan, sticky="nsew", padx=3, pady=3)

    def toggle_keyboard(self):
        if self.keyboard_visible:
            self.keyboard_frame.place_forget()
            self.keyboard_visible = False
        else:
            self.keyboard_frame.place(relx=0.02, rely=0.98, anchor="sw")
            self.keyboard_visible = True

    def on_keyboard_click(self, char):
        if not self.focused_entry:
            if self.equations:
                self.set_focused_entry(self.equations[-1]['entry'])
            else:
                return

        entry = self.focused_entry
        if char == 'C':
            entry.delete(0, 'end')
        elif char == 'DEL':
            pos = entry.index("insert")
            if pos > 0:
                entry.delete(pos - 1, pos)
        elif char in ['sin', 'cos', 'tan', '∫', 'd/dx']:
            pos = entry.index("insert")
            if char == '∫':
                entry.insert(pos, 'int(')
            elif char == 'd/dx':
                entry.insert(pos, 'deriv(')
            else:
                entry.insert(pos, char + '(')
        else:
            pos = entry.index("insert")
            entry.insert(pos, char)

    def on_scroll(self, event):
        if event.inaxes != self.ax: return
        base_scale = 1.2
        scale_factor = 1/base_scale if event.button == 'up' else base_scale
        
        cur_xlim = self.current_xlim
        cur_ylim = self.current_ylim
        
        xdata = event.xdata
        ydata = event.ydata
        if xdata is None or ydata is None: return
        
        new_width = (cur_xlim[1] - cur_xlim[0]) * scale_factor
        new_height = (cur_ylim[1] - cur_ylim[0]) * scale_factor
        
        relx = (xdata - cur_xlim[0]) / (cur_xlim[1] - cur_xlim[0])
        rely = (ydata - cur_ylim[0]) / (cur_ylim[1] - cur_ylim[0])
        
        self.current_xlim = (xdata - new_width * relx, xdata + new_width * (1 - relx))
        self.current_ylim = (ydata - new_height * rely, ydata + new_height * (1 - rely))
        
        self.replot()

    def on_press(self, event):
        if event.button == 1 and event.inaxes == self.ax:
            self.panning = True
            self.pan_start_x_px = event.x
            self.pan_start_y_px = event.y
            self.pan_start_xlim = self.current_xlim
            self.pan_start_ylim = self.current_ylim

    def on_release(self, event):
        if event.button == 1:
            self.panning = False

    def on_motion(self, event):
        if not self.panning or event.inaxes != self.ax: return
        
        dx_px = event.x - self.pan_start_x_px
        dy_px = event.y - self.pan_start_y_px
        
        xlim_range = self.pan_start_xlim[1] - self.pan_start_xlim[0]
        ylim_range = self.pan_start_ylim[1] - self.pan_start_ylim[0]
        
        dx_data = dx_px * xlim_range / self.ax.bbox.width
        dy_data = dy_px * ylim_range / self.ax.bbox.height
        
        self.current_xlim = (self.pan_start_xlim[0] - dx_data, self.pan_start_xlim[1] - dx_data)
        self.current_ylim = (self.pan_start_ylim[0] - dy_data, self.pan_start_ylim[1] - dy_data)
        
        self.replot()

    def toggle_theme(self):
        self.is_dark_mode = not self.is_dark_mode
        if self.is_dark_mode:
            ctk.set_appearance_mode("Dark")
            self.theme_switch.configure(text="Dark Mode")
        else:
            ctk.set_appearance_mode("Light")
            self.theme_switch.configure(text="Light Mode")
        self.replot()

    def replot(self):
        self.ax.clear()
        
        self.ax.spines['left'].set_position('zero')
        self.ax.spines['bottom'].set_position('zero')
        self.ax.spines['right'].set_color('none')
        self.ax.spines['top'].set_color('none')
        
        self.ax.xaxis.set_ticks_position('bottom')
        self.ax.yaxis.set_ticks_position('left')
        
        self.ax.xaxis.set_major_locator(MultipleLocator(2))
        self.ax.yaxis.set_major_locator(MultipleLocator(2))
        
        self.ax.grid(True, linestyle=':', alpha=0.6)
        
        if self.is_dark_mode:
            bg_color = '#1a1a1a'
            fg_color = 'white'
        else:
            bg_color = 'white'
            fg_color = 'black'
            
        self.ax.set_facecolor(bg_color)
        self.figure.patch.set_facecolor(bg_color)
        self.ax.tick_params(colors=fg_color)
        for spine in self.ax.spines.values():
            spine.set_edgecolor(fg_color)

        N = int(self.detail_slider.get()) if hasattr(self, 'detail_slider') else 400
        x_1d = np.linspace(self.current_xlim[0], self.current_xlim[1], N)
        y_1d = np.linspace(self.current_ylim[0], self.current_ylim[1], N)
        
        allowed_names = {k: v for k, v in np.__dict__.items() if not k.startswith("__")}
        
        for eq_dict in self.equations:
            expr = eq_dict['var'].get().strip()
            if not expr:
                if 'val_lbl' in eq_dict:
                    eq_dict['val_lbl'].configure(text="")
                continue
                
            expr_lower = expr.lower()
            
            is_explicit_x = True
            is_explicit_y = False
            is_implicit = False
            
            lhs, rhs = 'y', expr_lower
            if '=' in expr_lower:
                parts = expr_lower.split('=', 1)
                lhs = parts[0].strip()
                rhs = parts[1].strip()
                if not rhs:
                    if 'val_lbl' in eq_dict:
                        eq_dict['val_lbl'].configure(text="")
                    continue
            
            # Check for derivative
            deriv_match = re.match(r'^d/dx\((.*)\)\|_([^\|]+)$', rhs)
            deriv_alt_match = re.match(r'^deriv\((.*),\s*([^,]+)\)$', rhs)
            
            if deriv_match or deriv_alt_match:
                if deriv_match:
                    func_str = deriv_match.group(1)
                    a_str = deriv_match.group(2)
                else:
                    func_str = deriv_alt_match.group(1)
                    a_str = deriv_alt_match.group(2)
                
                try:
                    a_str = a_str.replace('^', '**')
                    func_str = func_str.replace('^', '**')
                    
                    a = eval(a_str, {"__builtins__": {}}, allowed_names)
                    if not isinstance(a, (int, float)):
                        if 'val_lbl' in eq_dict:
                            eq_dict['val_lbl'].configure(text="")
                        continue
                        
                    h = float(self.deriv_slider.get()) if hasattr(self, 'deriv_slider') else 0.1
                    
                    # Plot the curve over the viewing window
                    allowed_names['x'] = x_1d
                    y_eval = eval(func_str, {"__builtins__": {}}, allowed_names)
                    if isinstance(y_eval, (int, float)):
                        y_eval = np.full_like(x_1d, y_eval, dtype=float)
                    self.ax.plot(x_1d, y_eval, color=eq_dict['color'], linewidth=2)
                    
                    # Evaluate points
                    allowed_names['x'] = a
                    ya = eval(func_str, {"__builtins__": {}}, allowed_names)
                    
                    allowed_names['x'] = a + h
                    yah = eval(func_str, {"__builtins__": {}}, allowed_names)
                    
                    # Draw points
                    self.ax.scatter([a, a+h], [ya, yah], color=eq_dict['color'], zorder=5)
                    
                    # Draw secant line
                    slope = (yah - ya) / h
                    intercept = ya - slope * a
                    y_secant = slope * x_1d + intercept
                    self.ax.plot(x_1d, y_secant, color=eq_dict['color'], linestyle='--', linewidth=1.5, alpha=0.8)
                    
                    if hasattr(self, 'rounded_value_var') and self.rounded_value_var.get():
                        # High accuracy central difference
                        eps = 1e-6
                        allowed_names['x'] = a + eps
                        y_plus = eval(func_str, {"__builtins__": {}}, allowed_names)
                        allowed_names['x'] = a - eps
                        y_minus = eval(func_str, {"__builtins__": {}}, allowed_names)
                        exact_slope = (y_plus - y_minus) / (2 * eps)
                        if 'val_lbl' in eq_dict:
                            eq_dict['val_lbl'].configure(text=f"d/dx ≈ {exact_slope:.3f}")
                    else:
                        if 'val_lbl' in eq_dict:
                            eq_dict['val_lbl'].configure(text=f"Sec ≈ {slope:.4f}")
                except Exception as e:
                    if 'val_lbl' in eq_dict:
                        eq_dict['val_lbl'].configure(text="Error")
                continue

            # Check for integral/Riemann sum
            int_match = re.match(r'^int\((.+),\s*([^,]+),\s*([^,]+)\)$', rhs)
            mathprint_match = re.match(r'^∫_([^\^]+)\^([^\(]+)\((.*)\)$', rhs)
            
            if int_match or mathprint_match:
                if int_match:
                    func_str = int_match.group(1)
                    a_str = int_match.group(2)
                    b_str = int_match.group(3)
                else:
                    a_str = mathprint_match.group(1)
                    b_str = mathprint_match.group(2)
                    func_str = mathprint_match.group(3)
                
                try:
                    # Replace ^ with ** for power evaluation
                    a_str = a_str.replace('^', '**')
                    b_str = b_str.replace('^', '**')
                    func_str = func_str.replace('^', '**')
                    
                    a = eval(a_str, {"__builtins__": {}}, allowed_names)
                    b = eval(b_str, {"__builtins__": {}}, allowed_names)
                    
                    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
                        if 'val_lbl' in eq_dict:
                            eq_dict['val_lbl'].configure(text="")
                        continue
                        
                    riemann_N = int(self.riemann_slider.get()) if hasattr(self, 'riemann_slider') else 10
                    
                    # Plot the curve over the viewing window
                    allowed_names['x'] = x_1d
                    y_eval = eval(func_str, {"__builtins__": {}}, allowed_names)
                    if isinstance(y_eval, (int, float)):
                        y_eval = np.full_like(x_1d, y_eval, dtype=float)
                    self.ax.plot(x_1d, y_eval, color=eq_dict['color'], linewidth=2)
                    
                    # Draw Riemann sum rectangles (Left)
                    if riemann_N > 0:
                        x_rects = np.linspace(a, b, riemann_N + 1)
                        x_eval_pts = x_rects[:-1]
                        dx = (b - a) / riemann_N
                        
                        allowed_names['x'] = x_eval_pts
                        y_rects = eval(func_str, {"__builtins__": {}}, allowed_names)
                        if isinstance(y_rects, (int, float)):
                            y_rects = np.full_like(x_eval_pts, y_rects, dtype=float)
                            
                        edge_color = eq_dict['color'] if riemann_N <= 100 else 'none'
                        self.ax.bar(x_eval_pts, y_rects, width=dx, align='edge', color=eq_dict['color'], alpha=0.4, edgecolor=edge_color)
                        
                        # Calculate Riemann sum value
                        riemann_sum = np.sum(y_rects) * dx
                        
                        if hasattr(self, 'rounded_value_var') and self.rounded_value_var.get():
                            # Numerical Integral with N = 10,000 (10k) rounded to 3 decimal places
                            x_10k = np.linspace(a, b, 10001)
                            x_eval_10k = x_10k[:-1]
                            dx_10k = (b - a) / 10000
                            allowed_names['x'] = x_eval_10k
                            y_10k = eval(func_str, {"__builtins__": {}}, allowed_names)
                            if isinstance(y_10k, (int, float)):
                                y_10k = np.full_like(x_eval_10k, y_10k, dtype=float)
                            riemann_sum_10k = np.sum(y_10k) * dx_10k
                            if 'val_lbl' in eq_dict:
                                eq_dict['val_lbl'].configure(text=f"Int ≈ {riemann_sum_10k:.3f}")
                        else:
                            # Standard Riemann sum value
                            if 'val_lbl' in eq_dict:
                                eq_dict['val_lbl'].configure(text=f"R ≈ {riemann_sum:.4f}")
                except Exception as e:
                    if 'val_lbl' in eq_dict:
                        eq_dict['val_lbl'].configure(text="Error")
                continue

            if 'val_lbl' in eq_dict:
                eq_dict['val_lbl'].configure(text="")
                
            # Replace ^ with ** for non-integral equations
            lhs = lhs.replace('^', '**')
            rhs = rhs.replace('^', '**')
            
            if lhs == 'y' or re.match(r'^[a-zA-Z_]\w*\(x\)$', lhs):
                is_explicit_x = True
                is_implicit = False
            elif lhs == 'x' or re.match(r'^[a-zA-Z_]\w*\(y\)$', lhs):
                is_explicit_x = False
                is_explicit_y = True
                is_implicit = False
            else:
                is_implicit = True
                is_explicit_x = False
            
            try:
                if is_explicit_x:
                    allowed_names['x'] = x_1d
                    allowed_names['y'] = y_1d
                    y_eval = eval(rhs, {"__builtins__": {}}, allowed_names)
                    if isinstance(y_eval, (int, float)):
                        y_eval = np.full_like(x_1d, y_eval, dtype=float)
                    self.ax.plot(x_1d, y_eval, color=eq_dict['color'], linewidth=2)
                elif is_explicit_y:
                    allowed_names['x'] = x_1d
                    allowed_names['y'] = y_1d
                    x_eval = eval(rhs, {"__builtins__": {}}, allowed_names)
                    if isinstance(x_eval, (int, float)):
                        x_eval = np.full_like(y_1d, x_eval, dtype=float)
                    self.ax.plot(x_eval, y_1d, color=eq_dict['color'], linewidth=2)
                elif is_implicit:
                    X, Y = np.meshgrid(x_1d, y_1d)
                    allowed_names['x'] = X
                    allowed_names['y'] = Y
                    z_lhs = eval(lhs, {"__builtins__": {}}, allowed_names)
                    z_rhs = eval(rhs, {"__builtins__": {}}, allowed_names)
                    
                    if isinstance(z_lhs, (int, float)): z_lhs = np.full_like(X, z_lhs, dtype=float)
                    if isinstance(z_rhs, (int, float)): z_rhs = np.full_like(X, z_rhs, dtype=float)
                    
                    Z = z_lhs - z_rhs
                    self.ax.contour(X, Y, Z, levels=[0], colors=[eq_dict['color']], linewidths=2)
            except Exception as e:
                pass 
                
        self.ax.set_xlim(self.current_xlim)
        self.ax.set_ylim(self.current_ylim)
        
        self.canvas.draw()

if __name__ == "__main__":
    app = Calculator()
    app.mainloop()
