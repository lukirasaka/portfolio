#include <stdio.h>

#define CELL_WIDTH 9
#define NUM_COLUMNS 16

void print_border(FILE *file) {
    int border_width = NUM_COLUMNS * CELL_WIDTH - 39; 
    for (int i = 0; i < border_width; i++) {
        fprintf(file, "-");
    }
    fprintf(file, "\n");
}

void save_ascii_table(const char *filename) {
    FILE *file = fopen(filename, "w");
    if (file == NULL) {
        printf("Nelze otevřít soubor pro zápis!\n");
        return;
    }

    print_border(file); 

    for (int i = 2; i <= 7; i++) {
        for (int j = 0; j < 8; j++) {
            int asciiValue = i * 16 + j;
            if (asciiValue == 127) {
                fprintf(file, "|%*s", CELL_WIDTH, "");
            } else {
                fprintf(file, "|%4d %3X %2c ", asciiValue, asciiValue, (char)asciiValue);
            }
        }
        fprintf(file, "|\n"); 
        for (int j = 8; j < 16; j++) {
            int asciiValue = i * 16 + j;
            if (asciiValue == 127) {
                fprintf(file, "| 127  7F    "); 
            } else {
                fprintf(file, "|%4d %3X %2c ", asciiValue, asciiValue, (char)asciiValue);
            }
        }
        fprintf(file, "|\n"); 
    }

    print_border(file); 

    fclose(file);
}

void print_ascii_table_from_file(const char *filename) {
    FILE *file = fopen(filename, "r");
    if (file == NULL) {
        printf("Nelze otevřít soubor pro čtení!\n");
        return;
    }

    char line[256];
    while (fgets(line, sizeof(line), file)) {
        printf("%s", line);
    }

    fclose(file);
}

int main() {
    const char *filename = "ascii_table.txt";

    save_ascii_table(filename);
    print_ascii_table_from_file(filename);

    return 0;
}