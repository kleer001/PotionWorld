#!/usr/bin/env python3
"""
Command-line interface for the ESENS (Enhanced Status Effect Notation System) Parser.
"""

import argparse
import json
import sys
from esens_parser import parse_esens, validate_esens, ESENSParseError

def main():
    parser = argparse.ArgumentParser(
        description="Parse and validate Enhanced Status Effect Notation System (ESENS) strings"
    )
    
    # Main arguments
    parser.add_argument("notation", nargs="?", help="The ESENS notation to parse")
    
    # Options
    parser.add_argument("--file", "-f", help="File containing ESENS notations, one per line")
    parser.add_argument("--validate", "-v", action="store_true", 
                        help="Only validate syntax, don't show parsed results")
    parser.add_argument("--no-explain", action="store_true", 
                        help="Disable human-readable explanations")
    parser.add_argument("--json", "-j", action="store_true", 
                        help="Output in JSON format")
    parser.add_argument("--interactive", "-i", action="store_true", 
                        help="Run in interactive mode")
    
    args = parser.parse_args()
    
    # Interactive mode
    if args.interactive:
        run_interactive_mode(args.no_explain, args.json)
        return
    
    # File input mode
    if args.file:
        try:
            with open(args.file, 'r') as f:
                notations = [line.strip() for line in f if line.strip()]
        except IOError as e:
            print(f"Error reading file: {e}", file=sys.stderr)
            return 1
    # Direct input mode
    elif args.notation:
        notations = [args.notation]
    else:
        parser.print_help()
        return 1
    
    # Process each notation
    for notation in notations:
        process_notation(notation, args.validate, not args.no_explain, args.json)
    
    return 0

def process_notation(notation, validate_only, explain, output_json):
    """Process a single ESENS notation"""
    try:
        if validate_only:
            validate_esens(notation)
            if output_json:
                print(json.dumps({"status": "valid", "notation": notation}))
            else:
                print(f"✓ {notation} is valid")
        else:
            result = parse_esens(notation, explain)
            
            if output_json:
                # Convert the object to dict for JSON output
                print(json.dumps({
                    "status": "valid",
                    "notation": notation,
                    "parsed": result["dict"],
                    "explanation": result.get("explanation")
                }, indent=2))
            else:
                print(f"\n=== {notation} ===")
                if "explanation" in result:
                    print(f"Explanation: {result['explanation']}")
                print("Parsed structure:")
                print(json.dumps(result["dict"], indent=2))
    
    except ESENSParseError as e:
        if output_json:
            print(json.dumps({
                "status": "error",
                "notation": notation,
                "error": str(e)
            }))
        else:
            print(f"\nError parsing {notation}:")
            print(e)

def run_interactive_mode(no_explain, output_json):
    """Run in interactive mode, parsing notations entered by the user"""
    print("=== ESENS Interactive Parser ===")
    print("Enter ESENS notations to parse, or 'exit' to quit.")
    print("Examples: P+S10%3T, E-D15C, P#Stun1T.RD")
    print()
    
    while True:
        try:
            notation = input("> ")
            if notation.lower() in ('exit', 'quit', 'q'):
                break
            
            if notation:
                process_notation(notation, False, not no_explain, output_json)
        
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")

if __name__ == "__main__":
    sys.exit(main())
