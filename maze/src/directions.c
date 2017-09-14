#include "directions.h"

/* Define global variables */
size_t WIDTH;

/* Define setup function */
void setup_directions(size_t width)
{
    WIDTH = width;
}

/* Define direction functions */
index_t n1(index_t idx) {return idx - WIDTH;}
index_t s1(index_t idx) {return idx + WIDTH;}
index_t e1(index_t idx) {return idx + 1;}
index_t w1(index_t idx) {return idx - 1;}
index_t n2(index_t idx) {return idx - 2 * WIDTH;}
index_t s2(index_t idx) {return idx + 2 * WIDTH;}
index_t e2(index_t idx) {return idx + 2;}
index_t w2(index_t idx) {return idx - 2;}

indices_t n2b(index_t idx)
{
    indices_t idc;
    idc.idx1 = n2(idx);
    idc.idx2 = n1(idx);
    return idc;
}

indices_t s2b(index_t idx)
{
    indices_t idc;
    idc.idx1 = s2(idx);
    idc.idx2 = s1(idx);
    return idc;
}

indices_t e2b(index_t idx)
{
    indices_t idc;
    idc.idx1 = e2(idx);
    idc.idx2 = e1(idx);
    return idc;
}

indices_t w2b(index_t idx)
{
    indices_t idc;
    idc.idx1 = w2(idx);
    idc.idx2 = w1(idx);
    return idc;
}

/* Define directions */
directions_t* get_c_dir_one()
{
    directions_t* dir = malloc(4 * sizeof(directions_t));
    dir[0] = n2;
    dir[1] = s2;
    dir[2] = e2;
    dir[3] = w2;
    return dir;
}

directions_t* get_s_dir_one()
{
    directions_t* dir = malloc(4 * sizeof(directions_t));
    dir[0] = n1;
    dir[1] = s1;
    dir[2] = e1;
    dir[3] = w1;
    return dir;
}

directions_b_t* get_dir_two()
{
    directions_b_t* dir = malloc(4 * sizeof(directions_b_t));
    dir[0] = n2b;
    dir[1] = s2b;
    dir[2] = e2b;
    dir[3] = w2b;
    return dir;
}
