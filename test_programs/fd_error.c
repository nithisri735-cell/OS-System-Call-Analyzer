#include <unistd.h>
#include <stdio.h>

int main() {
    char buffer[20];

    int result = read(999, buffer, sizeof(buffer));

    if (result == -1) {
        perror("File descriptor error");
        return 1;
    }

    return 0;
}