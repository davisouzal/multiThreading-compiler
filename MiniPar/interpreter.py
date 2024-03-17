import threading
import socket
from time import sleep

SIZE = 1024
FORMAT = "utf-8"
ADDR = ("127.0.0.1", 5546)

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def tuple(self):
        return [self.type, self.value]

class SymbolTable:
    def __init__(self):
        self.symbols = {}

    def add_symbol(self, name, type_, value=None):
        self.symbols[name] = (value, type_)

    def get_value(self, name):
        return self.symbols.get(name, (None, None))[0]

    def get_type(self, name):
        return self.symbols.get(name, (None, None))[1]

    def set_value(self, name, value):
        current_type = self.get_type(name)
        self.symbols[name] = (value, current_type)

def receive(conection, response):
    conn, addr = conection.accept()
    msg = conn.recv(SIZE).decode(FORMAT)
    if response != None:
        conn.send(response.encode(FORMAT))
    return msg;
    
def send(conection, msg, waitForResp):
    msg = str(msg)
    conection.connect(ADDR)
    conection.send(msg.encode(FORMAT))
    if waitForResp:
        response = conection.recv(SIZE).decode(FORMAT)
        return response

def parseExpr(expr, symbol_table):
        
    if len(expr) == 0:
        return False
    
    if (symbol_table.get_type(expr[0].value) == 'server'):
        return receive(symbol_table.get_value(expr[0].value), None)
    elif (symbol_table.get_type(expr[0].value) == 'client'):
        return send(symbol_table.get_value(expr[0].value), "awaiting", True)
    expr_str = ''
    
    for token in expr:
        if token.type == 'IDENTIFIER':
            expr_str += str(symbol_table.get_value(token.value))
        elif token.type in ['INT','BOOL','PLUS','MINUS','MULTIPLY','DIVIDE','LESS','GREATER','GREATER_EQUAL','EQUAL_EQUAL','NOT_EQUAL','R_PAREN','L_PAREN','R_PAREN']:
            expr_str += str(token.value)
        else:
            return False
        
    return eval(expr_str)

def parseStr(expr, symbol_table):    
    expr_str = ''
    
    for token in expr:
        if token.type == 'IDENTIFIER':
            expr_str += str(symbol_table.get_value(token.value))
        else:
            expr_str += str(token.value)
        
    return expr_str

def intParser(tokens, symbol_table):
    if tokens[0].type != 'IDENTIFIER':
        return "Syntax Error"
    
    identifier_name = tokens[0].value
    symbol_table.add_symbol(identifier_name, 'int')
    
    if tokens[1].type == 'EQUALS':        
        expr = []
        i = 2
        if tokens[2].type == 'INPUT':
            symbol_table.set_value(identifier_name, input())
        else:
            while (tokens[i].type != 'SEMICOLON'):             
                expr.append(tokens[i])
                i += 1

            symbol_table.set_value(identifier_name, parseExpr(expr, symbol_table))
        
    elif tokens[1].type == 'SEMICOLON':
        return
    
    else:
        return "Syntax Error"


def indenParser(tokens, symbol_table):   
    identifier_name = tokens[0].value
    
    if tokens[1].type == 'EQUALS':        
        expr = []
        i = 2
        if tokens[2].type == 'INPUT':
            symbol_table.set_value(identifier_name, input())
        else:
            while (tokens[i].type != 'SEMICOLON'):             
                expr.append(tokens[i])
                i += 1
            
            if symbol_table.get_type(identifier_name) == 'str':
                symbol_table.set_value(identifier_name, parseStr(expr, symbol_table))
            else:
                symbol_table.set_value(identifier_name, parseExpr(expr, symbol_table))
        
    elif tokens[1].type == 'SEMICOLON':
        return
    
    else:
        return "Syntax Error"     

def strParser(tokens, symbol_table):
    if tokens[0].type != 'IDENTIFIER':
        return "Syntax Error"
    
    identifier_name = tokens[0].value
    symbol_table.add_symbol(identifier_name, 'str')
    
    if tokens[1].type == 'EQUALS':        
        expr = []
        i = 2
        if tokens[2].type == 'INPUT':
            symbol_table.set_value(identifier_name, input())
        else:
            while (tokens[i].type != 'SEMICOLON'):             
                expr.append(tokens[i])
                i += 1

            symbol_table.set_value(identifier_name, parseStr(expr, symbol_table))
        
    elif tokens[1].type == 'SEMICOLON':
        return
    
    else:
        return "Syntax Error"

