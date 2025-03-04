import requests
import json
import os
import time
from typing import List, Dict, Any, Optional
from Prompt_Template import PromptManager
class ClaudeClient:
    def __init__(self, api_key: Optional[str] = None):
        self.prompt_manager = PromptManager()
        self.prompt_manager.register_default_templates()

        self.api_key = "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"
        self.api_url = "https://api.anthropic.com/v1/messages"
        self.headers = {
            "x-api-key": self.api_key,
            "content-type": "application/json",
            "anthropic-version": "2023-06-01"
        }
        self.model = "claude-3-7-sonnet-20250219"
        self.conversation_history: List[Dict[str, str]] = []


    def send_templated_message(self, template_name, max_tokens=1000, **variables):
        prompt = self.prompt_manager.get_prompt(template_name, **variables)
        return self.send_message(prompt, max_tokens)

    def register_custom_template(self, name, template_string):
        self.prompt_manager.register_template(name, template_string)



    def send_message(self, message: str, max_tokens: int = 1000) -> str:
        """Odešle zprávu na Claude API a vrátí odpověď."""
        # Přidáme novou zprávu do historie
        self.conversation_history.append({"role": "user", "content": message})

        # Připravíme data pro API požadavek
        data = {
            "model": self.model,
            "max_tokens": max_tokens,
            "messages": self.conversation_history
        }

        try:
            # Odeslání požadavku
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=data
            )

            # Kontrola, zda požadavek byl úspěšný
            response.raise_for_status()

            # Zpracování odpovědi
            result = response.json()

            # Extrakce textu odpovědi
            assistant_message = result["content"][0]["text"]

            # Přidání odpovědi do historie
            self.conversation_history.append({"role": "assistant", "content": assistant_message})

            return assistant_message

        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error: {e}")
            print(f"Response content: {response.text}")
            return f"Chyba při komunikaci s API: {e}"
        except requests.exceptions.ConnectionError:
            return "Chyba připojení k API serveru."
        except requests.exceptions.Timeout:
            return "Vypršel časový limit požadavku."
        except requests.exceptions.RequestException as e:
            return f"Obecná chyba požadavku: {e}"
        except KeyError as e:
            return f"Chyba při zpracování odpovědi (chybějící klíč {e})."
        except Exception as e:
            return f"Neočekávaná chyba: {e}"

    def clear_history(self) -> None:
        """Vymaže historii konverzace."""
        self.conversation_history = []

    def save_history(self, filename: str) -> None:
        """Uloží historii konverzace do souboru."""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.conversation_history, f, ensure_ascii=False, indent=2)

    def load_history(self, filename: str) -> None:
        """Načte historii konverzace ze souboru."""
        with open(filename, 'r', encoding='utf-8') as f:
            self.conversation_history = json.load(f)

# Příklad použití
if __name__ == "__main__":
    # Vytvoření instance klienta
    client = ClaudeClient("")

    # Poslání zprávy
    question = "Vysvětli, jak funguje rekurzivní funkce v programování. Uveď příklad v Pythonu."
    print(f"\nOtázka: {question}\n")

    # Měření času odpovědi
    start_time = time.time()
    response = client.send_message(question)
    end_time = time.time()

    print(f"Odpověď (za {end_time - start_time:.2f} sekund):\n{response}\n")

    # Pokračování konverzace
    follow_up = "Můžeš ukázat ještě jeden složitější příklad rekurze?"
    print(f"Doplňující otázka: {follow_up}\n")

    start_time = time.time()
    response = client.send_message(follow_up)
    end_time = time.time()

    print(f"Odpověď (za {end_time - start_time:.2f} sekund):\n{response}\n")

    # Uložení konverzace
    client.save_history("conversation.json")
    print("Konverzace byla uložena do souboru conversation.json")