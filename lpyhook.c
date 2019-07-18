#include <sys/mman.h>
#include <unistd.h>
#include <string.h>

#include "lpyhook.h"

#pragma pack(push, 1)
static struct {
    char push_rax;
    char mov_rax[2];
    char addr[8];
    char jmp_rax[2];
}

jumper = {
   .push_rax = 0x50,
   .mov_rax  = {0x48, 0xb8},
   .jmp_rax = {0xff, 0xe0}
};
#pragma pack(pop)

static int up(void* addr) {
    return mprotect((char *)((size_t)addr & ~(sysconf(_SC_PAGE_SIZE) -1)), sysconf(_SC_PAGE_SIZE), PROT_WRITE | PROT_READ | PROT_EXEC);
}
int lpyhook(void* t, void* r) {
    int count;

    if(up(r) || up(t)) {
        return 1;
    }

    for(count = 0; count < 255 && ((unsigned char*)r)[count] != 0x90; ++count);

    if(count == 255) {
        return 1;
    }

    memmove(r+1, r, count);
    *((unsigned char *)r) = 0x58;
    memcpy(jumper.addr, &r, sizeof (void *));
    memcpy(t, &jumper, sizeof jumper);
    return 0;
}
