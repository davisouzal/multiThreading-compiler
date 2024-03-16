import threading

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def tuple(self):
        return [self.type, self.value]

class SymbolTable:
    def __init__(self):
        self.symbols = {}

    def add_symbol(self, name, value=None):
        self.symbols[name] = value

    def get_value(self, name):
        return self.symbols.get(name)

    def set_value(self, name, value):
        self.symbols[name] = value

def arithExpr(expr, symbol_table):
    if len(expr) == 0:
        #TODO throw error
        return "Syntax Error"
    
    expr_str = ''
    
    for token in expr:
        if token.type == 'IDENTIFIER':
            expr_str += str(symbol_table.get_value(token.value))
        elif token.type == 'INT' or 'PLUS' or 'MINUS' or 'MULTIPLY' or 'DIVIDE' or 'L_PAREN' or 'R_PAREN':
            expr_str += str(token.value)
        else:
            #TODO throw error
            return "Syntax Error"
        
    return eval(expr_str)

def boolExpr(expr):
    pass

def intParser(tokens, symbol_table):
    if tokens[0].type != 'IDENTIFIER':
        #TODO throw error
        return "Syntax Error"
    
    identifier_name = tokens[0].value
    symbol_table.add_symbol(identifier_name)
    
    if tokens[1].type == 'EQUALS':
        expr = []
        i = 2
        while (tokens[i].type != 'SEMICOLON'):
            expr.append(tokens[i])
            i += 1
        
        symbol_table.set_value(identifier_name, arithExpr(expr, symbol_table))
        
        print(symbol_table.get_value(identifier_name))
        
    elif tokens[1].type == 'SEMICOLON':
        return
    
    else:
        #TODO throw error
        return "Syntax Error"
     

def STRING(tokens):
    pass

def BOOL(tokens):
    pass

def IF(condition, tokens):
    pass

def WHILE(condition, tokens):
    pass
        
def block_stmts(block_tokens):        
    interpreter = Interpreter(block_tokens)
    interpreter.interpret()

class Interpreter:
    def __init__(self, tokens):
        self.tokens = tokens
        self.symbol_table = SymbolTable()
        
    def interpret(self):
        
        i = 0;
        while True:
            
            token = self.tokens[i]
            print(token.type)
            
            i += 1
            if token.type == 'SEQ':                 
                if self.tokens[i].type != 'L_BRACE':
                    return('Syntax Error')
                i += 1
                brace_count = 1
                block_tokens = []
                while(True):
                    if self.tokens[i].type == 'L_BRACE':
                        brace_count += 1
                    elif self.tokens[i].type == 'R_BRACE':
                        brace_count -= 1
                    elif(self.tokens[i].type == 'EOF'):   
                        #TODO throw error
                        return('Syntax Error')
                    if(brace_count == 0):
                        i += 1
                        break
                    block_tokens.append(self.tokens[i])
                    i += 1

                block_tokens.append(Token('EOF', 'EOF'))

                block_stmts(block_tokens)
                
            elif token.type == 'PAR':
                if self.tokens[i].type != 'L_BRACE':
                    return('Syntax Error')
                i += 1
                brace_count = 1
                block_tokens = []
                while(True):
                    if self.tokens[i].type == 'L_BRACE':
                        brace_count += 1
                    elif self.tokens[i].type == 'R_BRACE':
                        brace_count -= 1
                    elif(self.tokens[i].type == 'EOF'):   
                        #TODO throw error
                        return('Syntax Error')
                    if(brace_count == 0):
                        i += 1
                        break
                    block_tokens.append(self.tokens[i])
                    i += 1

                block_tokens.append(Token('EOF', 'EOF'))
                
                thread = threading.Thread(target=lambda: block_stmts(block_tokens))
                thread.start()
            elif token.type == 'IDENTIFIER':
                pass    
            
            elif token.type == 'INT':
                line_tokens = []
                while self.tokens[i].type != 'SEMICOLON':
                    line_tokens.append(self.tokens[i])
                    i += 1
                    
                line_tokens.append(self.tokens[i])
                i += 1
                
                intParser(line_tokens, self.symbol_table)
                    
            elif token.type == 'BOOL':
                pass         
            elif token.type == 'STRING':
                pass
            elif token.type == 'IF':
                pass
            elif token.type == 'WHILE':
                pass
            elif token.type == 'EOF':
                break;
            else:
                #TODO throw error
                return('Syntax Error')  
            
        return('Success')