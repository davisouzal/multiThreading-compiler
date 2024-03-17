int x = 20;
int y = 20;

par{
    int a = 1;
    int b = 1;
    print(a);
    print(b);
    int i = 1;
    int j = x;
    while(i < j) {
        c = a + b;
        print(c);
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
        print(y);
    }
}