def boolParser(tokens, symbol_table):
    if tokens[0].type != 'IDENTIFIER':
        return "Syntax Error"
    
    identifier_name = tokens[0].value
    symbol_table.add_symbol(identifier_name, 'bool')
    
    if tokens[1].type == 'EQUALS':        
        expr = []
        i = 2
        if tokens[2].type == 'INPUT':
            symbol_table.set_value(identifier_name, input())
        else:
            while (tokens[i].type != 'SEMICOLON'):             
                expr.append(tokens[i])
                i += 1

            symbol_table.set_value(identifier_name, parseExpr(expr, symbol_table))
        
    elif tokens[1].type == 'SEMICOLON':
        return
    
    else:
        return "Syntax Error"

def IF(block_tokens, symbol_table):
    interpreter = Interpreter(block_tokens, symbol_table)
    interpreter.interpret()

def whileParser(conditions, tokens, symbol_table):
    while(parseExpr(conditions, symbol_table)):
    
        interpreter = Interpreter(tokens, symbol_table)
        interpreter.interpret()
        
def block_stmts(block_tokens, symbol_table):        
    interpreter = Interpreter(block_tokens, symbol_table)
    interpreter.interpret()
    
def channel(channel_tokens, tokens, symbol_table):
    ADDR = (channel_tokens[2].value, int(channel_tokens[3].value))

    if channel_tokens[4].type == 'CLIENT':
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        symbol_table.add_symbol(channel_tokens[1].value, 'client', client)
        
        interpreter = Interpreter(tokens, symbol_table)
        interpreter.interpret()
        
        client.close()
            

    elif channel_tokens[4].type == 'SERVER':
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(ADDR)
        server.listen()  

        symbol_table.add_symbol(channel_tokens[1].value, 'server', server)
        
        connected = True
        while(connected): 
            interpreter = Interpreter(tokens, symbol_table)
            interpreter.interpret()
            

