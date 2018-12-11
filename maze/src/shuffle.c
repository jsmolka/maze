#include "shuffle.h"

#include <stdlib.h>

void shuffle(int *array)
{
    for (int i = 0; i < 3; ++i)
    {
        const int j = i + rand() / (RAND_MAX / (4 - i) + 1);
        const int t = array[j];
        array[j] = array[i];
        array[i] = t;
    }
}
