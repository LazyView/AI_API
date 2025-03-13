from Claude_Client import ClaudeClient
from Few_Shot_Prompt_Builder import FewShotPromptBuilder
from Prompt_chaining_manager import ChainingManager



def main():
    # Příklad použití PromptChain
    client = ClaudeClient()
    # OptimizedClient = OptimizedApiClient(client, 100, 10)

    # Chain manager implementation
    """
    chain = ChainingManager(client)

    # Nastavení šablon pro jednotlivé kroky
    client.prompt_manager.register_template(
        "extract_keywords",
        "Extrahuj 5-7 klíčových slov nebo frází z textu:\n\n{text}"
    )

    client.prompt_manager.register_template(
        "summarize",
        "Shrň následující text na {max_words} slov.\nKlíčová slova: {keywords}\n\nText:\n{text}"
    )

    client.prompt_manager.register_template(
        "generate_title",
        "Vytvoř poutavý titulek pro tento text, který upoutá pozornost čtenáře:\n\n{summary}\n\nKlíčová slova: {keywords}"
    )
    chain.add_step(
        name="keywords",
        template_name="extract_keywords",
        input_mapping={"text": "Artificial intelligence (AI) is technology that enables computers and machines to simulate human learning, comprehension, problem solving, decision making, creativity and autonomy. Applications and devices equipped with AI can see and identify objects. They can understand and respond to human language. They can learn from new information and experience. They can make detailed recommendations to users and experts. They can act independently, replacing the need for human intelligence or intervention (a classic example being a self-driving car). But in 2024, most AI researchers and practitioners—and most AI-related headlines—are focused on breakthroughs in generative AI (gen AI), a technology that can create original text, images, video and other content. To fully understand generative AI, it’s important to first understand the technologies on which generative AI tools are built: machine learning (ML) and deep learning."}
    )

    chain.add_step(
        name="summary",
        template_name="summarize",
        input_mapping={
            "text": "Artificial intelligence (AI) is technology that enables computers and machines to simulate human learning, comprehension, problem solving, decision making, creativity and autonomy. Applications and devices equipped with AI can see and identify objects. They can understand and respond to human language. They can learn from new information and experience. They can make detailed recommendations to users and experts. They can act independently, replacing the need for human intelligence or intervention (a classic example being a self-driving car). But in 2024, most AI researchers and practitioners—and most AI-related headlines—are focused on breakthroughs in generative AI (gen AI), a technology that can create original text, images, video and other content. To fully understand generative AI, it’s important to first understand the technologies on which generative AI tools are built: machine learning (ML) and deep learning.",
            "max_words": 100,
            "keywords": "$keywords"  # Reference na výstup předchozího kroku
        }
    )

    # Nastavení řetězce

    chain.add_step(
        name="title",
        template_name="generate_title",
        input_mapping={
            "summary": "$summary",    # Reference na výstup kroku "summary"
            "keywords": "$keywords"   # Reference na výstup kroku "keywords"
        }
    )

    # Provedení řetězce
    results = chain.execute()

    print("Výsledky:")
    print(f"Klíčová slova: {results['keywords']}")
    print(f"Shrnutí: {results['summary']}")
    print(f"Titulek: {results['title']}")
    """


    # Příklad použití FewShotPromptBuilder
    fs_builder = FewShotPromptBuilder()

    # Přidání příkladů pro kategorii "překlad"
    fs_builder.add_example(
        category="překlad",
        example_input="Přelož do angličtiny: Dobrý den, jak se máte?",
        example_output="Good day, how are you?"
    )
    fs_builder.add_example(
        category="překlad",
        example_input="Přelož do angličtiny: Jsem programátor a učím se pracovat s AI.",
        example_output="I am a programmer and I am learning to work with AI."
    )

    # Přidání příkladů pro kategorii "vysvětlení"
    fs_builder.add_example(
        category="vysvětlení",
        example_input="Vysvětli pojem 'strojové učení' jednoduše, jako bys to vysvětloval/a dítěti.",
        example_output="Strojové učení je, když počítače umí samy zjistit, jak řešit úkoly, podobně jako ty, když se učíš něco nového. Místo toho, aby jim někdo řekl, co mají přesně dělat, sbírají zkušenosti a samy se rozhodují. Trochu jako když se učíš jezdit na kole - čím víc jezdíš, tím lépe ti to jde."
    )

    # Vytvoření few-shot promptu
    query = "Vysvětli: Černé díry."
    prompt = fs_builder.build_prompt(
        query=query,
        category="vysvětlení",
        num_examples=2,
        instruction="Jsi expertní na vesmír, specialozovaný na černé díry. Vysvětli pojem černá díra."
    )

    response = client.send_message(prompt)
    print(f"Odpověď: {response}")
if __name__ == "__main__":
    main()