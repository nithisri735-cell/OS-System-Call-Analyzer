#include <stdio.h>

int main() {
    FILE *fp;

    fp = fopen("protected.txt", "r");

    if (fp == NULL) {
        perror("Permission error");
        return 1;
    }

    fclose(fp);

    return 0;
}