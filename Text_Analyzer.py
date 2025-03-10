
def analyze_text(client, responseParser, text, max_tokens=2000):
    """
    Provede strukturovanou analýzu textu.

    Args:
        text (str): Text k analýze
        max_tokens (int): Maximální počet tokenů v odpovědi

    Returns:
        dict: Strukturovaná analýza s klíči: summary, key_points, analysis, context, conclusions
    """
    response = client.send_templated_message(
        "structured_analysis",
        max_tokens=max_tokens,
        input_text=text
    )
    print("====SUROVA ODPOVED====")
    print(response)
    print("================")
    # Správné vytvoření instance parseru a předání textu
    structured_data = responseParser.parse_structured_analysis(response)  # Zde musí být předán response

    return structured_data


