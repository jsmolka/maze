#include "depth_first_search.h"

/* Define global variables */
uint8_t* maze;
directions_t* s_dir_one;
directions_b_t* dir_two;
size_t col_count_with_walls;

walk_t s_walk(index_t idx)
{
    walk_t w;
    w.idx = idx;
    w.walking = true;

    for (size_t i = 0; i < 4; i++)  /* Check adjacent cells */
    {
        indices_t idc = dir_two[i](idx);
        if (maze[idc.idx2] == 255)  /* Check if unvisited */
        {
            maze[idc.idx1] = maze[idc.idx2] = 0;  /* Mark as visited */
            w.idx = idc.idx1;
            return w;  /* Return new index and continue walking */
        }
    }
    w.walking = false;
    return w;  /* Return old index and stop walking */
}

index_t s_backtrack(stack_t* stack)
{
    while (!stack_empty(stack))
    {
        index_t idx = stack_pop(stack);
        for (size_t i = 0; i < 4; i++)  /* Check adjacent cells */
        {
            index_t tidx = s_dir_one[i](idx);
            if (maze[tidx] == 255)  /* Check if unvisited */
            {
                return idx;  /* Return index with unvisited neighbour */
            }
        }
    }
    return -1;  /* Return stop values if stack is empty */
}

void assign_color(uint8_t* output, index_t idx, size_t iteration, float offset)
{
    output[idx] = (int)255 - iteration * offset;
    output[idx + 1] = 0;
    output[idx + 2] = (int)0 + iteration * offset;
}

void draw_path(stack_t* stack, uint8_t* output)
{
    size_t size = stack_size(stack);
    index_t* index_stack = malloc(size * sizeof(index_t));
    for (size_t i = 0; i < size; i++)
    {
        index_stack[i] = 3 * stack_pop(stack);  /* Convert stack into array */
    }

    float offset = (float)255 / (2 * size);
    for (size_t i = 0; i < size - 1; i ++)  /* Draw path */
    {
        index_t idx1 = index_stack[i];
        index_t idx2 = (idx1 + index_stack[i + 1]) / 2;
        assign_color(output, idx1, 2 * i, offset);
        assign_color(output, idx2, 2 * i + 1, offset);
    }
    assign_color(output, index_stack[size - 1], 2 * (size - 1), offset);
}

void depth_first_search(uint8_t* input, uint8_t* output, size_t col_count, index_t start, index_t end)
{
    col_count_with_walls = 2 * col_count + 1;
    maze = input;

    setup_directions(col_count_with_walls);
    s_dir_one = get_s_dir_one();
    dir_two = get_dir_two();
    stack_t* stack = stack_new();

    walk_t w;
    w.idx = start;
    maze[w.idx] = 0;

    while (w.idx != -1)
    {
        w.walking = true;
        while (w.walking)
        {
            stack_push(stack, w.idx);
            if (w.idx == end)
            {
                return draw_path(stack, output);
            }
            w = s_walk(w.idx);
        }
        w.idx = s_backtrack(stack);
    }
}
