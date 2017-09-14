#include "shuffle.h"

void shuffle(directions_b_t* array)
{
    for (size_t i = 0; i < 3; i++)
    {
        size_t j = i + rand() / (RAND_MAX / (4 - i) + 1);
        directions_b_t t = array[j];
        array[j] = array[i];
        array[i] = t;
    }
}
