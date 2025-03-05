import argparse
from Claude_Client import ClaudeClient

def read_multiline_text():
    print("Zadejte text (ukončete řádkem obsahujícím pouze 'END'):")
    lines = []
    while True:
        try:
            line = input()
            if line == "END":
                break
            lines.append(line)
        except EOFError:
            break
    return '\n'.join(lines)

def main():
    sample_text = read_multiline_text()

    client = ClaudeClient()
    result = client.analyze_text(sample_text)
    # Výpis výsledků
    print("SOUHRN:")
    print(result["summary"])
    print("\nKLÍČOVÉ BODY:")
    for i, point in enumerate(result["key_points"], 1):
        print(f"{i}. {point}")
    print("\nZÁVĚRY:")
    print(result["conclusions"])

if __name__ == "__main__":
    main()


