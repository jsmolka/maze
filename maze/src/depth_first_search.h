#ifndef DEPTH_FIRST_SEARCH_H
#define DEPTH_FIRST_SEARCH_H

#include <stdlib.h>
#include <stdbool.h>
#include <stdint.h>
#include "directions.h"
#include "stack.h"

typedef struct walk_s
{
    index_t idx;
    bool walking;
} walk_t;

void depth_first_search(uint8_t* input, uint32_t* output, size_t col_count, uint32_t start, uint32_t end);

#endif
