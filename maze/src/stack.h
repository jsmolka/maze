#ifndef STACK_H
#define STACK_H

#include <stdbool.h>

typedef struct stack_frame_s
{
    struct stack_frame_s *next;
    int idx;
} stack_frame_t;

typedef struct stack_s
{
    stack_frame_t *top;
} stack_t;

stack_t *stack_new(void);
void stack_free(stack_t *stack);
bool stack_empty(stack_t *stack);
int stack_size(stack_t *stack);
void stack_push(stack_t *stack, int idx);
int stack_pop(stack_t *stack);

#endif /* STACK_H */
