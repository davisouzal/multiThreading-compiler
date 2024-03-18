print("Digite o numero do da sequencia de fibonacci que quer achar:");
int x = input;

print("Digite o numero para calcular o fatorial:")
int y = input;

par{
    int a = 1;
    int b = 1;
    print("Valor fibonacci: 1");
    print("Valor fibonacci: 1");
    int i = 2;
    int j = x;
    while(i < j) {
        c = a + b;
        string imp = "Valor fibonacci: " c;
        print(imp);
        a = b;
        b = c;
        i = i + 1;
    }
}

par{
    l = y;
    while(l > 1){
        l = l - 1;
        y = y * l;
        string imp = "Valor fatorial: " y;
        print(imp);
    }
}
