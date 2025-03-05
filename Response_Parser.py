# response_parser.py
"""
Modul pro parsování a extrakci dat z odpovědí Claude API.
"""
import re
import json


class ResponseParser:
    def extract_numbers(self, text):
        """
        Extrahuje všechna čísla z textu.

        Args:
            text (str): Text k analýze

        Returns:
            list: Seznam nalezených čísel (float)
        """
        numbers = re.findall(r"[-+]?\d+(?:\.\d+)?", text)
        return numbers


    def extract_section(self, text, section_title):
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
        # Připraví regulární výraz pro hledání sekce
        # Hledá buď nadpis s # nebo nadpis ve formě "Nadpis:"
        section_pattern = re.escape(section_title)
        pattern = fr"(?:^|\n)(?:# {section_pattern}|{section_pattern}:)\s*\n(.*?)(?:\n(?:# |\w+:)|$)"

        # Najde všechny shody v textu (s příznakem re.DOTALL, který umožňuje . odpovídat i znakům nového řádku)
        matches = re.search(pattern, text, re.DOTALL | re.MULTILINE)

        if matches:
            return matches.group(1).strip()

        # Zkusíme jednodušší vzor bez speciálního formátování nadpisu
        pattern = fr"(?:^|\n){section_pattern}[:\s]*\n(.*?)(?:\n\w+[:\s]*\n|$)"
        matches = re.search(pattern, text, re.DOTALL | re.MULTILINE)

        if matches:
            return matches.group(1).strip()

        return None

    def extract_key_points(self, text, max_points=5):
        """
        Extrahuje klíčové body z textu.

        Args:
            text (str): Text k analýze
            max_points (int): Maximální počet bodů k extrakci

        Returns:
            list: Seznam klíčových bodů
        """
        key_points = []

        # Hledáme odrážky a číslované seznamy
        bullet_pattern = r"(?:^|\n)[\*\-•]\s+(.*?)(?=\n[\*\-•]|\n\n|$)"
        numbered_pattern = r"(?:^|\n)\d+\.\s+(.*?)(?=\n\d+\.|\n\n|$)"

        # Hledáme věty s klíčovými frázemi
        key_phrases = [
            "klíčové je", "důležité je", "hlavní bod", "zásadní je",
            "za prvé", "za druhé", "za třetí", "za čtvrté", "za páté",
            "především", "nejdůležitější", "podstatné je", "klíčovým faktorem",
            "v neposlední řadě", "závěrem", "shrnuto"
        ]

        phrase_patterns = []
        for phrase in key_phrases:
            # Sestavíme vzor pro každou frázi (ignorujeme velikost písmen)
            phrase_pattern = fr"(?:^|\n)(?:[^.!?\n]*?{re.escape(phrase)}[^.!?\n]*?[.!?])"
            phrase_patterns.append(phrase_pattern)

        # Spojíme všechny fráze do jednoho vzoru
        phrase_combined = "|".join(phrase_patterns)

        # Najdeme všechny shody pro každý vzor
        bullet_matches = re.findall(bullet_pattern, text, re.IGNORECASE | re.MULTILINE)
        numbered_matches = re.findall(numbered_pattern, text, re.IGNORECASE | re.MULTILINE)
        phrase_matches = re.findall(phrase_combined, text, re.IGNORECASE | re.MULTILINE)

        # Sloučíme výsledky, očistíme a omezíme počet
        for match in bullet_matches + numbered_matches:
            clean_point = match.strip()
            if clean_point and clean_point not in key_points:
                key_points.append(clean_point)
                if len(key_points) >= max_points:
                    return key_points

        for match in phrase_matches:
            clean_point = match.strip()
            if clean_point and clean_point not in key_points:
                key_points.append(clean_point)
                if len(key_points) >= max_points:
                    return key_points

        # Pokud je málo výsledků, můžeme hledat obecnější věty (např. ty začínající velkým písmenem)
        if len(key_points) < max_points and len(text) > 0:
            sentence_pattern = r"(?:^|\n)([A-Z][^.!?\n]{15,}[.!?])"
            sentence_matches = re.findall(sentence_pattern, text)

            for match in sentence_matches:
                clean_point = match.strip()
                if clean_point and clean_point not in key_points:
                    key_points.append(clean_point)
                    if len(key_points) >= max_points:
                        break

        return key_points

    def parse_structured_analysis(self, text):
        """
        Parsuje odpověď ve formátu strukturované analýzy.

        Args:
            text (str): Odpověď od Claude API

        Returns:
            dict: Parsovaná struktura s klíči: summary, key_points, analysis, context, conclusions
        """
        sections = ["SOUHRN", "KLÍČOVÉ BODY", "ANALÝZA", "KONTEXT", "ZÁVĚRY"]
        result = {}
        for section in sections:
            content = self.extract_section(text, section)
            # Převedeme názvy sekcí na anglické klíče pro konzistenci
            if section == "SOUHRN":
                result["summary"] = content
            elif section == "KLÍČOVÉ BODY":
                # Pro klíčové body extrahujeme seznam odrážek
                if content:
                    bullet_points = re.findall(r"(?:[\*\-•]\s+|\d+\.\s+)(.*?)(?=\n(?:[\*\-•]|\d+\.)\s+|\n\n|$)", content, re.DOTALL)
                    if not bullet_points:
                        # Zkusíme alternativní formát odrážek
                        bullet_points = re.findall(r"[\*\-]\s+(.*?)(?=\n[\*\-]|\n\n|$)", content, re.DOTALL)
                    result["key_points"] = [point.strip() for point in bullet_points] if bullet_points else []
                else:
                    result["key_points"] = []
            elif section == "ANALÝZA":
                result["analysis"] = content
            elif section == "KONTEXT":
                result["context"] = content
            elif section == "ZÁVĚRY":
                result["conclusions"] = content
        return result