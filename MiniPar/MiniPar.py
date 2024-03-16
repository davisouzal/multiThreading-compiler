if __name__ == "__main__":
    import sys
    from lexer import Lexer

    if len(sys.argv) != 2:
        print("Usage: python MiniPar.py example.mp")
        sys.exit(1)
    
    file_name = sys.argv[1]
    
    # Create an instance of the lexer
    lexer = Lexer()

    # Read the contents of the file
    with open(file_name, 'r') as file:
        source_code = file.read()

    # Tokenize the source code
    tokens = lexer.tokenize(source_code)
    
    # Print the tokens (for demonstration purposes)
    for token in tokens:
        print(token)
