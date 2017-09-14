#ifndef STACK_H
#define STACK_H

#include <stdlib.h>
#include <stdbool.h>

struct stack_frame_s
{
  struct stack_frame_s* next;
  int* data;
};
typedef struct stack_s
{
  struct stack_frame_s* top;
} stack_t;

stack_t* stack_new();
bool stack_empty(stack_t* stack);
int* stack_pop(stack_t* stack);
void stack_push(stack_t* stack, int* data);

#endif
