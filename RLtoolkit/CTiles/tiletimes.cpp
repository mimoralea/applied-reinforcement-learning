#include <stdio.h>
#include <sys/types.h>
#include <sys/time.h>

#include "tiles.h"

void runit (int num=10, int ct=2048, int numt=1)
{
    int i,j;
    float vars[2];
    int* the_tiles = (int*) malloc(numt*sizeof(int));
    for (i=0; i<num; i++)
    {
        for (j=0; j<num; j++)
        {
            vars[0] = i*0.5;
            vars[1] = j*0.5;
            tiles(the_tiles, numt, ct, vars, 2, NULL, 0);
        }
    }
}

void runit2 (int num=10, int ct=2048, int numt=1)
{
    int i,j;
    float vars[4];
    int ints[2];
    int* the_tiles = (int*)malloc(numt*sizeof(int));
    for (i=0; i < num; i++)
    {
        for (j=0; j < num; j++)
        {
            vars[0] = i*0.5;
            vars[1] = j*0.5;
            vars[2] = float(i+j)/2;
            vars[3] = float(i-j)/2;
            ints[0] = i;
            ints[1] = j;
            tiles(the_tiles, numt, ct, vars, 4, ints, 2);
        }
    }
}

void runitw (int num=10, int ct=2048, int numt=1)
{
    int i,j;
    float vars[2];
    int ints[2];
    int* the_tiles = (int*)malloc(numt * sizeof(int));
    for (i=0; i < num; i++)
    {
        for (j=0; j < num; j++)
        {
            vars[0] = i*0.5;
            vars[1] = j*0.5;
            ints[0] = 10;
            ints[1] = 1;
            tileswrap(the_tiles,numt, ct, vars, 2, ints,NULL,0);
        }
    }
}

void runitl (int num=10, int ct=2048, int numt=1)
{
    int i,j;
    float vars[2];
    int* tlist = (int*)malloc((num*num*numt)*sizeof(int));
    for (i=0; i < num; i++)
    {
        for (j=0; j < num; j++)
        {
            vars[0] = i*0.5;
            vars[1] = j*0.5;
            tiles(tlist+(i*num*num+j), numt, ct, vars, 2,NULL,0);
        }
    }
}

void runitlw (int num=10, int ct=2048, int numt=1)
{
    int i,j;
    float vars[2];
    int ints[2];
    int* tlist = (int*)malloc((num*num*numt)*sizeof(int));
    for (i=0; i < num; i++)
    {
        for (j=0; j < num; j++)
        {
            vars[0] = i*0.5;
            vars[1] = j*0.5;
            ints[0] = 10;
            ints[1] = 1;
            tileswrap(tlist+(i*num*numt+j), numt, ct, vars, 2, ints,NULL,0);
        }
    }

}

////////////////////Collision table versions

void runit_ct (int num=10, collision_table* ct=NULL, int numt=1)
{
    int i,j;
    float vars[2];
    int* the_tiles = (int*) malloc(numt*sizeof(int));
    for (i=0; i<num; i++)
    {
        for (j=0; j<num; j++)
        {
            vars[0] = i*0.5;
            vars[1] = j*0.5;
            tiles(the_tiles, numt, ct, vars, 2, NULL, 0);
        }
    }
}

void runitn_ct (int num=10, collision_table* ct=NULL, int numt=4)
{
    int i,j;
    float vars[2];
    int* the_tiles = (int*)malloc(numt*sizeof(int));
    for (i=0; i < num; i++)
    {
        for (j=0; j < num; j++)
        {
            vars[0] = i*0.5;
            vars[1] = j*0.5;
            tiles(the_tiles,numt, ct, vars, 2, NULL, 0);
        }
    }
}

void runit2_ct (int num=10, collision_table* ct=NULL, int numt=1)
{
    int i,j;
    float vars[4];
    int ints[2];
    int* the_tiles = (int*)malloc(numt*sizeof(int));
    for (i=0; i < num; i++)
    {
        for (j=0; j < num; j++)
        {
            vars[0] = i*0.5;
            vars[1] = j*0.5;
            vars[2] = float(i+j)/2;
            vars[3] = float(i-j)/2;
            ints[0] = i;
            ints[1] = j;
            tiles(the_tiles, numt, ct, vars, 4, ints, 2);
        }
    }
}

