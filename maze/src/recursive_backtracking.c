#include "recursive_backtracking.h"

/* Define global variables */
uint8_t* maze;
size_t row_count_with_walls;
size_t col_count_with_walls;
size_t max_index;

void mark_visited(index_t idx)
{
    maze[idx] = 255;
}

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

    directions_b_t* dir_two = get_dir_two();
    shuffle(dir_two);
    for (size_t i = 0; i < 4; i++)  /* Check adjacent cells randomly */
    {
        indices_t idc = dir_two[i](idx);
        if (!out_ouf_bounds(idc.idx1) && maze[idc.idx1] == 0)  /* Check if unvisited */
        {
            mark_visited(idc.idx1);
            mark_visited(idc.idx2);
            w.idx = idc.idx1;
            free(dir_two);
            return w;  /* Return new index and continue walking */
        }
    }
    w.walking = false;
    free(dir_two);
    return w;  /* Return old index and stop walking */
}

index_t c_backtrack(stack_t* stack)
{
    directions_t* c_dir_one = get_c_dir_one();
    while (!stack_empty(stack))
    {
        index_t idx = (index_t)stack_pop(stack);
        for (size_t i = 0; i < 4; i++)  /* Check adjacent cells */
        {
            index_t tidx = c_dir_one[i](idx);
            if (!out_ouf_bounds(tidx) && maze[tidx] == 0)  /* Check if unvisited */
            {
                free(c_dir_one);
                return idx;  /* Return index with unvisited neighbour */
            }
        }
    }
    free(c_dir_one);
    return -1;  /* Return stop values if stack is empty */
}

void recursive_backtracking(uint8_t* array, size_t idx, size_t row_count, size_t col_count)
{
    row_count_with_walls = 2 * row_count + 1;
    col_count_with_walls = 2 * col_count + 1;
    max_index = row_count_with_walls * col_count_with_walls;
    maze = array;

    setup_directions(col_count_with_walls);
    srand(time(NULL));  /* Seed rand with time */
    stack_t* stack = stack_new();

    walk_t w;
    w.idx = idx;
    mark_visited(w.idx);

    while (w.idx != -1)
    {
        w.walking = true;
        while (w.walking)
        {
            stack_push(stack, (index_t*)w.idx);
            w = c_walk(w.idx);
        }
        w.idx = c_backtrack(stack);
    }
    free(stack);
}
