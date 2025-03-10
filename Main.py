from Claude_Client import ClaudeClient
from Prompt_chaining_manager import ChainingManager
from Optimized_Claude_Client import OptimizedApiClient



def main():
    # Příklad použití PromptChain
    client = ClaudeClient()
    # OptimizedClient = OptimizedApiClient(client, 100, 10)
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

if __name__ == "__main__":
    main()