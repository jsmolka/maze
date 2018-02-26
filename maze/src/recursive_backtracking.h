#ifndef RECURSIVE_BACKTRACKING_H
#define RECURSIVE_BACKTRACKING_H

#include <stdlib.h>
#include <stdbool.h>
#include <stdint.h>
#include <time.h>
#include "directions.h"
#include "shuffle.h"
#include "stack.h"

void recursive_backtracking(uint8_t* input, int row_count, int col_count, int idx);

#endif
