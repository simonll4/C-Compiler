int sumaDiez(int a){

    int i;
    for ( i = 0; i < 10 ; i = i + 1 ){
        a = a + 1;
    }
    return a;
}

void main(){
    int x = 20;

    x = sumaDiez(x);
}