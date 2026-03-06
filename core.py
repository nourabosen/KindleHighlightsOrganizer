import re
import os
from typing import List, Dict, Set, Optional
from collections import defaultdict
from models import Clipping

def parse_clippings_file(file_path: str) -> Dict[str, List[Clipping]]:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(file_path, 'r', encoding='utf-8-sig') as f:
        content = f.read()

    # Split by separator
    blocks = content.split('==========')
    
    clippings_by_book = defaultdict(list)
    
    # Regex for metadata line - handles all Kindle formats:
    # 1. "on page X | location Y-Z"   (ebooks with page + location)
    # 2. "at location Y-Z"            (PDFs / no-page entries)
    # 3. "on page X-Y"                (physical-page-only, no location field)
    meta_pattern = re.compile(
        r"- Your (?P<type>\w+) "
        r"(?:"
        r"on page (?P<page>[\d-]+) \| location (?P<loc1>[\d-]+)"  # format 1: page + location
        r"|at location (?P<loc2>[\d-]+)"                           # format 2: at location only
        r"|on page (?P<page3>[\d-]+)"                              # format 3: page only, no location
        r")"
        r" \| Added on (?P<date>.+)"
    )

    for block in blocks:
        lines = [l.strip() for l in block.strip().split('\n') if l.strip()]
        if len(lines) < 2:
            continue
            
        title_line = lines[0]
        author = ""
        book = title_line
        if "(" in title_line and title_line.endswith(")"):
            match_author = re.search(r"\(([^)]+)\)$", title_line)
            if match_author:
                author = match_author.group(1)
                book = title_line[:match_author.start()].strip()
        
        meta_match = meta_pattern.match(lines[1])
        if not meta_match:
            continue
            
        c_type = meta_match.group("type")
        loc_str = meta_match.group("loc1") or meta_match.group("loc2") or meta_match.group("page3")
        date_str = meta_match.group("date")
        
        if '-' in loc_str:
            start_s, end_s = loc_str.split('-')
            loc_start = int(start_s)
            loc_end = int(end_s)
        else:
            loc_start = int(loc_str)
            loc_end = int(loc_str)
            
        body = "\n".join(lines[2:])
        
        clipping = Clipping(book, author, body, c_type, loc_start, loc_end, date_str)
        clippings_by_book[title_line].append(clipping)

    return clippings_by_book

def process_book_clippings(clippings: List[Clipping]) -> List[Clipping]:
    highlights = []
    notes = []
    
    for c in clippings:
        if c.type == 'Highlight':
            highlights.append(c)
        elif c.type == 'Note':
            notes.append(c)
            
    # Associate notes with highlights
    for note in notes:
        candidates = []
        for h in highlights:
            if not (note.location_end < h.location_start or note.location_start > h.location_end):
                candidates.append(h)
        
        if candidates:
            best_h = candidates[0]
            for h in candidates:
                if h.location_start <= note.location_start and h.location_end >= note.location_end:
                    best_h = h
                    break
            best_h.notes.append(note.content)

    # Remove Exact Duplicates
    unique_highlights = []
    seen_content = set()
    
    for h in highlights:
        if h.content not in seen_content:
            unique_highlights.append(h)
            seen_content.add(h.content)
        else:
            existing = next((x for x in unique_highlights if x.content == h.content), None)
            if existing and h.notes:
                existing.notes.extend(h.notes)

    # Remove Partial Duplicates
    to_remove = set()
    for i in range(len(unique_highlights)):
        if i in to_remove:
            continue
        h1 = unique_highlights[i]
        for j in range(len(unique_highlights)):
            if i == j or j in to_remove:
                continue
            h2 = unique_highlights[j]
            if h1.content in h2.content:
                h2.notes.extend(h1.notes)
                to_remove.add(i)
                break
            
    final_highlights = []
    for i, h in enumerate(unique_highlights):
        if i not in to_remove:
            final_highlights.append(h)
            
    final_highlights.sort(key=lambda x: x.location_start)
    for h in final_highlights:
        h.notes = sorted(list(set(h.notes)))
        
    return final_highlights

def write_output(clippings_by_book: Dict[str, List[Clipping]], output_path: str):
    with open(output_path, 'w', encoding='utf-8') as f:
        for book_title, clippings in clippings_by_book.items():
            processed = process_book_clippings(clippings)
            if not processed:
                continue
                
            f.write(f"{book_title}\n")
            for h in processed:
                clean_content = h.content.replace('\n', ' ')
                f.write(f'    - "{clean_content}"\n')
                for note in h.notes:
                    clean_note = note.replace('\n', ' ')
                    f.write(f'        - Note: *{clean_note}*\n')
            f.write("\n")
