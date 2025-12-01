"""
Parser for rFactor .gdb (track) files.

Parses track configuration files to extract basic information like TrackName,
VenueName and optional Layout. Also provides directory scanning utilities.
"""

import re
from pathlib import Path
from typing import Optional, Iterable

from ..models.track import Track


class GdbParser:
    """Parser for .gdb track files."""

    TRACKNAME_RE = re.compile(r"^TrackName\s*=\s*\"?(?P<val>[^\"]+)\"?\s*$", re.IGNORECASE)
    VENUENAME_RE = re.compile(r"^VenueName\s*=\s*\"?(?P<val>[^\"]+)\"?\s*$", re.IGNORECASE)
    LAYOUT_RE = re.compile(r"^Layout\s*=\s*\"?(?P<val>[^\"]+)\"?\s*$", re.IGNORECASE)

    def parse_file(self, file_path: str | Path) -> Optional[Track]:
        """Parse a .gdb file and return a Track object or None if not parsable."""
        file_path = Path(file_path)
        if not file_path.exists() or file_path.suffix.lower() != ".gdb":
            return None

        try:
            # GDB often uses ANSI/Windows-1252 like other rFactor files
            with open(file_path, 'r', encoding='windows-1252', errors='ignore') as f:
                content = f.read()
        except Exception:
            return None

        return self.parse_content(content, str(file_path))

    def parse_content(self, content: str, file_path: str = "") -> Optional[Track]:
        """Parse content of a .gdb file into a Track."""
        track = Track()

        # Reset any previous info
        track.gdb_info = {}

        for raw_line in content.splitlines():
            # Remove comments then strip
            line = raw_line.split("//")[0].strip()
            if not line:
                continue
            # Skip section braces or headers
            if line in ("{", "}"):
                continue

            m = self.TRACKNAME_RE.match(line)
            if m:
                val = m.group("val").strip()
                track.track_name = val
                track.gdb_info["TrackName"] = val
                continue

            m = self.VENUENAME_RE.match(line)
            if m:
                val = m.group("val").strip()
                track.venue_name = val
                track.gdb_info["VenueName"] = val
                continue

            m = self.LAYOUT_RE.match(line)
            if m:
                val = m.group("val").strip()
                track.layout = val
                track.gdb_info["Layout"] = val
                continue

            # Generic key=value capture
            if "=" in line:
                key, val = line.split("=", 1)
                key = key.strip()
                val = val.strip()
                # Trim surrounding quotes if present
                if len(val) >= 2 and ((val[0] == '"' and val[-1] == '"') or (val[0] == "'" and val[-1] == "'")):
                    val = val[1:-1]
                # Avoid empty keys
                if key:
                    track.gdb_info[key] = val

        # Set file metadata
        if file_path:
            p = Path(file_path)
            track.file_path = str(p)
            track.file_name = p.name
        return track

    def scan_directory(self, locations_dir: str | Path) -> list[Track]:
        """Scan recursively for .gdb files under locations_dir."""
        locations_dir = Path(locations_dir)
        tracks: list[Track] = []
        for gdb in locations_dir.glob("**/*.gdb"):
            tr = self.parse_file(gdb)
            if tr:
                # Set relative path w.r.t GameData/Locations
                try:
                    rel = gdb.relative_to(locations_dir)
                    tr.relative_path = str(rel).replace("\\", "/")
                except Exception:
                    tr.relative_path = tr.file_name
                tracks.append(tr)
        return tracks

    @staticmethod
    def search(tracks: Iterable[Track], query: str) -> list[Track]:
        q = query.lower()
        res = []
        for t in tracks:
            if (
                q in (t.track_name or "").lower()
                or q in (t.venue_name or "").lower()
                or q in (t.layout or "").lower()
                or q in (t.file_name or "").lower()
            ):
                res.append(t)
        return res
