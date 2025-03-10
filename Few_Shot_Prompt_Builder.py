class FewShotPromptBuilder:
    """Třída pro tvorbu few-shot promptů s příklady."""

    def __init__(self):
        """Inicializuje builder s prázdnou kolekcí příkladů."""
        self.examples = {}  # kategorie -> [příklady]

    def add_example(self, category, example_input, example_output):
        """
        Přidá nový příklad do dané kategorie.

        Args:
            category (str): Kategorie příkladu
            example_input (str): Vstup příkladu
            example_output (str): Očekávaný výstup příkladu
        """
        if category not in self.examples:
            self.examples[category] = []

        self.examples[category].append({
            "input": example_input,
            "output": example_output
        })

    def build_prompt(self, query, category=None, num_examples=3, instruction=None):
        """
        Vytvoří few-shot prompt s příklady a dotazem.

        Args:
            query (str): Aktuální dotaz
            category (str, optional): Kategorie příkladů k použití
            num_examples (int): Počet příkladů k zahrnutí
            instruction (str, optional): Dodatečné instrukce

        Returns:
            str: Sestavený few-shot prompt
        """
        prompt_parts = []

        # Přidání instrukcí pokud jsou
        if instruction:
            prompt_parts.append(instruction)
            prompt_parts.append("")  # Prázdný řádek pro oddělení

        # Vybrání příkladů
        selected_examples = []
        if category and category in self.examples:
            # Výběr příkladů z dané kategorie
            selected_examples = self.examples[category][:num_examples]
        elif not category:
            # Výběr příkladů ze všech kategorií
            all_examples = []
            for cat_examples in self.examples.values():
                all_examples.extend(cat_examples)

            # Jednoduchý výběr prvních N příkladů (v reálném nasazení by zde byl sofistikovanější algoritmus)
            selected_examples = all_examples[:num_examples]

        # Přidání příkladů do promptu
        for i, example in enumerate(selected_examples):
            prompt_parts.append(f"Příklad {i+1}:")
            prompt_parts.append(f"Otázka: {example['input']}")
            prompt_parts.append(f"Odpověď: {example['output']}")
            prompt_parts.append("")  # Prázdný řádek pro oddělení

        # Přidání aktuálního dotazu
        prompt_parts.append("Nyní odpověz na tento dotaz:")
        prompt_parts.append(f"Otázka: {query}")
        prompt_parts.append("Odpověď:")

        # Složení promptu
        return "\n".join(prompt_parts)