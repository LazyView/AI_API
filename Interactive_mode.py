import secrets
from Coding_Partner import CodingPartner


def interactive_mode():
    """Interactive mode for the Coding Partner."""
    import os

    # Initialize the coding partner
    api_key = secrets.API_KEY

    partner = CodingPartner(api_key)

    print("=== Coding Partner Interactive Mode ===")
    print("Available commands:")
    print("  analyze: Analyze code quality and issues")
    print("  optimize: Optimize existing code")
    print("  generate: Generate code from requirements")
    print("  debug: Fix issues in problematic code")
    print("  translate: Translate code between languages")
    print("  exit: Exit interactive mode")
    print()

    while True:
        command = input("Command (or 'exit'): ").strip().lower()

        if command == "exit":
            break

        elif command == "analyze":
            language = input("Programming language: ")
            print("Enter the code to analyze (type 'END' on a new line when finished):")
            code = read_multiline_input()

            print("\nAnalyzing code...")
            result = partner.analyze_code(code, language)
            print("\n=== Analysis Result ===")
            print(result)

        elif command == "optimize":
            language = input("Programming language: ")
            print("Enter the code to optimize (type 'END' on a new line when finished):")
            code = read_multiline_input()

            print("\nOptimizing code...")
            optimized_code, explanation = partner.optimize_code(code, language)

            print("\n=== Optimization Explanation ===")
            print(explanation)
            print("\n=== Optimized Code ===")
            print(optimized_code)

            save = input("\nSave optimized code to file? (y/n): ")
            if save.lower() == 'y':
                filename = input("Enter filename: ")
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(optimized_code)
                print(f"Optimized code saved to {filename}")

        elif command == "generate":
            language = input("Target programming language: ")
            requirement = input("Describe what the code should do: ")
            print("Any additional specifications? (type 'END' on a new line when finished):")
            specifications = read_multiline_input()

            print("\nGenerating code...")
            generated_code = partner.generate_code(requirement, language, specifications)

            print("\n=== Generated Code ===")
            print(generated_code)

            save = input("\nSave generated code to file? (y/n): ")
            if save.lower() == 'y':
                filename = input("Enter filename: ")
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(generated_code)
                print(f"Generated code saved to {filename}")

        elif command == "debug":
            language = input("Programming language: ")
            problem = input("Describe the issue: ")
            print("Enter the problematic code (type 'END' on a new line when finished):")
            code = read_multiline_input()

            print("\nDebugging code...")
            fixed_code, explanation = partner.debug_code(code, problem, language)

            print("\n=== Debug Explanation ===")
            print(explanation)
            print("\n=== Fixed Code ===")
            print(fixed_code)

            save = input("\nSave fixed code to file? (y/n): ")
            if save.lower() == 'y':
                filename = input("Enter filename: ")
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(fixed_code)
                print(f"Fixed code saved to {filename}")

        elif command == "translate":
            source_language = input("Source programming language: ")
            target_language = input("Target programming language: ")
            print("Enter the code to translate (type 'END' on a new line when finished):")
            code = read_multiline_input()

            print("\nTranslating code...")
            translated_code = partner.translate_code(code, source_language, target_language)

            print("\n=== Translated Code ===")
            print(translated_code)

            save = input("\nSave translated code to file? (y/n): ")
            if save.lower() == 'y':
                filename = input("Enter filename: ")
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(translated_code)
                print(f"Translated code saved to {filename}")

        else:
            print("Unknown command. Please try again.")

        print()  # Add blank line between commands

def read_multiline_input():
    """Read multiple lines of input until 'END' is entered on a line by itself."""
    lines = []
    while True:
        line = input()
        if line == "END":
            break
        lines.append(line)
    return "\n".join(lines)

# Update main function to include interactive mode
def main():
    import argparse

    parser = argparse.ArgumentParser(description="AI-powered coding assistant")
    parser.add_argument("--interactive", "-i", action="store_true",
                        help="Start in interactive mode")
    # Add other arguments as before...

    args = parser.parse_args()

    if args.interactive:
        interactive_mode()
    else:
        # Original command-line mode...
        pass
