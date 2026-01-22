# Kindle Highlights Organizer

A robust, modular Python application for organizing and managing Kindle highlights. It parses "My Clippings.txt", removes duplicates, associates notes with highlights, and exports them into a structured format compatible with outliner apps like Logseq, Obsidian, and Roam Research.

## Overview
This application serves as a **free, local alternative to Readwise**. It takes the raw, unstructured clippings from your Kindle device and transforms them into a clean, organized markdown format. 

Key capabilities include:
- **Smart Parsing**: Robustly handles the Kindle clippings format, identifying Book Titles, Authors, Highlights, and Notes.
- **Intelligent Deduplication**: Automatically removes exact duplicates and handles partial overlaps (e.g., when you re-highlight a larger section, it keeps the most complete version and preserves your notes).
- **Contextual Note Linking**: Correctly associates your notes with the specific highlight they belong to, ensuring no context is lost.

## Features
- **Modern GUI**: A user-friendly, clean interface for easy file selection and processing.
- **Outliner-Ready**: Output is formatted specifically for indentation-based tools (Logseq, Obsidian, etc.).
- **Zero Dependencies**: Built using standard Python libraries (Tkinter), requiring no external package installation.

### Example Input
```plaintext
Designing Your Life (Bill Burnett)
- Your Highlight on page 50 | location 765-765 | Added on Wednesday, 4 September 2024 21:09:37

It’s rare that people sail beautifully straight through their beautiful lives, always looking beautiful.
==========
Designing Your Life (Bill Burnett)
- Your Highlight on page 53 | location 802-803 | Added on Thursday, 5 September 2024 18:15:53

Enjoyment is a guide to finding the right work for you.
==========
```

### Example Output
```plaintext
Designing Your Life (Bill Burnett)
    - "It’s rare that people sail beautifully straight through their beautiful lives, always looking beautiful."
    - "Enjoyment is a guide to finding the right work for you."
```

## Requirements
- Python 3.6 or higher
- Tkinter (Standard Python GUI library, usually included with Python installation)

## Installation
**Download the Project**
  Clone the repository or download the source files to a local directory.
  ```bash
  git clone https://github.com/nourabosen/KindleHighlightsOrganizer.git
  cd KindleHighlightsOrganizer
  ```

## Usage

### Graphical User Interface (GUI)
The recommended way to use the application is via the GUI.

1. **Launch the Application**:
   ```bash
   python kindle_highlights_organizer.py
   ```
2. **Select Input**: Click "Browse File" to locate your `My Clippings.txt` file.
   - *Tip*: On a connected Kindle, this is located in the `documents` folder.
3. **Select Output**: Choose where to save the generated text file.
4. **Run**: Click "START ORGANIZING". The log window will display the progress and summary.

### Command Line Interface (CLI)
For power users who prefer the terminal or want to automate the process:

```bash
# Syntax: python kindle_highlights_organizer.py [Input File] [Output File]
python kindle_highlights_organizer.py "My Clippings.txt" "organized_highlights.txt"
```

## Project Architecture
The application follows a modular architecture to ensure maintainability and separation of concerns:

| File | Description |
|------|-------------|
| **`kindle_highlights_organizer.py`** | **Entry Point**: Handles command-line arguments and initializes the application (CLI or GUI). |
| **`gui.py`** | **Presentation Layer**: Implements the `tkinter` interface, handling user interaction and visual feedback. |
| **`core.py`** | **Business Logic**: Contains the core algorithms for file parsing, duplicate detection, and content processing. |
| **`models.py`** | **Data Layer**: Defines the `Clipping` class data structure. |

## License
This project is open-source and free to use.
