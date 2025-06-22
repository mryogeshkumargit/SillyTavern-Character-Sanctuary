# 🌸 Character Card Sanctuary 🌸

A beautiful, sensual, and robust desktop application for viewing the soul of AI character cards.

This application provides an elegant and intuitive interface to extract and display the hidden JSON data within character card PNG files, revealing the character's personality, backstory, and portrait in a beautifully organized tabbed view.


---

### ✨ Features

* **Elegant & Sensual UI**: A user interface designed with a soft, feminine aesthetic, featuring a delicate color palette and graceful typography.
* **Intelligent Data Extraction**: Robustly extracts character data from various PNG metadata formats (`chara`, `tEXt`, `zTXt`).
* **Organized Tabbed Interface**: Displays character information in beautifully arranged tabs:
    * **🌹 Summary**: An at-a-glance overview of the character's most essential traits.
    * **📖 Lorebook**: A dedicated, formatted view for the character's extensive `character_book` or `lorebook` entries.
    * **💎 Details**: A comprehensive look at all other character data points, each presented cleanly.
    * **🖼️ Portrait**: A dedicated tab to showcase the character's image.
    * **📜 Raw JSON**: The complete, unprocessed data for technical users and developers.
    * **❤️ About**: Information about the application and its creator.
* **Robust & Performant**: Built to handle complex and long data fields without sacrificing speed or responsiveness.
* **Save & Copy**: Easily save the full character data to a `.json` file or copy it to your clipboard.

---

### 🛠️ How to Use

1.  **Run the Application**:
    * Ensure you have Python installed on your system.
    * Install the required library, Pillow:
        ```bash
        pip install Pillow
        ```
    * Save the application code as a Python file (e.g., `sanctuary.py`).
    * Run it from your terminal:
        ```bash
        python sanctuary.py
        ```

2.  **Reveal a Character**:
    * Click the **"Browse..."** button to open a file dialog.
    * Select a character card `.png` file from your computer.
    * Click the **"Reveal Character"** button.

3.  **Explore the Sanctuary**:
    * Navigate through the tabs to explore the character's summary, lore, details, and portrait.
    * Use the **"Save JSON"** or **"Copy JSON"** buttons to export the character's data.

---

### ❤️ Created With Care By

**Yogesh Kumar Singh**

(yogeshatreliance@gmail.com)

---

### 📜 License

This project is open-source and available for personal and non-commercial use. Feel free to fork, modify, and share with love.
