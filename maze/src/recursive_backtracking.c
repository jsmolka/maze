#include "recursive_backtracking.h"

uint8_t* maze;
dir_t* dir_one;
dir_t* dir_two;
int* range;
int row_count_with_walls;
int col_count_with_walls;
int max_index;

bool out_ouf_bounds(int idx)
{
    return idx >= max_index || (idx % col_count_with_walls) % 2 == 0;
}

int c_walk(int idx)
{
    shuffle(range);
    for (int i = 0; i < 4; i++)
    {
        int j = range[i];
        int idx2 = dir_two[j](idx);
        if (!out_ouf_bounds(idx2) && maze[idx2] == 0)
        {
            int idx1 = dir_one[j](idx);
            maze[idx1] = maze[idx2] = 255;
            return idx2;
        }
    }
    return -1;
}

int c_backtrack(stack_t* stack)
{
    while (!stack_empty(stack))
    {
        int idx = stack_pop(stack);
        for (int i = 0; i < 4; i++)
        {
            int tidx = dir_two[i](idx);
            if (!out_ouf_bounds(tidx) && maze[tidx] == 0)
            {
                return idx;
            }
        }
    }
    return -1;
}

void recursive_backtracking(uint8_t* input, int row_count, int col_count, int idx)
{
    srand(time(NULL));

    row_count_with_walls = 2 * row_count + 1;
    col_count_with_walls = 2 * col_count + 1;
    max_index = row_count_with_walls * col_count_with_walls;
    maze = input;

    initialize(col_count_with_walls);
    dir_one = get_dir_one();
    dir_two = get_dir_two();

    range = malloc(4 * sizeof(int));
    range[0] = 0;
    range[1] = 1;
    range[2] = 2;
    range[3] = 3;

    maze[idx] = 255;
    stack_t* stack = stack_new();
    while (idx != -1)
    {
        while (idx != -1)
        {
            stack_push(stack, idx);
            idx = c_walk(idx);
        }
        idx = c_backtrack(stack);
    }
}
