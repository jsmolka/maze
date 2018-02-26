#include "shuffle.h"

void shuffle(int* array)
{
    for (int i = 0; i < 3; i++)
    {
        int j = i + rand() / (RAND_MAX / (4 - i) + 1);
        int t = array[j];
        array[j] = array[i];
        array[i] = t;
    }
}
