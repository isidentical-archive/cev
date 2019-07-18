if __name__ == "__main__":
    from libcgen import *
    lpyhook = CGen("LPyHook")

    hook_sign = Sign("int", "lpyhook", [Sign("void*", "t"), Sign("void*", "r")])
    lpyhook.gen_header(hook_sign)

    packpush_source = (
        "static struct {",
        f"    {Sign('char', 'push_rax')};",
        f"    {Sign('char', 'mov_rax[2]')};",
        f"    {Sign('char', 'addr[8]')};",
        f"    {Sign('char', 'jmp_rax[2]')};",
        "}",
        "",
        "jumper = {",
        "   .push_rax = 0x50,",
        "   .mov_rax  = {0x48, 0xb8},",
        "   .jmp_rax = {0xff, 0xe0}",
        "};",
    )
    source_pragmas = [
        Pragma("pack", ["push", "1"], packpush_source),
        Pragma("pack", ["pop"]),
    ]
    code = textwrap.dedent(
        """
        %s(%s) {
            return mprotect((char *)((size_t)addr & ~(sysconf(_SC_PAGE_SIZE) -1)), sysconf(_SC_PAGE_SIZE), %s);
        }
        %s(%s) {
            %s;

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
    """
        % (
            Sign("static int", "up"),
            Sign("void*", "addr"),
            " | ".join([f"PROT_{op.upper()}" for op in {"read", "write", "exec"}]),
            Sign("int", "lpyhook"),
            ", ".join(map(str, [Sign("void*", "t"), Sign("void*", "r")])),
            Sign("int", "count"),
        )
    )
    lpyhook.gen_source(libs=[ "_lpyhook", "string", "unistd", "sys/mman"], pragmas=source_pragmas, source=code)
    lpyhook.generate()
