#include <fcntl.h>
#include <stdio.h>

int main()
{
    FILE *fp;
    char buf[0x10] = "TEST!!";

    fp = fopen("./test_write", "r");
    fread(buf, 0x1, 0x10, fp);
    fclose(fp);

    return 0;
}