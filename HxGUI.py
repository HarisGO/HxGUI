# HxGUI 5.2 - The Simple, Stable & Powerful CLI (Corrected)
import sys
import re
import os
import subprocess
import tempfile

def show_help():
    print("""
--- HxGUI 5.2 Command Reference ---

**Compiler Commands**
help                   -> Shows this help message.
preview                -> Opens a live preview of your current app.
compile                -> Compiles your commands into a final app.py file.
exit                   -> Quits the compiler.
note: You can write multiple commands on one line separated by a semicolon (;)

**Core Syntax**
window "Title"
screen <name>
show <name>
text "Content" at <r>,<c> on <screen> [options]
button "Content" at <r>,<c> on <screen> [options]
entry "" at <r>,<c> on <screen> [options]

**Options**
name:<widget_name>
action:"<action> <target> [value]"
fg:"<color>"
bg:"<color>"
colspan:<number>

**Actions**
show <screen_name>      -> Switches to a different screen.
quit                    -> Closes the application.
set_entry <entry_name> "" -> Clears the text in an entry field.
append_entry <entry_name> "<text>" -> Adds text to an entry field.
eval_entry <entry_name>   -> Evaluates the math expression in an entry field.
""")

class HxGuiCompiler:
    def reset(self):
        self.python_code, self.setup_code = [], []
        self.widget_counters, self.screens, self.named_widgets = {}, {}, {}
        self.grid_config = {}

    def _get_widget_name(self, widget_type):
        count = self.widget_counters.get(widget_type, 0) + 1
        self.widget_counters[widget_type] = count
        return f"{re.sub(r'[^a-zA-Z0-9_]', '', widget_type)}_{count}"

    def _parse_props(self, prop_str):
        props = {}
        # This regex correctly finds key:"value with spaces" or key:value
        pattern = r'(\w+):(".*?"|\S+)'
        for key, value in re.findall(pattern, prop_str):
            props[key.strip()] = value.strip()
        return props

    def parse(self, hx_code):
        self.reset()
        for line in hx_code.splitlines():
            line = line.strip()
            if not line or line.startswith('#'): continue

            try:
                # This more robust regex captures the whole line structure
                widget_match = re.match(r'(\w+)\s+(".*?")\s+at\s+([\d,]+)\s+on\s+(\w+)(.*)', line)
                simple_match = re.match(r'(\w+)\s+(".*?"|\w+)', line)

                if widget_match:
                    command, content, pos, parent_name, prop_str = widget_match.groups()
                    row, col = pos.split(',')
                    props = self._parse_props(prop_str)
                    
                    if parent_name not in self.grid_config:
                        self.grid_config[parent_name] = {'rows': set(), 'cols': set()}
                    
                    parent_var = self.screens.get(parent_name)
                    self.grid_config[parent_name]['rows'].add(int(row))
                    self.grid_config[parent_name]['cols'].add(int(col))

                    widget_name = props.get('name')
                    widget_var = self._get_widget_name(widget_name or command)
                    if widget_name: self.named_widgets[widget_name] = widget_var

                    action_str = props.pop('action', None)
                    props.pop('name', None)
                    colspan = props.pop('colspan', '1')
                    
                    config_items = [f'{k}={v}' for k, v in props.items()]

                    if command == 'text':
                        args = [parent_var, f'text={content}'] + config_items
                        self.python_code.append(f'{widget_var} = tk.Label({", ".join(args)})')
                    elif command == 'button':
                        action_code = self._generate_action_code(action_str)
                        args = [parent_var, f'text={content}', action_code, 'font=("Arial", 14)'] + config_items
                        valid_args = [arg for arg in args if arg]
                        self.python_code.append(f'{widget_var} = tk.Button({", ".join(valid_args)})')
                    else: # entry
                        args = [parent_var, 'font=("Arial", 20)', 'justify="right"'] + config_items
                        valid_args = [arg for arg in args if arg]
                        self.python_code.append(f'{widget_var} = tk.Entry({", ".join(valid_args)})')

                    self.python_code.append(f'{widget_var}.grid(row={row}, column={col}, columnspan={colspan}, sticky="nsew", padx=1, pady=1)')

                elif simple_match:
                    command, target = simple_match.groups()
                    target = target.strip('"')

                    if command == 'window':
                        self.setup_code.append(f'root.title("{target}")')
                    elif command == 'screen':
                        self.grid_config[target] = {'rows': set(), 'cols': set()}
                        var = self._get_widget_name(f"screen_{target}")
                        self.screens[target] = var
                        self.setup_code.append(f"{var} = tk.Frame(root)")
                    elif command == 'show':
                        self.python_code.append(f"initial_screen = '{target}'")
            except Exception as e:
                print(f"Error parsing line: '{line}'. Details: {e}")

    def _generate_action_code(self, action_str):
        if not action_str: return 'command=lambda: None'
        parts = action_str.strip('"').split()
        action = parts[0]
        target = parts[1] if len(parts) > 1 else None
        value = parts[2] if len(parts) > 2 else None

        if action == 'show' and target: return f"command=lambda: show_screen('{target}')"
        if action == 'quit': return 'command=root.destroy'
        if action == 'set_entry' and target: return f"command=lambda: set_entry_text('{target}', {value or '\"\"'})"
        if action == 'append_entry' and target: return f"command=lambda: append_entry_text('{target}', '{value}')"
        if action == 'eval_entry' and target: return f"command=lambda: evaluate_entry('{target}')"
        return 'command=lambda: None'

    def generate_code_string(self, hx_code):
        self.parse(hx_code)
        if not self.setup_code and not self.python_code: return None

        grid_code = []
        for screen, config in self.grid_config.items():
            screen_var = self.screens.get(screen)
            if screen_var:
                for r in config['rows']: grid_code.append(f"{screen_var}.grid_rowconfigure({r}, weight=1)")
                for c in config['cols']: grid_code.append(f"{screen_var}.grid_columnconfigure({c}, weight=1)")
        
        screen_map = [f"screens['{n}'] = {v}" for n, v in self.screens.items()]
        widget_map = [f"named_widgets['{n}'] = {v}" for n, v in self.named_widgets.items()]

        return f"""
# Generated by HxGUI 5.2
import tkinter as tk

def main():
    root = tk.Tk()
    root.geometry("400x600")

    screens, named_widgets = {{}}, {{}}
    initial_screen = None

    def show_screen(name):
        for s in screens.values(): s.pack_forget()
        if name in screens: screens[name].pack(fill='both', expand=True)

    def set_entry_text(name, text):
        if name in named_widgets:
            named_widgets[name].delete(0, tk.END)
            named_widgets[name].insert(0, text)
    
    def append_entry_text(name, text):
        if name in named_widgets:
            named_widgets[name].insert(tk.END, text)

    def evaluate_entry(name):
        if name in named_widgets:
            try:
                # A safe eval replacement for simple math
                allowed_chars = "0123456789.+-*/() "
                expr = named_widgets[name].get()
                if all(char in allowed_chars for char in expr):
                    result = eval(expr)
                    set_entry_text(name, str(result))
                else:
                    set_entry_text(name, "Invalid Chars")
            except:
                set_entry_text(name, "Error")

    {'\n    '.join(self.setup_code)}
    {'\n    '.join(self.python_code)}
    {'\n    '.join(screen_map)}
    {'\n    '.join(widget_map)}
    {'\n    '.join(grid_code)}
    
    if initial_screen:
        show_screen(initial_screen)
    
    if not root.title(): root.title("HxGUI App")
    root.mainloop()

if __name__ == "__main__":
    main()
"""

