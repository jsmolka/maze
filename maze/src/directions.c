#include "directions.h"

#include <stdlib.h>

int g_width;

void init(int width)
{
    g_width = width;
}

int n1(int idx) {return idx - g_width;}
int s1(int idx) {return idx + g_width;}
int e1(int idx) {return idx + 1;}
int w1(int idx) {return idx - 1;}
int n2(int idx) {return idx - 2 * g_width;}
int s2(int idx) {return idx + 2 * g_width;}
int e2(int idx) {return idx + 2;}
int w2(int idx) {return idx - 2;}

dir_t *get_dir_one(void)
{
    dir_t *dir = malloc(4 * sizeof(dir_t));
    dir[0] = n1;
    dir[1] = s1;
    dir[2] = e1;
    dir[3] = w1;

    return dir;
}

dir_t *get_dir_two(void)
{
    dir_t *dir = malloc(4 * sizeof(dir_t));
    dir[0] = n2;
    dir[1] = s2;
    dir[2] = e2;
    dir[3] = w2;

    return dir;
}
