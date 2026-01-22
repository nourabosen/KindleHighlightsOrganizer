import argparse
import sys
from core import parse_clippings_file, write_output
from gui import run_gui

def main():
    # If no arguments are provided, launch GUI by default
    if len(sys.argv) == 1:
        print("No arguments provided. Launching GUI...")
        try:
            run_gui()
        except ImportError as e:
            print(f"Error launching GUI: {e}")
            print("Usage: python kindle_highlights_organizer.py [input_file] [output_file]")
        return

    parser = argparse.ArgumentParser(description="Organize Kindle Highlights")
    parser.add_argument("input", nargs="?", help="Input clippings file path")
    parser.add_argument("output", nargs="?", help="Output file path")
    parser.add_argument("--gui", action="store_true", help="Launch Graphical User Interface")
    
    args = parser.parse_args()
    
    if args.gui:
        run_gui()
        return
        
    # CLI Mode
    input_path = args.input if args.input else "My Clippings.txt"
    output_path = args.output if args.output else "organized_highlights.txt"

    print(f"Reading from {input_path}...")
    try:
        clippings = parse_clippings_file(input_path)
        
        if not clippings:
            print("No clippings found or file is empty.")
            return

        print(f"Found {sum(len(c) for c in clippings.values())} raw clippings across {len(clippings)} books.")
        print(f"Writing organized highlights to {output_path}...")
        
        write_output(clippings, output_path)
        print("Done!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