def interactive_shell():
    print("--- HxGUI 5.2 Simple CLI (Corrected) ---")
    print("Enter code. Separate commands with ';'. Type 'preview' or 'compile'.")
    compiler = HxGuiCompiler()
    code_lines = []
    while True:
        try:
            line = input("> ")
            cmd = line.strip().lower()

            if cmd == 'exit': break
            elif cmd == 'help': show_help()
            elif cmd in ['preview', 'compile']:
                full_code = "\n".join(code_lines)
                py_code = compiler.generate_code_string(full_code)
                if not py_code:
                    print("No code to process.")
                    continue
                
                if cmd == 'preview':
                    tmp_path = None
                    try:
                        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as tmp:
                            tmp_path = tmp.name
                            tmp.write(py_code)
                        result = subprocess.run([sys.executable, tmp_path], capture_output=True, text=True)
                        if result.returncode != 0:
                            print(f"--- ERROR IN PREVIEW ---\n{result.stderr}------------------------")
                        else:
                            print("Preview finished.")
                    finally:
                        if tmp_path and os.path.exists(tmp_path): os.remove(tmp_path)
                
                elif cmd == 'compile':
                    with open("app.py", 'w', encoding='utf-8') as f:
                        f.write(py_code)
                    print("Successfully compiled to app.py")
            else:
                commands = line.split(';')
                for command in commands:
                    if command.strip():
                        code_lines.append(command.strip())
        except (KeyboardInterrupt, EOFError):
            break
    print("\nExiting.")

if __name__ == "__main__":
    interactive_shell()
