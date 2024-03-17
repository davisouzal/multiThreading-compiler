chan calc "127.0.0.1" "5546" server {
    int op = calc receive;
    int a = calc receive;
    int b = calc receive;

    if (op == 1) {
        int x = a + b;
        calc receive x;
    } else if (op == 2) {
        int x = a - b;
        calc receive x;
    } else if (op == 3) {
        int x = a * b;
        calc receive x;
    } else if (op == 4) {
        int x = a / b;
        calc receive x;
    } else {
        string error = "Operacao invalida";
        calc receive error;
    }
    print(x);
    print("calculo realizado com sucesso!");
}