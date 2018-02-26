#ifndef DIRECTIONS_H
#define DIRECTIONS_H

#include <stdlib.h>

typedef int (*dir_t)(int);

int n1(int idx);
int s1(int idx);
int e1(int idx);
int w1(int idx);
int n2(int idx);
int s2(int idx);
int e2(int idx);
int w2(int idx);

void initialize(int width);

dir_t* get_dir_one();
dir_t* get_dir_two();

#endif