void runitw_ct (int num=10, collision_table* ct=NULL, int numt=1)
{
    int i,j;
    float vars[2];
    int ints[2];
    int* the_tiles = (int*)malloc(numt * sizeof(int));
    for (i=0; i < num; i++)
    {
        for (j=0; j < num; j++)
        {
            vars[0] = i*0.5;
            vars[1] = j*0.5;
            ints[0] = 10;
            ints[1] = 1;
            tileswrap(the_tiles,numt, ct, vars, 2, ints,NULL,0);
        }
    }
}

void runitl_ct (int num=10, collision_table* ct=NULL, int numt=1)
{
    int i,j;
    float vars[2];
    int* tlist = (int*)malloc((num*num*numt)*sizeof(int));
    for (i=0; i < num; i++)
    {
        for (j=0; j < num; j++)
        {
            vars[0] = i*0.5;
            vars[1] = j*0.5;
            tiles(tlist+(i*num*num+j), numt, ct, vars, 2,NULL,0);
        }
    }
}

void runitlw_ct (int num=10, collision_table* ct=NULL, int numt=1)
{
    int i,j;
    float vars[2];
    int ints[2];
    int* tlist = (int*)malloc((num*num*numt)*sizeof(int));
    for (i=0; i < num; i++)
    {
        for (j=0; j < num; j++)
        {
            vars[0] = i*0.5;
            vars[1] = j*0.5;
            ints[0] = 10;
            ints[1] = 1;
            tileswrap(tlist+(i*num*numt+j), numt, ct, vars, 2, ints,NULL,0);
        }
    }

}

collision_table* ctu;
collision_table* cts;
collision_table* ctss;

void initct(int mem=16384)
{
    ctu=new collision_table(mem, 0);
    cts=new collision_table(mem, 1);
    ctss=new collision_table(mem, 2);
}

void timetest(void (*command)(int,int,int),void (*command2)(int,collision_table*,int), char* info, 
                            char* info2="2 floats", int num=100, int numt=1, int mem=16384)            
{
    //time_t t1,t2;
    timeval t1, t2;
    float t;

    initct(mem);
    printf(" \n");
    printf("%s\n",info);
    printf("Timing over %d calls to tiles, %d tiling each for %s\n", num*num, numt, info2);
    
    (void)gettimeofday(&t1,0);
    (*command)(num,mem,numt);
    (void)gettimeofday(&t2,0);
    t = t2.tv_sec-t1.tv_sec + ((float)(t2.tv_usec - t1.tv_usec))/1000000.0;
    
    printf("With no collision table %f seconds\n",t);

    (void)gettimeofday(&t1,0);
    (*command2)(num,ctu,numt);
    (void)gettimeofday(&t2,0);
    t = t2.tv_sec-t1.tv_sec + ((float)(t2.tv_usec - t1.tv_usec))/1000000.0;
    
    printf("With unsafe collision table %f seconds\n",t);
    ctu->print();

    (void)gettimeofday(&t1,0);
    (*command2)(num,cts,numt);
    (void)gettimeofday(&t2,0);
    t = t2.tv_sec-t1.tv_sec + ((float)(t2.tv_usec - t1.tv_usec))/1000000.0;

    printf("With safe collision table %f seconds\n",t);
    cts->print();

    (void)gettimeofday(&t1,0);
    (*command2)(num,ctss,numt);
    (void)gettimeofday(&t2,0);
    t = t2.tv_sec-t1.tv_sec + ((float)(t2.tv_usec - t1.tv_usec))/1000000.0;
    
    printf("With super safe collision table %f seconds\n",t);
    ctss->print();

    printf(" \n");
    printf("Timing over %d calls to tiles, 16 tilings each for %s\n", num*num, info2);

    (void)gettimeofday(&t1,0);
    (*command)(num,16384,16);
    (void)gettimeofday(&t2,0);
    t = t2.tv_sec-t1.tv_sec + ((float)(t2.tv_usec - t1.tv_usec))/1000000.0;

    printf("With no collision table %f seconds\n",t);
}

int main(void)
{
    timeval t1, t2;
    float t;
    timetest(runit, runit_ct, "Standard test", "2 floats",100,4);
    timetest(runit2,runit2_ct, "Testing with more input variables","4 floats, 2 ints", 100, 3, 32768);
    timetest(runitw,runitw_ct, "WRAP version", "2 floats",100,4);
    timetest(runitl,runitl_ct, "Load version", "2 floats", 10, 4); //# only do 10 x 10 calls, but with 4 tilings each
    timetest(runitlw,runitlw_ct, "Load WRAP version", "2 floats", 10, 4);
    return 0;
}
