Note: I made this before I found about [premake](https://github.com/premake/premake-core). Premake can do exactly this and much much more. I recommend you use it (or other simple build configuration software) instead.

# depplier
Depplier - meaning "dependency applier" - is a script for easier C++ dependancies assignment, made to bypass annoying, 90s design, finnicky Visual Studio properties. 

### What does it do?

It uses a plain text ini file where you write your dependencies in a much nicer way and then applies it to your vcxproj file.

Simple sample of deps.ini:
``` ini
[ALL]
include =
    deps\include

libdir =
    deps\sdl\lib\x64

deps =
    SDL2.lib
    SDL2main.lib
    mylibrary.lib

[Debug|x64]
libdir =
    deps\mylibrary\Debug

[Release|x64]
libdir =
    deps\mylibrary\Release

```

Plain, simple and nice, right?

Explained:

``` ini
// ALL is a special section that will be applied to all configurations:
[ALL]
// "include" corresponds to C++ > General > "Additional Include Directories":
// all paths are relative to project, i.e. they will have "$(SolutionDir)" automatically prepended
include =
    deps\include // note: indentation is important, otherwise configparser will not read it as a single line

// "libdir" corresponds to Linker > General > "Additional Library Directories":
libdir =
    deps\sdl\lib\x64

// "deps" corresponds to Linker > Input > "Additional Dependencies"
deps =
    SDL2.lib
    SDL2main.lib
    mylibrary.lib

// Specific configurations are named as [Configuration|Platform]
// Will be appended after all entries found in [ALL]
[Debug|x64]
libdir =
    deps\mylibrary\Debug

[Release|x64]
libdir =
    deps\mylibrary\Release
```

### How to use

1. Put the deplier.py and deps.ini into the folder where your .vcxproj is
2. Add your dependencies to deps.ini
3. Run depplier.py
4. You will get a message in terminal if the application was successful and any messages or errors that might've happened, hit any key to shut it down.

- In case the terminal just flashes, i.e. immediately shuts down without success message, there's a bug! Run it in command terminal to see the error message.

### Not tested

- Using it for personal use for now, so use at own risk. If you find an error, report it so I can fix it!
- If you have a suggestion for more features, contact me as well.
