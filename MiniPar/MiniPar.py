if __name__ == "__main__":
    import sys
    from lexer import Lexer
    from interpreter import Interpreter

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
    try:
        lexer = Lexer()
        tokens = lexer.tokenize(source_code)
    except Exception as e:
        print("Lexer error:", e)
        tokens = []

    try:
        interpreter = Interpreter(tokens)
    except Exception as e:
        print("Interpreter initialization error:", e)
        interpreter = None

    if interpreter:
        try:
            result = interpreter.interpret()
        except Exception as e:
            print("Interpreter error:", e)