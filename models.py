from typing import List

class Clipping:
    def __init__(self, book: str, author: str, content: str, c_type: str, location_start: int, location_end: int, date_str: str):
        self.book = book
        self.author = author
        self.content = content.strip()
        self.type = c_type
        self.location_start = location_start
        self.location_end = location_end
        self.date_str = date_str
        self.notes: List[str] = []

    def __repr__(self):
        return f"<{self.type} {self.location_start}-{self.location_end}: {self.content[:20]}...>"
