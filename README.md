# depplier
Deplier - meaning "dependency applier" - is a script for easier C++ dependancies assignment, made to bypass annoying, 90s design, finnicky Visual Studio properties. 

### What does it do?

It uses a plain text ini file where you write your dependencies in a much nicer way and then applies it to your vcxproj file.

Simple sample of deps.ini:
```
[ALL]
include =
    deps\include

libdir =
    deps\sdl\lib\x64

deps =
    SDL2.lib
    SDL2main.lib
    mydep.lib

[Debug|x64]
libdir =
    deps\mylib\Debug

[Release|x64]
libdir =
    deps\mydep\Debug

```

Plain, simple and nice, right?

Explained:

```
// ALL is a special section that will be applied to all configurations:
[ALL]
// "include" corresponds to C++ > General > "Additional Include Directories":
// (indentation is important, otherwise configparser won't read is as a single line)
// all paths are relative to project, i.e. they will have "$(SolutionDir)" automatically prepended
include =
    deps\include

// "libdir" corresponds to Linker > General > "Additional Library Directories":
libdir =
    deps\sdl\lib\x64

// "deps" corresponds to Linker > Input > "Additional Dependencies"
deps =
    SDL2.lib
    SDL2main.lib
    mydep.lib

// Specific configurations are named as [Configuration|Platform]
// Will be appended after all deps found in "deps"
[Debug|x64]
libdir =
    deps\mylib\Debug

[Release|x64]
libdir =
    deps\mydep\Debug
```

### How to use

1. Put the deplier.py and deps.ini into the folder where your .vcxproj is
2. Add your dependencies to deps.ini
3. Run depplier.py
4. You will get a message in terminal if the application was successful and any messages or errors that might've happened, hit any key to shut it down.

- In case the terminal just flashes, i.e. immediately shuts down without success message, there's a bug!

### Not tested

- Using it for personal use. If you find an error, report it so I can fix it!
- If you have a suggestion for more features, contact me as well.