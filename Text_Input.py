def read_multiline_text():
    print("Zadejte text (ukončete řádkem obsahujícím pouze 'END'):")
    lines = []
    while True:
        try:
            line = input()
            if line == "END":
                break
            lines.append(line)
        except EOFError:
            break
    return '\n'.join(lines)