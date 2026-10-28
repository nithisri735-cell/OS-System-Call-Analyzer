#include <stdio.h>
int main(){
    FILE *fp;
    fp= fopen("sample.txt","w");
    if(fp==NULL){
        perror("Error opening file");
        return 1;
    }
    fprintf(fp, "Hello from OS System Call Analyzer!\n");
    fclose(fp);
    return 0;
}