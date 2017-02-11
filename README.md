[![Build Status](https://travis-ci.org/kbinani/conan-boost.svg?branch=testing/1.63.0)](https://travis-ci.org/kbinani/conan-boost)

# conan-boost

[![badge](https://img.shields.io/badge/conan.io-Boost%2F1.63.0-green.svg?logo=data:image/png;base64%2CiVBORw0KGgoAAAANSUhEUgAAAA4AAAAOCAMAAAAolt3jAAAA1VBMVEUAAABhlctjlstkl8tlmMtlmMxlmcxmmcxnmsxpnMxpnM1qnc1sn85voM91oM11oc1xotB2oc56pNF6pNJ2ptJ8ptJ8ptN9ptN8p9N5qNJ9p9N9p9R8qtOBqdSAqtOAqtR%2BrNSCrNJ/rdWDrNWCsNWCsNaJs9eLs9iRvNuVvdyVv9yXwd2Zwt6axN6dxt%2Bfx%2BChyeGiyuGjyuCjyuGly%2BGlzOKmzOGozuKoz%2BKqz%2BOq0OOv1OWw1OWw1eWx1eWy1uay1%2Baz1%2Baz1%2Bez2Oe02Oe12ee22ujUGwH3AAAAAXRSTlMAQObYZgAAAAFiS0dEAIgFHUgAAAAJcEhZcwAACxMAAAsTAQCanBgAAAAHdElNRQfgBQkREyOxFIh/AAAAiklEQVQI12NgAAMbOwY4sLZ2NtQ1coVKWNvoc/Eq8XDr2wB5Ig62ekza9vaOqpK2TpoMzOxaFtwqZua2Bm4makIM7OzMAjoaCqYuxooSUqJALjs7o4yVpbowvzSUy87KqSwmxQfnsrPISyFzWeWAXCkpMaBVIC4bmCsOdgiUKwh3JojLgAQ4ZCE0AMm2D29tZwe6AAAAAElFTkSuQmCC)](http://www.conan.io/source/Boost/1.63.0/kbinani/develop)

[Conan.io](https://conan.io) package for boost library

The packages generated with this **conanfile** can be found in [conan.io](https://conan.io/source/Boost/1.63.0/kbinani/develop).

## dependencies

* conan [Conan.io](https://conan.io)
* cmake
* modern C++ compiler (Xcode, Visual Studio, etc.)

## example

Here is an example how to build a project with `conan-boost`.

1. write a `conanfile.txt`
    
    ```
    [requires]
    Boost/1.63.0@kbinani/develop

    [options]
    Boost:shared=true # false
    # write custom options here. see `package specific options` section for detail

    [generators]
    cmake
    ```

1. write a `CMakeLists.txt`

    ```
    project(example)
    cmake_minimum_required(VERSION 2.8)
    set(CMAKE_MODULE_PATH ${CMAKE_CURRENT_BINARY_DIR})
    include(conanbuildinfo)
    conan_basic_setup()
    add_executable(example main.cpp)
    target_link_libraries(example ${CONAN_LIBS})
    ```

1. create out-of-source build directory

	```
    mkdir debug32
    ```

1. install packages

    ```
    cd debug32
    conan install .. --update --build missing -s build_type=Debug -s arch=x86
    ```

1. generate project file

    ```
    cd debug32
    cmake .. -G "Visual Studio 14 2015"
    ```
    or
    ```
    cd debug32
    cmake .. -G Xcode
    ```
    etc.

1. build the project

	```
    cd debug32
    cmake --build . --config Debug
    ```

## package specific options

|option                |description                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |default|
|----------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------|
|`Boost:shared`        |if `True`, build dynamic link libraries. This option will be ignored when `header_only` is set to `True`.                                                                                                                                                                                                                                                                                                                                                                        |`True` |
|`Boost:header_only`   |if `True`, install boost with header only mode.                                                                                                                                                                                                                                                                                                                                                                                                                                  |`False`|
|`Boost:cxxdefines`    |`;` separated list of preprocessor macros. To define macro with value, escape `=` to `%3D`. ex) `Boost:cxxdefines="FOO;BAR%3D1"`                                                                                                                                                                                                                                                                                                                                                 |       |
|`Boost:cxxflags`      |Additional compile flags, separated with `;`. `=` should be escaped to `%3D`. ex) `Boost::cxxflags=--foo;--bar%3D1`. This option will be ignored when `header_only` is set to `True`.                                                                                                                                                                                                                                                                                            |       |
|`Boost:without_{name}`|Exclude library `{name}` from build. This option will be ignored when `header_only` is set to `True`. `{name}` should be `atomic`, `chrono`, `container`, `context`, `coroutine`, `coroutine2`, `date_time`, `exception`, `fiber`, `filesystem`, `graph`, `graph_parallel`, `iostreams`, `locale`, `log`, `math`, `metaparse`, `mpi`, `program_options`, `python`, `random`, `regex`, `serialization`, `signals`, `system`, `test`, `thread`, `timer`, `type_erasure`, or `wave`.|`False`|
