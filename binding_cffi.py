import cffi
import pathlib
import re
import sys
import os
import invoke

on_win = sys.platform.startswith("win")

def print_banner(msg):
    print("==================================================")
    print("= {} ".format(msg))

def build_cmult(path="C:\\Program Files (x86)\\Microsoft Visual Studio\\2019\\Professional\\VC\\Auxiliary\\Build\\"):
    """Build the shared library for the sample C code"""
    # Moving this type hint into signature causes an error (???)
    c = invoke.Context()

    if on_win:
        if not path:
            print("Path is missing")
        else:
            # Using c.cd didn't work with paths that have spaces :/
            path = f'"{path}vcvars32.bat" x64'  # Enter the VS venv
            path += f'&& cd "{os.getcwd()}"'  # Change to current dir
            path += "&& cl /LD cmult.c"  # Compile
            # Uncomment line below, to suppress stdout
            # path = path.replace("&&", " >nul &&") + " >nul"
            c.run(path)
    else:
        print_banner("Building C Library")
        cmd = "gcc -c -Wall -Werror -fpic cmult.c -I /usr/include/python3.7"
        invoke.run(cmd)
        invoke.run("gcc -shared -o libcmult.so cmult.o")
        print("* Complete")

def build_cffi():
    """Build the CFFI Python bindings"""
    print_banner("Building CFFI Module")
    ffi = cffi.FFI()

    this_dir = pathlib.Path().resolve()
    h_file_name = this_dir / "cmult.h"
    with open(h_file_name) as h_file:
        # cffi does not like our preprocessor directives, so we remove them
        lns = h_file.read().splitlines()
        flt = filter(lambda ln: not re.match(r" *#", ln), lns)
        flt = map(lambda ln: ln.replace("EXPORT_SYMBOL ", ""), flt)
        ffi.cdef(str("\n").join(flt))

    ffi.set_source(
        "cffi_example",
        # Since we are calling a fully built library directly no custom source
        # is necessary. We need to include the .h files, though, because behind
        # the scenes cffi generates a .c file which contains a Python-friendly
        # wrapper around each of the functions.
        '#include "cmult.h"',
        # The important thing is to include the pre-built lib in the list of
        # libraries we are linking against:
        libraries=["cmult"],
        library_dirs=[this_dir.as_posix()],
        extra_link_args=["-Wl,-rpath,."],
    )

    ffi.compile()
    print("* Complete")

build_cmult()
build_cffi()