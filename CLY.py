import secrets
from Coding_Partner import CodingPartner
from Interactive_mode import interactive_mode


def main():
    """Command-line interface for the Coding Partner."""
    import argparse
    parser = argparse.ArgumentParser(description="AI-powered coding assistant")

    # Add interactive mode as a separate argument group
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--interactive", "-i", action="store_true",
                       help="Start in interactive mode")
    group.add_argument("action", choices=["analyze", "optimize", "generate", "debug", "translate"],
                       nargs="?", help="Action to perform")

    # Other arguments
    parser.add_argument("--file", help="Path to the code file")
    parser.add_argument("--language", help="Programming language")
    parser.add_argument("--target-language", help="Target language for translation")
    parser.add_argument("--requirement", help="Code requirement for generation")
    parser.add_argument("--problem", help="Problem description for debugging")
    parser.add_argument("--output", help="Output file path")

    args = parser.parse_args()

    # Interactive mode
    if args.interactive:
        interactive_mode()
        return

    # Command-line mode
    # Initialize the coding partner
    api_key = secrets.API_KEY

    partner = CodingPartner(api_key)

    # Rest of your code for handling different actions...
if __name__ == '__main__':
    main()