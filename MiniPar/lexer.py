class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return f"Token({self.type}, {self.value})"
    
class Lexer:
    def __init__(self):
        # Define token types
        self.token_types = {
            '+': 'PLUS',
            '-': 'MINUS',
            '*': 'MULTIPLY',
            '/': 'DIVIDE',
            ';': 'SEMICOLON',
            '(': 'L_PAREN',
            ')': 'R_PAREN',
            '{': 'L_BRACE',
            '}': 'R_BRACE',
            '=': 'EQUALS',
            '>=': 'GREATER_EQUAL',
            '==': 'EQUAL_EQUAL',   # Treat '==' as a single token
            '<=': 'LESS_EQUAL',
            '!=': 'NOT_EQUAL',
            '>': 'GREATER',
            '<': 'LESS',
            'true': 'BOOL_TRUE',
            'false': 'BOOL_FALSE',
            'int': 'INT_TYPE',
            'bool': 'BOOL_TYPE',
            'string': 'STRING_TYPE',
            'par': 'PAR',
            'seq': 'SEQ',
            'if': 'IF',
            'else': 'ELSE',
            'while': 'WHILE'
        }

    def tokenize(self, source_code):
        tokens = []
        current_number = ''
        current_string = ''
        current_word = ''

        inside_string = False

        i = 0
        while i < len(source_code):
            char = source_code[i]

            if char == '"':
                if not inside_string:
                    inside_string = True
                else:
                    tokens.append(Token('STRING', current_string))
                    current_string = ''
                    inside_string = False
            elif inside_string:
                current_string += char
            elif char.isdigit():
                current_number += char
            elif char.isalpha():
                current_word += char
            elif char in self.token_types:
                if current_number:
                    tokens.append(Token('INT', int(current_number)))
                    current_number = ''
                elif current_word:
                    if current_word in self.token_types:
                        tokens.append(Token(self.token_types[current_word], current_word))
                    elif current_word == 'true':
                        tokens.append(Token('BOOL', True))
                    elif current_word == 'false':
                        tokens.append(Token('BOOL', False))
                    else:
                        tokens.append(Token('IDENTIFIER', current_word))
                    current_word = ''
                # Check if the next character forms a combined token
                if i < len(source_code) - 1 and source_code[i:i+2] in self.token_types:
                    tokens.append(Token(self.token_types[source_code[i:i+2]], source_code[i:i+2]))
                    i += 1  # Move to the next character
                else:
                    tokens.append(Token(self.token_types[char], char))
            elif char.isspace():
                if current_number:
                    tokens.append(Token('INT', int(current_number)))
                    current_number = ''
                elif current_word:
                    if current_word in self.token_types:
                        tokens.append(Token(self.token_types[current_word], current_word))
                    elif current_word == 'true':
                        tokens.append(Token('BOOL', True))
                    elif current_word == 'false':
                        tokens.append(Token('BOOL', False))
                    else:
                        tokens.append(Token('IDENTIFIER', current_word))
                    current_word = ''
            else:
                raise Exception(f"Invalid character: {char}")

            i += 1

        if current_number:
            tokens.append(Token('INT', int(current_number)))
        elif current_word:
            if current_word in self.token_types:
                tokens.append(Token(self.token_types[current_word], current_word))
            elif current_word == 'true':
                tokens.append(Token('BOOL', True))
            elif current_word == 'false':
                tokens.append(Token('BOOL', False))
            else:
                tokens.append(Token('IDENTIFIER', current_word))
        elif current_string:
            tokens.append(Token('STRING', current_string))

        return tokens
