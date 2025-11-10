#!/usr/bin/env python3
"""
ESENS Godot Wrapper
Simple wrapper for calling ESENS parser from Godot via OS.execute()

Usage from Godot:
    var output = []
    OS.execute("python3", ["res://python/esens_godot_wrapper.py", "P+H30%10s.ST"], output, true)
    var json = JSON.parse_string(output[0])

Returns JSON with effect data.
"""

import sys
import json
from ESENS_Parser import parse_esens_notation

def main():
    if len(sys.argv) < 2:
        result = {
            "error": "No ESENS notation provided",
            "usage": "python3 esens_godot_wrapper.py <notation>"
        }
        print(json.dumps(result))
        sys.exit(1)

    notation = sys.argv[1]

    try:
        # Parse the notation using existing ESENS parser
        parsed = parse_esens_notation(notation)

        # Convert to Godot-friendly format
        result = {
            "success": True,
            "notation": notation,
            "effects": parsed
        }

    except Exception as e:
        result = {
            "success": False,
            "error": str(e),
            "notation": notation
        }

    # Output as JSON
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
