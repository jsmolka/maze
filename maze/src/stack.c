#include "stack.h"

bool stack_empty(stack_t* stack)
{
    if (stack == NULL || stack->top == NULL)
    {
        return true;
    }
    else
    {
        return false;
    }
}

long stack_size(stack_t* stack)
{
    stack_frame_t* frame = stack->top;
    long size = 0;

    while (frame != NULL)
    {
        size++;
        frame = frame->next;
    }
    return size;
}

stack_t* stack_new()
{
    stack_t* stack = malloc(sizeof(*stack));
    stack->top = NULL;
    return stack;
}

index_t stack_pop(stack_t* stack)
{
    stack_frame_t* frame = stack->top;
    index_t idx = (index_t)frame->idx;
    stack->top = frame->next;
    free(frame);
    return idx;
}

void stack_push(stack_t* stack, index_t idx)
{
    stack_frame_t* frame = malloc(sizeof(stack_frame_t*));
    frame->idx = (index_t*)idx;
    frame->next = stack->top;
    stack->top = frame;
}
