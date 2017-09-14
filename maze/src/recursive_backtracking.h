#ifndef RECURSIVE_BACKTRACKING_H
#define RECURSIVE_BACKTRACKING_H

#include <stdlib.h>
#include <stdbool.h>
#include <stdint.h>
#include <time.h>
#include "directions.h"
#include "stack.h"
#include "shuffle.h"

typedef struct walk_s
{
    index_t idx;
    bool walking;
} walk_t;

void recursive_backtracking(uint8_t* array, size_t idx, size_t row_count, size_t col_count);

#endif
