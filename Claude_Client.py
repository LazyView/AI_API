import requests
import json
import os
import time
from typing import List, Dict, Any, Optional
from Prompt_Template import PromptManager
from Response_Parser import ResponseParser
from secrets import API_KEY
class ClaudeClient:

    def __init__(self):
        self.prompt_manager = PromptManager()
        self.prompt_manager.register_default_templates()
        self.response_parser = ResponseParser()
        self.api_key = API_KEY
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

    def analyze_text(self, text, max_tokens=2000):
        """
        Provede strukturovanou analýzu textu.

        Args:
            text (str): Text k analýze
            max_tokens (int): Maximální počet tokenů v odpovědi

        Returns:
            dict: Strukturovaná analýza s klíči: summary, key_points, analysis, context, conclusions
        """
        response = self.send_templated_message(
            "structured_analysis",
            max_tokens=max_tokens,
            input_text=text
        )
        print("====SUROVA ODPOVED====")
        print(response)
        print("================")
        # Správné vytvoření instance parseru a předání textu
        parser = ResponseParser()
        structured_data = parser.parse_structured_analysis(response)  # Zde musí být předán response

        return structured_data

