print("Digite o numero que representa o operador (1 para +, 2 para -, 3para * ou 4 para /):")
int op = input;
print("Digite um numero:")
int a = input;
print("Digite um numero:")
int b = input;

chan teste "127.0.0.1" "5546" client {
    teste send op;
}

chan teste "127.0.0.1" "5546" client {
    teste send a;
}

chan teste "127.0.0.1" "5546" client {
    teste send b;
}

chan teste "127.0.0.1" "5546" client {
    int x = teste send;
    print("resultado");
    print(x);
}