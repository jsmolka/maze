#include "depth_first_search.h"

uint8_t* maze;
dir_t* dir_one;
dir_t* dir_two;
int col_count_with_walls;

int s_walk(int idx)
{
    for (int i = 0; i < 4; i++)
    {
        int idx1 = dir_one[i](idx);
        if (maze[idx1] == 255)
        {
            int idx2 = dir_two[i](idx);
            maze[idx1] = maze[idx2] = 0;
            return idx2;
        }
    }
    return -1;
}

int s_backtrack(stack_t* stack)
{
    while (!stack_empty(stack))
    {
        int idx = stack_pop(stack);
        for (int i = 0; i < 4; i++)
        {
            int tidx = dir_one[i](idx);
            if (maze[tidx] == 255)
            {
                return idx;
            }
        }
    }
    return -1;
}

void assign_color(uint8_t* output, int idx, int iteration, float offset)
{
    output[idx] = (int)255 - iteration * offset;
    output[idx + 1] = 0;
    output[idx + 2] = (int)0 + iteration * offset;
}

void draw_path(stack_t* stack, uint8_t* output)
{
    int size = stack_size(stack);
    int* index_stack = malloc(size * sizeof(int));
    for (int i = 0; i < size; i++)
    {
        index_stack[i] = 3 * stack_pop(stack);
    }

    float offset = (float)255 / (2 * size);
    for (int i = 0; i < size - 1; i ++)
    {
        int idx = (index_stack[i] + index_stack[i + 1]) / 2;
        assign_color(output, index_stack[i], 2 * i, offset);
        assign_color(output, idx, 2 * i + 1, offset);
    }
    assign_color(output, index_stack[size - 1], 2 * (size - 1), offset);
}

void depth_first_search(uint8_t* input, uint8_t* output, int col_count, int start, int end)
{
    col_count_with_walls = 2 * col_count + 1;
    maze = input;

    initialize(col_count_with_walls);
    dir_one = get_dir_one();
    dir_two = get_dir_two();

    int idx = start;
    maze[idx] = 0;

    stack_t* stack = stack_new();
    while (idx != -1)
    {
        while (idx != -1)
        {
            stack_push(stack, idx);
            if (idx == end)
            {
                return draw_path(stack, output);
            }
            idx = s_walk(idx);
        }
        idx = s_backtrack(stack);
    }
}
