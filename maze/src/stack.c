#include "stack.h"

bool stack_empty(stack_t* stack)
{
    return stack == NULL || stack->top == NULL;
}

int stack_size(stack_t* stack)
{
    stack_frame_t* frame = stack->top;
    int size = 0;

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

int stack_pop(stack_t* stack)
{
    stack_frame_t* frame = stack->top;
    int idx = (int)frame->idx;
    stack->top = frame->next;
    free(frame);
    return idx;
}

void stack_push(stack_t* stack, int idx)
{
    stack_frame_t* frame = malloc(sizeof(stack_frame_t*));
    frame->idx = (int*)idx;
    frame->next = stack->top;
    stack->top = frame;
}
