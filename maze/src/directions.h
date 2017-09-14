#ifndef DIRECTIONS_H
#define DIRECTIONS_H

#include <stdlib.h>

/* Define types */
typedef int index_t;
typedef struct indices_s
{
    index_t idx1;
    index_t idx2;
} indices_t;
typedef index_t (*directions_t)(index_t);
typedef indices_t (*directions_b_t)(index_t);

/* Define direction functions */
index_t n1(index_t idx);  /* Returns northern index with a step length of one */
index_t s1(index_t idx);  /* Returns southern index with a step length of one */
index_t e1(index_t idx);  /* Returns eastern index with a step length of one */
index_t w1(index_t idx);  /* Returns western index with a step length of one */
index_t n2(index_t idx);  /* Returns northern index with a step length of two */
index_t s2(index_t idx);  /* Returns southern index with a step length of two */
index_t e2(index_t idx);  /* Returns eastern index with a step length of two */
index_t w2(index_t idx);  /* Returns western index with a step length of two */
indices_t n2b(index_t idx);  /* Returns northern indices with a step length of two */
indices_t s2b(index_t idx);  /* Returns southern indices with a step length of two */
indices_t e2b(index_t idx);  /* Returns eastern indices with a step length of two */
indices_t w2b(index_t idx);  /* Returns western indices with step length of two */

/* Define setup function */
void setup_directions(size_t width);  /* Set global variable to calculate directions */

/* Define directions */
directions_t* get_c_dir_one();
directions_t* get_s_dir_one();
directions_b_t* get_dir_two();

#endif
