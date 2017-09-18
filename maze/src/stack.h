#ifndef STACK_H
#define STACK_H

#include <stdlib.h>
#include <stdbool.h>

#include "directions.h"

/* Define types */
typedef struct stack_frame_s
{
  struct stack_frame_s* next;
  index_t* idx;
} stack_frame_t;

typedef struct stack_s
{
  stack_frame_t* top;
} stack_t;

/* Define functions */
stack_t* stack_new();
bool stack_empty(stack_t* stack);
long stack_size(stack_t* stack);
index_t stack_pop(stack_t* stack);
void stack_push(stack_t* stack, index_t idx);

#endif
