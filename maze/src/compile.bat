@echo off

gcc -static-libgcc -shared -fPIC -o maze64.dll depth_first_search.c directions.c recursive_backtracking.c shuffle.c stack.c