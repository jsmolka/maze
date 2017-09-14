#ifndef SHUFFLE_H
#define SHUFFLE_H

#include <stdlib.h>
#include "directions.h"

/* Seed with srand(time(NULL)) at startup */
void shuffle(directions_b_t* array);

#endif
