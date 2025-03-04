# response_parser.py
"""
Modul pro parsování a extrakci dat z odpovědí Claude API.
"""
import re
import json

def extract_numbers(text):
    """
    Extrahuje všechna čísla z textu.

    Args:
        text (str): Text k analýze

    Returns:
        list: Seznam nalezených čísel (float)
    """
    # TODO: Implementujte funkci pro extrakci čísel pomocí regulárních výrazů
    # Tip: Použijte re.findall s patřičným vzorem pro čísla
    # Nezapomeňte ošetřit různé formáty čísel (celá, desetinná, se zápornými hodnotami)
    numbers = re.findall("\d", text)
    return numbers

def extract_section(text, section_title):
    """
    Extrahuje sekci textu označenou nadpisem.

    Args:
        text (str): Text k analýze
        section_title (str): Název sekce k vyhledání

    Returns:
        str: Obsah sekce nebo None, pokud sekce nebyla nalezena
    """
    # TODO: Implementujte funkci pro vyhledání sekce podle nadpisu
    # Tip: Sekce obvykle začíná nadpisem a končí dalším nadpisem nebo koncem textu
    # Použijte regulární výrazy nebo jiné metody pro nalezení začátku a konce sekce

def extract_key_points(text, max_points=5):
    """
    Extrahuje klíčové body z textu.

    Args:
        text (str): Text k analýze
        max_points (int): Maximální počet bodů k extrakci

    Returns:
        list: Seznam klíčových bodů
    """
    # TODO: Implementujte funkci pro extrakci klíčových bodů
    # Tip: Hledejte odrážky, číslované seznamy nebo věty začínající frázemi jako
    # "Klíčové je", "Důležité", "Za prvé", atd.