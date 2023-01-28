#include <fcntl.h>
#include <stdio.h>

int main()
{
    FILE *fp;
    fp = fopen("./test", "r");
    fclose(fp);

    return 0;
}