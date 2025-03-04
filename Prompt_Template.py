"""Modul pro správu a generování dynamických promptů pro Claude API."""
class PromptTemplate:
    """Třída reprezentující šablonu promptu s možností formátování."""
    def __init__(self, template_string):
        """
       Inicializuje novou šablonu promptu.

       Args:
           template_string (str): String šablony s placeholdery pro formátování.
       """
        self.template = template_string

    def format(self, **kwargs):
        """
        Vyplní šablonu dodanými proměnnými.

        Args:
            **kwargs: Klíčové argumenty odpovídající placeholderům v šabloně.

        Returns:
            str: Formátovaný prompt.

        Raises:
            ValueError: Pokud chybí některá požadovaná proměnná.
        """
        try:
            return self.template.format(**kwargs)
        except KeyError as e:
            raise ValueError(f"Variable the template is missing.")


class PromptManager:
    """Správce šablon promptů."""
    def __init__(self):
        self.templates = {}

    def register_template(self, name, template_string):
        self.templates[name] = PromptTemplate(template_string)

    def register_default_templates(self):
        for name, template in DEFAULT_TEMPLATES.items():
            self.register_template(name, template)

    def list_templates(self):
        return list(self.templates.keys())

    def get_template(self, template_name):
        if template_name not in self.templates:
            raise ValueError(f"Template {template_name} is not existing.")
        return self.templates[template_name]

    def get_prompt(self, template_name, **variables):
        if template_name not in self.templates:
            raise ValueError(f"Template {template_name} is not existing.")

        return self.templates[template_name].format(**variables)

    def create_composite_prompt(self, main_template_name, section=None, **variables):
        if section is None:
            section = {}

        formatted_section = {}
        for section_name, section_vars in section.items():
            if section_name in self.templates:
                formatted_section[section_name] = self.get_prompt(section_name, **section_vars)
            else:
                formatted_section[section_name] = ""
        all_vars = {**variables, **formatted_section}

        return self.get_prompt(main_template_name, **all_vars)

DEFAULT_TEMPLATES = {
    "summarize":
        """
        Shrň následující text na {max_words} slov. 
        Zaměř se na {focus_aspect} a style psaní ať je {tone}.
        
        Text k shrnutí:
        {input_text}
        """,
    "code_analysis":
        """
        Analyzuj následující {language} kód a poskytni zpětnou vazbu.
        {include_performance_tips}
        {include_security_tips}
        
        ```{language}
        {code}""",
    "question_answer":
        """
        Jsi expert na téma {topic}. Odpověz na následující otázku
        v {detail_level} detailu a s {tone} tónem.
        Otázka: {question}
        Dodatečný kontext:
        {context}
        """
}