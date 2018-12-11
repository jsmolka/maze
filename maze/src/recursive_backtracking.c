#include "recursive_backtracking.h"

#include <stdbool.h>
#include <stdlib.h>
#include <time.h>

#include "directions.h"
#include "shuffle.h"
#include "stack.h"

uint8_t *maze;
dir_t *dir_one;
dir_t *dir_two;
int range[4] = {0, 1, 2, 3};
int row_count_with_walls;
int col_count_with_walls;
int max_idx;

static bool out_ouf_bounds(int idx)
{
    return idx >= max_idx || (idx % col_count_with_walls) % 2 == 0;
}

static int walk(int idx)
{
    shuffle(range);

    for (int i = 0; i < 4; ++i)
    {
        const int j = range[i];
        const int idx2 = dir_two[j](idx);
        if (!out_ouf_bounds(idx2) && maze[idx2] == 0)
        {
            const int idx1 = dir_one[j](idx);
            maze[idx1] = maze[idx2] = 255;
            
            return idx2;
        }
    }
    return -1;
}

static int backtrack(stack_t *stack)
{
    while (!stack_empty(stack))
    {
        const int idx = stack_pop(stack);
        for (int i = 0; i < 4; ++i)
        {
            const int tidx = dir_two[i](idx);
            if (!out_ouf_bounds(tidx) && maze[tidx] == 0)
                return idx;
        }
    }
    return -1;
}

void recursive_backtracking(uint8_t *input, int row_count, int col_count, int idx)
{
    srand(time(NULL));

    row_count_with_walls = 2 * row_count + 1;
    col_count_with_walls = 2 * col_count + 1;
    max_idx = row_count_with_walls * col_count_with_walls;

    init(col_count_with_walls);
    dir_one = get_dir_one();
    dir_two = get_dir_two();

    maze = input;
    maze[idx] = 255;
    
    stack_t *stack = stack_new();
    while (idx != -1)
    {
        while (idx != -1)
        {
            stack_push(stack, idx);
            idx = walk(idx);
        }
        idx = backtrack(stack);
    }
    stack_free(stack);
    free(dir_one);
    free(dir_two);
}

