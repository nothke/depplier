# depplier
A script for easier C++ dependancies assignment, made to bypass annoying, 90s design, finnicky Visual Studio properties. "Deplier" stands for "dependency applier".

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
// Corresponds to C++ > General > "Additional Include Directories":
include =
    deps\include

// Corresponds to Linker > General > "Additional Library Directories":
libdir =
    deps\sdl\lib\x64

// Corresponds to Linker > Input > Additional Dependencies
deps =
    SDL2.lib
    SDL2main.lib
    mydep.lib

// Specific configurations are named as [Configuration|Platform]
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

### Details
* deps.ini [SECTIONS] define your configuration in the form of [Debug|x64] with [ALL] being a special configuration that will be added to all configurations

### Not tested

Using it for personal use. If you find an error, report it so I can fix it!
