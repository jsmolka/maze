#ifndef DEPTH_FIRST_SEARCH_H
#define DEPTH_FIRST_SEARCH_H

#include <stdlib.h>
#include <stdbool.h>
#include <stdint.h>
#include "directions.h"
#include "stack.h"

void depth_first_search(uint8_t* input, uint8_t* output, int col_count, int start, int end);

#endif
