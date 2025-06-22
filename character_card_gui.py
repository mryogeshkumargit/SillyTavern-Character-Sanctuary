import json
import base64
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from PIL import Image, ImageTk
import os
import zlib
import io

class CharacterCardExtractorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Character Card Sanctuary")
        self.root.geometry("950x750")
        self.root.minsize(800, 600)

        self.current_json_data = None
        self.character_photo = None # To hold a reference to the image
        
        self.setup_styles()
        self.setup_ui()
        
    def setup_styles(self):
        """Configure the sensual, beautiful, and feminine theme."""
        self.primary_bg = '#FFF0F5'      # Lavender Blush
        self.secondary_bg = '#FDF5E6'    # Old Lace (warmer white for content)
        self.content_bg = '#FFFFFF'      # White for the text areas
        self.accent_color = '#E6A4B4'    # Muted Raspberry
        self.active_accent = '#D9859A'   # Deeper Raspberry
        self.text_color = '#5D4037'      # Soft, dark brown
        self.header_color = '#8B008B'    # Dark Magenta
        self.separator_color = '#D1C4E9' # Soft Lavender for separators
        self.font_main = ('Georgia', 11)
        self.font_bold = ('Georgia', 11, 'bold')
        self.font_title = ('Garamond', 20, 'bold', 'italic')
        self.font_tab = ('Georgia', 10, 'bold')
        self.font_details_header = ('Georgia', 14, 'italic')
        self.font_json = ('Consolas', 10)

        style = ttk.Style()
        style.theme_use('clam')

        # --- General Styles ---
        style.configure('.', background=self.primary_bg, foreground=self.text_color, font=self.font_main)
        self.root.configure(background=self.primary_bg)

        # --- Frame Styles ---
        style.configure('TFrame', background=self.primary_bg)
        style.configure('Details.TFrame', background=self.secondary_bg)
        style.configure('TLabelframe', background=self.primary_bg, bordercolor=self.accent_color, font=self.font_bold)
        style.configure('TLabelframe.Label', background=self.primary_bg, foreground=self.header_color, font=self.font_bold)
        
        # --- Button Styles ---
        style.configure('TButton', background=self.accent_color, foreground='white', font=self.font_bold, borderwidth=0, padding=(10, 5))
        style.map('TButton', background=[('active', self.active_accent), ('!disabled', self.accent_color)])

        # --- Notebook (Tabs) Styles ---
        style.configure('TNotebook', background=self.primary_bg, borderwidth=0)
        style.configure('TNotebook.Tab', background=self.primary_bg, foreground=self.text_color, borderwidth=0, padding=(20, 8), font=self.font_tab)
        style.map('TNotebook.Tab', background=[('selected', self.secondary_bg)], foreground=[('selected', self.header_color)])
        
        # --- Scrollbar Style ---
        style.configure('Vertical.TScrollbar', background=self.accent_color, troughcolor=self.primary_bg)


    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)

        title_label = ttk.Label(main_frame, text="Character Card Sanctuary", font=self.font_title, foreground=self.header_color)
        title_label.pack(pady=(0, 20))
        
        file_frame = ttk.LabelFrame(main_frame, text="Select a Character Card", padding="15")
        file_frame.pack(fill=tk.X, pady=(0, 15))
        file_frame.columnconfigure(0, weight=1)
        
        self.file_path_var = tk.StringVar()
        file_entry = ttk.Entry(file_frame, textvariable=self.file_path_var, state='readonly', font=self.font_main)
        file_entry.grid(row=0, column=0, sticky='ew', padx=(0, 10))
        
        browse_button = ttk.Button(file_frame, text="Browse...", command=self.browse_file)
        browse_button.grid(row=0, column=1, padx=(0, 5))
        
        extract_button = ttk.Button(file_frame, text="Reveal Character", command=self.extract_json)
        extract_button.grid(row=0, column=2)
        
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        self.create_welcome_tab()
        
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill=tk.X)
        
        self.save_button = ttk.Button(buttons_frame, text="Save JSON", command=self.save_json, state='disabled')
        self.save_button.pack(side=tk.LEFT, padx=(0, 10))
        self.copy_button = ttk.Button(buttons_frame, text="Copy JSON", command=self.copy_to_clipboard, state='disabled')
        self.copy_button.pack(side=tk.LEFT)
        self.clear_button = ttk.Button(buttons_frame, text="Clear", command=self.clear_results)
        self.clear_button.pack(side=tk.RIGHT)

    def create_welcome_tab(self):
        welcome_frame = ttk.Frame(self.notebook, style='TFrame')
        canvas = tk.Canvas(welcome_frame, bg=self.primary_bg, highlightthickness=0)
        canvas.pack(fill=tk.BOTH, expand=True)
        
        try:
            img_data = b'iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAyZpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADw/eHBhY2tldCBiZWdpbj0i77u/IiBpZD0iVzVNME1wQ2VoaUh6cmVTek5UY3prYzlkIj8+IDx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IkFkb2JlIFhNUCBDb3JlIDUuNi1jMTQwIDc5LjE2MDQ1MSwgMjAxNy8wNS8wNi0wMTowODoyMSAgICAgICAgIj4gPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4gPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIgeG1sbnM6eG1wPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvIiB4bWxuczp4bXBNTT0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL21tLyIgeG1sbnM6c3RSZWY9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9zVHlwZS9SZXNvdXJjZVJlZiMiIHhtcDpDcmVhdG9yVG9vbD0iQWRvYmUgUGhvdG9zaG9wIENDIDIwMTggKFdpbmRvd3MpIiB4bXBNTTpJbnN0YW5jZUlEPSJ4bXAuaWlkOjY1QkE1N0M3NzFEMTExRUFBRDY0RDAxMUI1NDNCNEMxIiB4bXBNTTpEb2N1bWVudElEPSJ4bXAuZGlkOjY1QkE1N0M4NzFEMTExRUFBRDY0RDAxMUI1NDNCNEMxIj4gPHhtcE1NOkRlcml2ZWRGcm9tIHN0UmVmOmluc3RhbmNlSUQ9InhtcC5paWQ6NjVCQTU3QzU3MUQxMTFFQUFENjREMDExQjU0M0I0QzEiIHN0UmVmOmRvY3VtZW50SUQ9InhtcC5kaWQ6NjVCQTU3QzY3MUQxMTFFQUFENjREMDExQjU0M0I0QzEiLz4gPC9yZGY6RGVzY3JpcHRpb24+IDwvcmRmOlJERj4gPC94OnhtcG1ldGE+IDw/eHBhY2tldCBlbmQ9InIiPz6dJTMIAAACzUlEQVR42uzd203DQBAF0L+sARUQCggVBCpIKggqCCoAKggqCCoAKggqwD/gEruxx5J3s91Nckmy5GS/eO/N5rYwCAAAAAAAAAAAAACAlJqmeb/v+2VZtl6XJUmS16U5i4Ig6P8Xj+M4TdM0z3ne931Zlo+279/1/yEAAgABgAAgABCAAgABgAAgABCAAgABgAAgABCAAgABgAAgABCAAgABgAAgABCAAgABgAAgABCAAgABgAAgABCAAgABgAAgABCAAgABgAAgABCAAgABgAAgABCAAgABgAAgABCAAgABgAAgABCAAgABgADg510UxbIsS9N03/d93/d935ZlIQRBKIpipVLpAw/8v6/rer/vS5IkDMMwDMMwDMMwDMPw3/cvCAAAQAAAABAAgAAgABAACAAEQAAgABAACAAEQAAgABAACAAEQAAgABAACAAEQAAgABAACAAEQAAgABAACAAEQAAgABAACAAEQAAgABAACAAEQAAgABAACAAEQAAgABAACAAEQAAgAAwOfB8zyjKMrzvCxL0zSGIYqiKIqiKIr8f13X/b5vWRZFUZIkQRCEIAj+G14AAIAAQAAgABAAgAAgABAACAAEQAAgABAACAAEQAAgABAACAAEQAAgABAACAAEQAAgABAACAAEQAAgABAACAAEQAAgABAACAAEQAAgABAACAAEQAAgABAACAAEQAAgAAMCPSyGEpmmOYxgGQRiGmqZpmqaI4jj+39d1bVmWpmmO45imiqIoDMMYhgAAAAAAAAAA8J2+BRgAU2NC86F4E/EAAAAASUVORK5CYII='
            img_obj = Image.open(io.BytesIO(base64.b64decode(img_data)))
            self.welcome_img = ImageTk.PhotoImage(img_obj)
            canvas.create_image(475, 280, image=self.welcome_img, anchor='center')
        except:
            canvas.create_text(475, 280, text="🌸", font=("Default", 100), anchor='center')

        canvas.create_text(475, 150, text="Welcome to the Sanctuary", font=self.font_title, fill=self.header_color, anchor='center')
        canvas.create_text(475, 200, text="Please select a character card to reveal its soul.", font=('Georgia', 14), fill=self.text_color, anchor='center')
        
        self.notebook.add(welcome_frame, text=' ✨ Welcome ✨ ')

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("PNG files", "*.png")])
        if file_path: self.file_path_var.set(file_path)
    
    def _try_parse_nested_json_string(self, text_value):
        if not isinstance(text_value, str) or not text_value.strip().startswith(('{', '[')): return text_value
        try: return json.loads(text_value)
        except json.JSONDecodeError: return text_value

    def _decode_and_parse_json(self, data_str):
        try: return json.loads(data_str)
        except json.JSONDecodeError: pass
        try: return json.loads(base64.b64decode(data_str).decode('utf-8'))
        except: return None
            
    def extract_json_from_png(self, image_path):
        try:
            with Image.open(image_path) as img:
                all_chunks = {**getattr(img, 'text', {}), **img.info}
                for key in ['chara', 'character', 'data', 'card']:
                    if key in all_chunks:
                        data = all_chunks[key]
                        if isinstance(data, bytes):
                            try: data = zlib.decompress(data).decode('utf-8')
                            except: data = data.decode('utf-8', 'ignore')
                        if (json_data := self._decode_and_parse_json(data)):
                            return self._process_nested_json_fields(json_data)
        except Exception as e: raise Exception(f"Error processing image file: {e}")
        return None

    def _process_nested_json_fields(self, data):
        if isinstance(data, dict): return {k: self._process_nested_json_fields(v) for k, v in data.items()}
        if isinstance(data, list): return [self._process_nested_json_fields(i) for i in data]
        if isinstance(data, str):
            parsed = self._try_parse_nested_json_string(data)
            return self._process_nested_json_fields(parsed) if parsed is not data else data
        return data

    def extract_json(self):
        if not (file_path := self.file_path_var.get()):
            messagebox.showwarning("No File", "Please select a character card.")
            return
        try:
            if (json_data := self.extract_json_from_png(file_path)):
                self.current_json_data = json_data
                self.display_character_data(json_data, file_path)
                self.save_button.config(state='normal')
                self.copy_button.config(state='normal')
            else:
                messagebox.showinfo("No Data", "No character data found in this file.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to extract data:\n{e}")

    def display_character_data(self, json_data, file_path):
        self.clear_tabs()
        
        char_data = json_data.get('data', json_data).copy()
        
        self.create_summary_tab(char_data)

        # Check for lorebook and remove it from the main data to avoid duplication
        lorebook_data = None
        for key in ['character_book', 'lorebook']:
            if key in char_data:
                lorebook_data = char_data.pop(key)
                self.create_lorebook_tab(lorebook_data)
                break
        
        self.create_details_tab(char_data)
        self.create_raw_json_tab(json_data)
        self.create_character_image_tab(file_path)
        self.create_about_tab()
        
        self.notebook.select(0)

    def create_text_widget(self, parent, **kwargs):
        text_widget = scrolledtext.ScrolledText(
            parent, wrap=tk.WORD, font=self.font_main, bg=self.content_bg, fg=self.text_color,
            padx=15, pady=15, relief=tk.FLAT, borderwidth=0, **kwargs)
        text_widget.tag_configure("header", font=self.font_bold, foreground=self.header_color, spacing3=5)
        text_widget.tag_configure("content", font=self.font_main, lmargin1=10, lmargin2=10)
        text_widget.tag_configure("json_code", font=self.font_json, foreground="#006400")
        text_widget.config(state='disabled')
        return text_widget

    def create_summary_tab(self, char_data):
        frame = ttk.Frame(self.notebook, style='Details.TFrame', padding=10)
        widget = self.create_text_widget(frame, height=1)
        widget.pack(fill=tk.BOTH, expand=True)
        widget.config(state='normal')
        
        for key in ['name', 'description', 'personality', 'first_mes']:
            widget.insert(tk.END, f"{key.replace('_', ' ').title()}\n", "header")
            widget.insert(tk.END, f"{char_data.get(key, '[Not Provided]')}\n\n", "content")
            
        widget.config(state='disabled')
        self.notebook.add(frame, text=' 🌹 Summary ')

    def create_lorebook_tab(self, lorebook_data):
        lore_frame = ttk.Frame(self.notebook, style='Details.TFrame', padding=(10, 10, 0, 10))
        
        text_widget = tk.Text(lore_frame, wrap=tk.WORD, font=self.font_main, bg=self.secondary_bg, 
                              fg=self.text_color, padx=20, pady=10, relief=tk.FLAT, 
                              highlightthickness=0, spacing1=5, spacing3=5)
        
        text_widget.tag_configure("entry_title", font=self.font_details_header, foreground=self.header_color, spacing3=10)
        text_widget.tag_configure("field_title", font=self.font_bold, lmargin1=15, lmargin2=15)
        text_widget.tag_configure("content", font=self.font_main, lmargin1=30, lmargin2=30)
        text_widget.tag_configure("separator", overstrike=True, foreground=self.separator_color)

        if isinstance(lorebook_data, dict) and 'entries' in lorebook_data:
            entries = lorebook_data.get('entries', [])
            for i, entry in enumerate(entries):
                entry_name = entry.get('comment') or entry.get('name') or f"Entry {i+1}"
                text_widget.insert(tk.END, f"{entry_name}\n", "entry_title")
                
                keys = entry.get('keys', [])
                if keys:
                    text_widget.insert(tk.END, "Keys:\n", "field_title")
                    text_widget.insert(tk.END, f"{', '.join(keys)}\n\n", "content")

                content = entry.get('content', '[No Content]')
                text_widget.insert(tk.END, "Content:\n", "field_title")
                text_widget.insert(tk.END, f"{content}\n", "content")
                
                separator_line = ' ' * 150 + '\n'
                text_widget.insert(tk.END, separator_line, "separator")

        text_widget.config(state='disabled')
        
        scrollbar = ttk.Scrollbar(lore_frame, orient="vertical", command=text_widget.yview, style='Vertical.TScrollbar')
        text_widget['yscrollcommand'] = scrollbar.set
        
        scrollbar.pack(side="right", fill="y")
        text_widget.pack(side="left", fill="both", expand=True)

        self.notebook.add(lore_frame, text=' 📖 Lorebook ')


    def create_details_tab(self, char_data):
        details_frame = ttk.Frame(self.notebook, style='Details.TFrame', padding=(10, 10, 0, 10))
        
        text_widget = tk.Text(details_frame, wrap=tk.WORD, font=self.font_main, bg=self.secondary_bg, 
                              fg=self.text_color, padx=20, pady=10, relief=tk.FLAT, 
                              highlightthickness=0, spacing1=5, spacing3=5)
        
        text_widget.tag_configure("title", font=self.font_details_header, foreground=self.header_color, spacing3=10)
        text_widget.tag_configure("content", font=self.font_main, lmargin1=15, lmargin2=15)
        text_widget.tag_configure("json_content", font=self.font_json, lmargin1=15, lmargin2=15, foreground="#4A148C")
        text_widget.tag_configure("separator", overstrike=True, foreground=self.separator_color)

        for key, value in char_data.items():
            text_widget.insert(tk.END, f"{key.replace('_', ' ').title()}\n", "title")
            
            if isinstance(value, (dict, list)):
                content = json.dumps(value, indent=2, ensure_ascii=False)
                text_widget.insert(tk.END, f"{content}\n", "json_content")
            else:
                content = str(value)
                text_widget.insert(tk.END, f"{content}\n", "content")
            
            separator_line = ' ' * 150 + '\n'
            text_widget.insert(tk.END, separator_line, "separator")

        text_widget.config(state='disabled')
        
        scrollbar = ttk.Scrollbar(details_frame, orient="vertical", command=text_widget.yview, style='Vertical.TScrollbar')
        text_widget['yscrollcommand'] = scrollbar.set
        
        scrollbar.pack(side="right", fill="y")
        text_widget.pack(side="left", fill="both", expand=True)

        self.notebook.add(details_frame, text=' 💎 Details ')

    def create_raw_json_tab(self, json_data):
        frame = ttk.Frame(self.notebook, style='Details.TFrame', padding=10)
        widget = self.create_text_widget(frame)
        widget.pack(fill=tk.BOTH, expand=True)
        widget.config(state='normal')
        widget.insert(tk.END, json.dumps(json_data, indent=2, ensure_ascii=False), "json_code")
        widget.config(state='disabled')
        self.notebook.add(frame, text=' 📜 Raw JSON ')

    def create_character_image_tab(self, file_path):
        image_frame = ttk.Frame(self.notebook, style='Details.TFrame')

        try:
            original_image = Image.open(file_path)
            max_width, max_height = 800, 600
            original_image.thumbnail((max_width, max_height), Image.LANCZOS)
            
            self.character_photo = ImageTk.PhotoImage(original_image)

            image_label = ttk.Label(image_frame, image=self.character_photo, background=self.secondary_bg)
            image_label.pack(pady=20, padx=20, expand=True)

        except Exception as e:
            error_label = ttk.Label(image_frame, text=f"Could not load image:\n{e}", font=self.font_main, background=self.secondary_bg)
            error_label.pack(pady=20, padx=20, expand=True)

        self.notebook.add(image_frame, text=' 🖼️ Portrait ')

    def create_about_tab(self):
        about_frame = ttk.Frame(self.notebook, style='Details.TFrame', padding=20)
        
        text_widget = tk.Text(about_frame, wrap=tk.WORD, font=self.font_main, bg=self.secondary_bg,
                              fg=self.text_color, relief=tk.FLAT, highlightthickness=0,
                              spacing1=5, spacing3=10)
        
        text_widget.tag_configure("header", font=('Georgia', 16, 'bold', 'italic'), foreground=self.header_color, justify='center')
        text_widget.tag_configure("subheader", font=self.font_bold, foreground=self.header_color)
        text_widget.tag_configure("creator", font=self.font_main, justify='center')
        text_widget.tag_configure("email", font=('Georgia', 11, 'italic'), foreground='#6A1B9A', justify='center')
        text_widget.tag_configure("content", font=self.font_main)
        
        text_widget.insert(tk.END, "Character Card Sanctuary\n\n", "header")
        
        text_widget.insert(tk.END, "Created with care by\n", "creator")
        text_widget.insert(tk.END, "Yogesh Kumar Singh\n", ('creator', 'bold'))
        text_widget.insert(tk.END, "yogeshatreliance@gmail.com\n\n", "email")

        text_widget.insert(tk.END, "How to Use This Sanctuary:\n\n", "subheader")
        
        how_to_use_text = (
            "1.  Click the 'Browse...' button to select a Character Card PNG file from your computer.\n\n"
            "2.  Once selected, click the 'Reveal Character' button to extract the soul of the card.\n\n"
            "3.  The character's essence will be revealed across several tabs:\n"
            "    •  🌹 Summary: A quick glance at the character's core traits.\n"
            "    •  📖 Lorebook: A dedicated space for the character's history, if available.\n"
            "    •  💎 Details: An in-depth look at all other character data.\n"
            "    •  🖼️ Portrait: A view of the character's image.\n"
            "    •  📜 Raw JSON: The unprocessed data for technical users.\n\n"
            "4.  You can save the extracted data as a .json file or copy it to your clipboard using the buttons at the bottom."
        )
        text_widget.insert(tk.END, how_to_use_text, "content")
        
        text_widget.config(state='disabled')
        text_widget.pack(fill=tk.BOTH, expand=True)

        self.notebook.add(about_frame, text=' ❤️ About ')

    def save_json(self):
        if not self.current_json_data: return
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(self.current_json_data, f, indent=2, ensure_ascii=False)
                messagebox.showinfo("Success", f"Data saved to:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save JSON: {e}")
    
    def copy_to_clipboard(self):
        if not self.current_json_data: return
        self.root.clipboard_clear()
        self.root.clipboard_append(json.dumps(self.current_json_data, indent=2, ensure_ascii=False))
        messagebox.showinfo("Success", "JSON copied to clipboard!")
        
    def clear_tabs(self):
        for i in reversed(range(self.notebook.index('end'))): self.notebook.forget(i)

    def clear_results(self):
        self.clear_tabs()
        self.create_welcome_tab()
        self.current_json_data = None
        self.save_button.config(state='disabled')
        self.copy_button.config(state='disabled')
        self.file_path_var.set("")

def main():
    root = tk.Tk()
    app = CharacterCardExtractorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
