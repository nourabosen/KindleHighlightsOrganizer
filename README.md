## Overview
This Python script is designed to parse and organize highlights and notes from a Kindle "My Clippings.txt" file. It extracts the highlights and associated notes, removes duplicates and partial duplicates, and writes the organized content into a new file.

## Features
1. **Parsing Highlights and Notes**: The script reads the "My Clippings.txt" file and extracts book titles, highlights, and notes.
2. **Duplicate Removal**: It removes exact duplicates and partial duplicates (where one highlight is a subset of another).
3. **Output Organization**: The organized highlights and notes are written to a new file in a structured format.

## Usage
### Steps to Run the Script
1. **Save the Script**: Save the provided Python script as `Python_Script.py`.
2. **Update File Paths**: Modify the `input_file_path` and `output_file_path` variables in the `main()` function to point to your "My Clippings.txt" file and the desired output file, respectively.
3. **Run the Script**: Execute the script using Python:
   ```bash
   python Python_Script.py
   ```

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
    - It’s rare that people sail beautifully straight through their beautiful lives, always looking beautiful.
    - Enjoyment is a guide to finding the right work for you.
```

## Functions

* **parse_highlights(file_path):** Extracts highlights and notes.
* **remove_duplicates(highlights_dict):** Removes exact duplicates.
* **remove_partial_duplicates(highlights_dict):** Removes partial duplicates.
* **write_organized_highlights(highlights_dict, notes_dict, output_file_path):** Writes organized content to a file.

## Notes
- Ensure the "My Clippings.txt" file is correctly formatted as expected by the script.
- The script assumes that the file follows the standard Kindle highlights format.

## License
This script is provided as-is, without any warranties. Feel free to modify and distribute it as needed.
