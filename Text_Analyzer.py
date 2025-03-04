import argparse
from Claude_Client import ClaudeClient

def main():
    parser = argparse.ArgumentParser(description="Analyzuje a sumarizuje textové soubory pomocí Claude API")
    parser.add_argument("file", help="Cesta k textovému souboru pro analýzu")
    parser.add_argument("--template", default="summarize", help="summarize")
    parser.add_argument("--words", type=int, default=100, help="Maximální počet slov v souhrnu")
    parser.add_argument("--focus", default="hlavní myšlenky", help="Na co se zaměřit v souhrnu")
    parser.add_argument("--tone", default="formální", help="Tón souhrnu")
    args = parser.parse_args()

    # Načtení obsahu souboru
    try:
        with open(args.file, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Chyba při čtení souboru: {e}")
        return

    # Inicializace klienta
    client = ClaudeClient()

    # Odeslání požadavku
    print(f"Zpracovávám soubor {args.file} pomocí šablony {args.template}...")

    try:
        response = client.send_templated_message(
            args.template,
            max_tokens=1500,
            max_words=args.words,
            focus_aspect=args.focus,
            tone=args.tone,
            input_text=content
        )

        print("\n--- Výsledek analýzy ---")
        print(response)
        print("------------------------")

    except Exception as e:
        print(f"Chyba při komunikaci s API: {e}")

if __name__ == "__main__":
    main()