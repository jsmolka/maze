#ifndef RECURSIVE_BACKTRACKING_H
#define RECURSIVE_BACKTRACKING_H

#include <stdlib.h>
#include <stdbool.h>
#include <stdint.h>
#include <time.h>
#include "directions.h"
#include "stack.h"
#include "shuffle.h"

/* Define types */
typedef struct walk_s
{
    index_t idx;
    bool walking;
} walk_t;

/* Define functions */
void recursive_backtracking(uint8_t* input, size_t row_count, size_t col_count, index_t idx);

#endif
