#include "depth_first_search.h"

#include <stdbool.h>
#include <stdlib.h>

#include "directions.h"
#include "stack.h"

uint8_t *maze;
dir_t *dir_one;
dir_t *dir_two;
int col_count_with_walls;

static int walk(int idx)
{
    for (int i = 0; i < 4; ++i)
    {
        const int idx1 = dir_one[i](idx);
        if (maze[idx1] == 255)
        {
            const int idx2 = dir_two[i](idx);
            maze[idx1] = maze[idx2] = 0;

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
            const int tidx = dir_one[i](idx);
            if (maze[tidx] == 255)
                return idx;
        }
    }
    return -1;
}

static void color(uint8_t *output, int idx, int iteration, float offset)
{
    const int clr = (int)iteration * offset;
    
    output[idx] = 255 - clr;
    output[idx + 1] = 0;
    output[idx + 2] = clr;
}

static void draw_path(stack_t *stack, uint8_t *output)
{
    const int total = 2 * stack_size(stack);
    const float offset =  (float)255 / (float)total;

    int idx1 = stack_pop(stack);
    color(output, 3 * idx1, 0, offset);

    for (int i = 2; i < total; i += 2)
    {
        const int idx2 = stack_pop(stack);
        const int idx3 = (idx1 + idx2) / 2;
        color(output, 3 * idx2, i, offset);
        color(output, 3 * idx3, i - 1, offset);
        idx1 = idx2;
    }
}

void depth_first_search(uint8_t *input, uint8_t *output, int col_count, int start, int end)
{
    col_count_with_walls = 2 * col_count + 1;

    init(col_count_with_walls);
    dir_one = get_dir_one();
    dir_two = get_dir_two();

    int idx = start;

    maze = input;
    maze[idx] = 0;

    stack_t *stack = stack_new();
    while (idx != -1)
    {
        while (idx != -1)
        {
            stack_push(stack, idx);
            if (idx == end)
            {
                draw_path(stack, output);
                break;
            }
            idx = walk(idx);
        }
        idx = backtrack(stack);
    }
    stack_free(stack);
    free(dir_one);
    free(dir_two);
}