class Interpreter:
    def __init__(self, tokens, global_symbol_table=None):
        self.tokens = tokens
        self.symbol_table = SymbolTable()
        if global_symbol_table:
            self.symbol_table.symbols = global_symbol_table.symbols
        
    def interpret(self):
        
        i = 0;
        while True:
            token = self.tokens[i]
            
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
                        return('Syntax Error')
                    if(brace_count == 0):
                        i += 1
                        break
                    block_tokens.append(self.tokens[i])
                    i += 1

                block_tokens.append(Token('EOF', 'EOF'))

                block_stmts(block_tokens, self.symbol_table)
                
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
                        return('Syntax Error')
                    if(brace_count == 0):
                        i += 1
                        break
                    block_tokens.append(self.tokens[i])
                    i += 1

                block_tokens.append(Token('EOF', 'EOF'))
                
                thread = threading.Thread(target=lambda: block_stmts(block_tokens, self.symbol_table))
                thread.start()
                
            elif token.type == 'IDENTIFIER':
                line_tokens = [token]
                
                while self.tokens[i].type != 'SEMICOLON':
                    line_tokens.append(self.tokens[i])
                    i += 1
                    
                line_tokens.append(self.tokens[i])
                i += 1
                
                if(self.symbol_table.get_type(token.value) == 'client'):
                    conection = self.symbol_table.get_value(token.value)
                    message = ''
                    if line_tokens[2].type == 'IDENTIFIER':
                        message = str(self.symbol_table.get_value(line_tokens[2].value))
                    elif line_tokens[2].type in ['BOOL', 'INT', 'STRING']:
                        message = str(line_tokens[2].value)
                    else:
                        return('Syntax Error')  
                    send(conection, message, False)
                elif(self.symbol_table.get_type(token.value) == 'server'):
                    conection = self.symbol_table.get_value(token.value)
                    message = ''
                    if line_tokens[2].type == 'IDENTIFIER':
                        message = str(self.symbol_table.get_value(line_tokens[2].value))
                    elif line_tokens[2].type in ['BOOL', 'INT', 'STRING']:
                        message = str(line_tokens[2].value)
                    else:
                        return('Syntax Error')  
                    receive(conection, message)
                else:
                    indenParser(line_tokens, self.symbol_table)  
            
            elif token.type == 'INT':
                line_tokens = []
                while self.tokens[i].type != 'SEMICOLON':
                    line_tokens.append(self.tokens[i])
                    i += 1
                    
                line_tokens.append(self.tokens[i])
                i += 1
                
                intParser(line_tokens, self.symbol_table)
                    
            elif token.type == 'BOOL':
                line_tokens = []
                while self.tokens[i].type != 'SEMICOLON':
                    line_tokens.append(self.tokens[i])
                    i += 1
                    
                line_tokens.append(self.tokens[i])
                i += 1
                
                boolParser(line_tokens, self.symbol_table)
                      
            elif token.type == 'STRING':
                line_tokens = []
                while self.tokens[i].type != 'SEMICOLON':
                    line_tokens.append(self.tokens[i])
                    i += 1
                    
                line_tokens.append(self.tokens[i])
                i += 1
                
                strParser(line_tokens, self.symbol_table)
                
            elif token.type == 'PRINT':
                if self.tokens[i].type != 'L_PAREN':
                    return('Syntax Error')
                i += 1
                paren_count = 1
                expr_tokens = []
                while(True):
                    if self.tokens[i].type == 'L_PAREN':
                        paren_count += 1
                    elif self.tokens[i].type == 'R_PAREN':
                        paren_count -= 1
                    elif(self.tokens[i].type == 'EOF'):   
                        return('Syntax Error')
                    if(paren_count == 0):
                        i += 1
                        break
                    
                    expr_tokens.append(self.tokens[i])
                    
                    i += 1;
                i += 1;  
                
                
                if (len(expr_tokens) == 1) and (expr_tokens[0].type != 'IDENTIFIER'):
                    print(expr_tokens[0].value)
                elif (len(expr_tokens) == 1) and (expr_tokens[0].type == 'IDENTIFIER'):
                    print(self.symbol_table.get_value(expr_tokens[0].value))
                else:
                    print(parseExpr(expr_tokens, self.symbol_table))               
                    
            elif token.type == 'IF':
                if self.tokens[i].type != 'L_PAREN':
                    return('Syntax Error')
                i += 1
                paren_count = 1
                condition_tokens = []
                while(True):
                    if self.tokens[i].type == 'L_PAREN':
                        paren_count += 1
                    elif self.tokens[i].type == 'R_PAREN':
                        paren_count -= 1
                    elif(self.tokens[i].type == 'EOF'):   
                        return('Syntax Error')
                    if(paren_count == 0):
                        i += 1
                        break
                    
                    condition_tokens.append(self.tokens[i])
                    
                    i += 1;
                
                finalElse = False
                visited = False    
                while True:
                    
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
                            return('Syntax Error')
                        if(brace_count == 0):
                            i += 1
                            break
                        block_tokens.append(self.tokens[i])
                        i += 1
    
                    block_tokens.append(Token('EOF', 'EOF'))
                    
                    if not finalElse and not visited:
                        if parseExpr(condition_tokens, self.symbol_table):
                            IF(block_tokens, self.symbol_table)
                            visited = True
                    elif finalElse:
                        if not visited:
                            IF(block_tokens, self.symbol_table)
                            visited = True
                        break
                            
                    
                    if self.tokens[i].type == 'ELSE':
                        i += 1
                        if self.tokens[i].type == 'IF':
                            i += 1
                            if self.tokens[i].type != 'L_PAREN':
                                return('Syntax Error')
                            i += 1
                            
                            paren_count = 1
                            condition_tokens = []
                            
                            while(True):
                                if self.tokens[i].type == 'L_PAREN':
                                    paren_count += 1
                                elif self.tokens[i].type == 'R_PAREN':
                                    paren_count -= 1
                                elif(self.tokens[i].type == 'EOF'):   
                                    return('Syntax Error')
                                if(paren_count == 0):
                                    i += 1
                                    break
                                
                                condition_tokens.append(self.tokens[i])
                                
                                i += 1
                                    
                        else:
                            finalElse = True
                    else:
                        break   
                
            elif token.type == 'WHILE':
                if self.tokens[i].type != 'L_PAREN':
                    return('Syntax Error')
                i += 1
                paren_count = 1
                condition_tokens = []
                while(True):
                    if self.tokens[i].type == 'L_PAREN':
                        paren_count += 1
                    elif self.tokens[i].type == 'R_PAREN':
                        paren_count -= 1
                    elif(self.tokens[i].type == 'EOF'):   
                        return('Syntax Error')
                    if(paren_count == 0):
                        i += 1
                        break
                    
                    condition_tokens.append(self.tokens[i])
                    
                    i += 1;
                    
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
                        return('Syntax Error')
                    if(brace_count == 0):
                        i += 1
                        break
                    block_tokens.append(self.tokens[i])
                    i += 1

                block_tokens.append(Token('EOF', 'EOF'))
                
                whileParser(condition_tokens, block_tokens, self.symbol_table)
                
            elif token.type == 'C_CHANNEL':
                channel_tokens = []
                channel_tokens.append(token)
                while self.tokens[i].type != 'L_BRACE':
                    channel_tokens.append(self.tokens[i])
                    i += 1
                    
                brace_count = 1
                i += 1
                block_tokens = []
                while(True):
                    if self.tokens[i].type == 'L_BRACE':
                        brace_count += 1
                    elif self.tokens[i].type == 'R_BRACE':
                        brace_count -= 1
                    elif(self.tokens[i].type == 'EOF'):   
                        return('Syntax Error')
                    if(brace_count == 0):
                        i += 1
                        break
                    block_tokens.append(self.tokens[i])
                    i += 1

                block_tokens.append(Token('EOF', 'EOF'))
                
                channel(channel_tokens, block_tokens, self.symbol_table)
                
            elif token.type == 'EOF':
                break;
            else:
                return('Syntax Error')  
            
        return('Success')