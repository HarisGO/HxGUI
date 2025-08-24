# HxGUI - The Simple GUI Creator

![HxGUI Logo](https://placehold.co/600x300/2c3e50/ffffff?text=HxGUI&font=raleway)

**HxGUI** is a simple, command-line based language and compiler that makes creating graphical user interfaces (GUIs) with Python's Tkinter library incredibly easy. The goal is to provide a syntax so simple that anyone can remember it and build functional desktop applications.

Forget complex boilerplate code. With HxGUI, you write simple, readable commands, preview your app instantly, and compile it into a standalone Python file.

---

## ✨ Features

- **Simple, Memorable Syntax:** Commands are designed to be as close to plain English as possible (`window "Title"`, `button "Click" at 0,0 on main`).
- **Command-Line Interface:** A lightweight, fast, and interactive CLI for writing and managing your code.
- **Live Preview:** Instantly see what your app looks like with the `preview` command without losing your progress.
- **One-Command Compilation:** Generate a clean, standalone `app.py` file with the `compile` command.
- **Powerful Actions:** Easily link buttons to actions like switching screens, updating text, performing calculations, and quitting the app.
- **Multi-Command Input:** Write multiple commands on a single line, separated by a semicolon (`;`), for rapid development.

---

## 🚀 Getting Started

### Prerequisites

- Python 3.x

### Usage

1.  Save the compiler code as `hxgui.py`.
2.  Run the interactive CLI from your terminal:
    ```bash
    python hxgui.py
    ```
3.  You will be greeted with the `>` prompt. Start typing your HxGUI code.
4.  When you're ready, type `preview` on a new line to see your app in action.
5.  Once you're happy with the result, type `compile` to generate `app.py`.
6.  You can then run your new application:
    ```bash
    python app.py
    ```

---

## 💡 Examples

### 1. Simple Two-Page App

This code creates a simple app with a home screen and a settings screen.

```hxgui
# Create the window and screens
window "My App" ; screen home ; screen settings

# Home screen widgets
text "Welcome Home!" at 0,0 on home
button "Go to Settings" at 1,0 on home action:"show settings"

# Settings screen widgets
text "This is the Settings Page" at 0,0 on settings
button "Go Home" at 1,0 on settings action:"show home"

# Set the starting screen
show home
```
## 2. Fully Functional Calculator (One Line)
This demonstrates the power of the multi-command input to create a complete calculator.
```
window "Calculator" ; screen main ; show main ; entry "" at 0,0 on main name:display colspan:4 ; button "C" at 1,0 on main action:"set_entry display" ; button "/" at 1,3 on main action:"append_entry display /" ; button "7" at 2,0 on main action:"append_entry display 7" ; button "8" at 2,1 on main action:"append_entry display 8" ; button "9" at 2,2 on main action:"append_entry display 9" ; button "*" at 2,3 on main action:"append_entry display *" ; button "4" at 3,0 on main action:"append_entry display 4" ; button "5" at 3,1 on main action:"append_entry display 5" ; button "6" at 3,2 on main action:"append_entry display 6" ; button "-" at 3,3 on main action:"append_entry display -" ; button "1" at 4,0 on main action:"append_entry display 1" ; button "2" at 4,1 on main action:"append_entry display 2" ; button "3" at 4,2 on main action:"append_entry display 3" ; button "+" at 4,3 on main action:"append_entry display +" ; button "0" at 5,0 on main action:"append_entry display 0" colspan:2 ; button "." at 5,2 on main action:"append_entry display ." ; button "=" at 5,3 on main action:"eval_entry display"
```
## 📚 Complete Command List
```help``` - Shows this help message.

```preview``` - Opens a live preview of your current app.

```compile``` - Compiles your commands into a final app.py file.

```exit``` - Quits the compiler.

*Core Syntax*

```window "Title"``` - Sets the title of the application window.

```screen <name>``` - Creates a new screen/page.

```show <name>``` - Sets the initial screen to display.

*Widgets*

```text "Content" at <r>,<c> on <screen>``` - Creates a text label.

```button "Content" at <r>,<c> on <screen>``` - Creates a clickable button.

```entry "" at <r>,<c> on <screen>``` - Creates a text input field.

*Options*

```name:<widget_name>``` - Give a widget a unique name for actions.

```action:"<action> <target> [value]"``` - Define what a button does.

```fg:"<color>"``` - Sets the foreground (text) color (e.g., fg:"blue").

```bg:"<color>"``` - Sets the background color (e.g., bg:"#f0f0f0").

```colspan:<number>``` - Makes the widget span multiple columns.

*Actions*

```show <screen_name>``` - Switches to a different screen.

```quit``` - Closes the application.

```set_entry <name>``` "" - Clears an entry field.

```append_entry <name> "<text>"``` - Adds text to an entry field.

```eval_entry <name>``` - Evaluates the math expression in an entry.

## 🤝 Contributing
*Contributions are welcome! If you have ideas for new features, widgets, or improvements to the syntax, feel free to open an issue or submit a pull request.*

## 📄 License
This project is licensed under the Apache 2 Licence. See the LICENSE file for details.
