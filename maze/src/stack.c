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

stack_t* stack_new()
{
    stack_t* stack = malloc(sizeof(*stack));
    stack->top = NULL;
    return stack;
}

int* stack_pop(stack_t* stack)
{
    struct stack_frame_s* frame = stack->top;
    int* data = frame->data;
    stack->top = frame->next;
    free(frame);
    return data;
}

void stack_push(stack_t* stack, int* data)
{
    struct stack_frame_s* frame = malloc(sizeof(*frame));
    frame->data = data;
    frame->next = stack->top;
    stack->top = frame;
}
