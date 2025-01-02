import re

def parse_highlights(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    highlights_dict = {}
    notes_dict = {}
    current_book = None
    current_highlight = None
    current_note = None
    seen_highlights = set()

    for i, line in enumerate(lines):
        line = line.strip()
        
        # Check if the line contains a book title
        if re.match(r"^.+ \(.+\)$", line):
            if current_book:
                # Store the last highlight and note for the previous book
                if current_highlight and current_highlight not in seen_highlights:
                    highlights_dict[current_book].append(current_highlight.strip())
                    seen_highlights.add(current_highlight.strip())
                    if current_note:
                        notes_dict[current_book].append(current_note.strip())
                        current_note = None
            current_book = line
            if current_book not in highlights_dict:
                highlights_dict[current_book] = []
                notes_dict[current_book] = []
            current_highlight = None
            current_note = None

        # Check if the line indicates the start of a highlight
        elif re.match(r"^- Your Highlight .+$", line):
            if current_highlight and current_highlight not in seen_highlights:
                highlights_dict[current_book].append(current_highlight.strip())
                seen_highlights.add(current_highlight.strip())
                if current_note:
                    notes_dict[current_book].append(current_note.strip())
                    current_note = None
            current_highlight = ""

        # Check if the line indicates the start of a note
        elif re.match(r"^- Your Note .+$", line):
            current_note = ""

        # If we're inside a highlight, append the text
        elif current_highlight is not None and line != "==========":
            current_highlight += " " + line

        # If we're inside a note, append the text
        elif current_note is not None and line != "==========":
            current_note += " " + line

        # Store the note when we hit the separator
        if current_note and line == "==========":
            if current_book:
                notes_dict[current_book].append(current_note.strip())
            current_note = None

    # Handle the last entry
    if current_highlight and current_highlight not in seen_highlights:
        highlights_dict[current_book].append(current_highlight.strip())
        seen_highlights.add(current_highlight.strip())
        if current_note:
            notes_dict[current_book].append(current_note.strip())

    return highlights_dict, notes_dict


def remove_duplicates(highlights_dict):
    for book, highlights in highlights_dict.items():
        unique_highlights = []
        seen = set()
        for highlight in highlights:
            if highlight not in seen:
                unique_highlights.append(highlight)
                seen.add(highlight)
        highlights_dict[book] = unique_highlights
    return highlights_dict


def remove_partial_duplicates(highlights_dict):
    for book, highlights in highlights_dict.items():
        unique_highlights = []
        seen = set()
        for highlight in highlights:
            is_partial = False
            for seen_highlight in seen:
                if highlight in seen_highlight:
                    is_partial = True
                    break
                elif seen_highlight in highlight:
                    seen.remove(seen_highlight)
                    unique_highlights.remove(seen_highlight)
                    break
            if not is_partial:
                unique_highlights.append(highlight)
                seen.add(highlight)
        highlights_dict[book] = unique_highlights
    return highlights_dict


def write_organized_highlights(highlights_dict, notes_dict, output_file_path):
    with open(output_file_path, 'w', encoding='utf-8') as file:
        for book, highlights in highlights_dict.items():
            file.write(f"{book}\n")
            for highlight in highlights:
                file.write(f"    - {highlight}\n")
            if book in notes_dict:
                for note in notes_dict[book]:
                    file.write(f"    Note: *{note}*\n")
            file.write("\n")


def main():
    input_file_path = "path/to/My Clippings.txt"  # Replace with your input file path
    output_file_path = "path/to/organized_highlights.txt"  # Replace with your desired output file path

    highlights_dict, notes_dict = parse_highlights(input_file_path)
    highlights_dict = remove_duplicates(highlights_dict)
    highlights_dict = remove_partial_duplicates(highlights_dict)
    write_organized_highlights(highlights_dict, notes_dict, output_file_path)

    print(f"Highlights have been organized and written to {output_file_path}")


if __name__ == "__main__":
    main()
