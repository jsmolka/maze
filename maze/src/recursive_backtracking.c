#include "recursive_backtracking.h"

/* Define global variables */
uint8_t* maze;
directions_t* c_dir_one;
directions_b_t* dir_two;
size_t row_count_with_walls;
size_t col_count_with_walls;
index_t max_index;

bool out_ouf_bounds(index_t idx)
{
    /* Check if index is out of bounds or if y is even */
    if (idx < 0 || idx >= max_index || (idx % col_count_with_walls) % 2 == 0)
    {
        return true;
    }
    else
    {
        return false;
    }
}

walk_t c_walk(index_t idx)
{
    walk_t w;
    w.idx = idx;
    w.walking = true;

    shuffle(dir_two);
    for (size_t i = 0; i < 4; i++)  /* Check adjacent cells randomly */
    {
        indices_t idc = dir_two[i](idx);
        if (!out_ouf_bounds(idc.idx1) && maze[idc.idx1] == 0)  /* Check if unvisited */
        {
            maze[idc.idx1] = maze[idc.idx2] = 255;  /* Mark as visited */
            w.idx = idc.idx1;
            return w;  /* Return new index and continue walking */
        }
    }
    w.walking = false;
    return w;  /* Return old index and stop walking */
}

index_t c_backtrack(stack_t* stack)
{
    while (!stack_empty(stack))
    {
        index_t idx = stack_pop(stack);
        for (size_t i = 0; i < 4; i++)  /* Check adjacent cells */
        {
            index_t tidx = c_dir_one[i](idx);
            if (!out_ouf_bounds(tidx) && maze[tidx] == 0)  /* Check if unvisited */
            {
                return idx;  /* Return index with unvisited neighbour */
            }
        }
    }
    return -1;  /* Return stop values if stack is empty */
}

void recursive_backtracking(uint8_t* input, size_t idx, size_t row_count, size_t col_count)
{
    row_count_with_walls = 2 * row_count + 1;
    col_count_with_walls = 2 * col_count + 1;
    max_index = row_count_with_walls * col_count_with_walls;
    maze = input;

    setup_directions(col_count_with_walls);
    c_dir_one = get_c_dir_one();
    dir_two = get_dir_two();
    srand(time(NULL));  /* Seed rand with time */
    stack_t* stack = stack_new();

    walk_t w;
    w.idx = idx;
    maze[w.idx] = 255;  /* Mark as visited */

    while (w.idx != -1)
    {
        w.walking = true;
        while (w.walking)
        {
            stack_push(stack, w.idx);
            w = c_walk(w.idx);
        }
        w.idx = c_backtrack(stack);
    }
}
