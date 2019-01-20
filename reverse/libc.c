#define _GNU_SOURCE
#include <dlfcn.h>
#include <string.h>
#include <stdio.h>

// gcc -Wall -fPIC -shared -o libc.so libc.c 
// LD_PRELOAD=./libc.so ./fixme  

typedef int (*ostrcmp)(const char* s1, const char* s2);
int strcmp(const char* s1, const char* s2){
    printf("[strcmp] s1: %s\n", s1);
    printf("[strcmp] s2: %s\n", s2);

    ostrcmp orig = (ostrcmp)dlsym(RTLD_NEXT, "strcmp");    
    return orig(s1, s2);
}


typedef int (*ostrncmp)(const char* s1, const char* s2, size_t n);
int strncmp(const char* s1, const char* s2, size_t n){   
    printf("[strncmp] s1: %s\n", s1);
    printf("[strncmp] s2: %s\n", s2);

    ostrncmp orig = (ostrncmp)dlsym(RTLD_NEXT, "strncmp");    
    return orig(s1, s2,n);
}


typedef char* (*ostrncpy)(char * destination, const char * source, size_t num );
char * strncpy ( char * destination, const char * source, size_t num )
{
	printf("[strcpy] src: %s\n", source);

	ostrncpy orig = (ostrncpy)dlsym(RTLD_NEXT,"strncpy");	
	return orig(destination, source, num);
}


typedef size_t (*ostrlen)(const char *str);
size_t strlen(const char *str) {
	printf("[strlen] %s\n",str);
	
	ostrlen orig = (ostrlen)dlsym(RTLD_NEXT, "strlen");
	return orig(str);
}
