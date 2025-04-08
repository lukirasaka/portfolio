#include <stdio.h>

#define X 80
#define Y 20

typedef union {
    short x, y, delka;
    char znak, smer;
} Operand;

typedef struct {
    char kod;
    Operand o;
} Instr;

// Načtení externích souborů
#include "U09.inc" 
#include "U09T.inc" 

// Funkce pro kreslení
void Kresleni(char plocha[X][Y], const Instr instr[], int n) {
    short x = 0, y = 0;
    char znak = ' ';
    short delka = 0;

    for (int i = 0; i < n; ++i) {
        switch (instr[i].kod) {
            case 1: x = instr[i].o.x; break;
            case 2: y = instr[i].o.y; break;
            case 3: znak = instr[i].o.znak; break;
            case 4: delka = instr[i].o.delka; break;
            case 5:
                for (int d = 0; d < delka; ++d) {
                    if (x >= 0 && x < X && y >= 0 && y < Y) {
                        plocha[x][y] = znak;
                    }
                    if (instr[i].o.smer & 1) x++;
                    if (instr[i].o.smer & 2) x--;
                    if (instr[i].o.smer & 4) y++;
                    if (instr[i].o.smer & 8) y--;
                }
                break;
        }
    }
}

// Funkce pro zobrazení
void Zobrazeni(const char plocha[X][Y]) {
    for (int y = 0; y < Y; ++y) {
        for (int x = 0; x < X; ++x) {
            putchar(plocha[x][y]);
        }
        putchar('\n');
    }
}

int main() {
    T(); 
    return 0;
}
