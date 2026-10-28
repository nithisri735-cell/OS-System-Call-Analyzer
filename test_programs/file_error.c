#include <stdio.h>

int main() {
    FILE *fp;

    fp = fopen("does_not_exist.txt", "r");

    if (fp == NULL) {
        perror("File error");
        return 1;
    }

    fclose(fp);

    return 0;
}