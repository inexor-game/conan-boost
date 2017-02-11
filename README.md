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

|option                         |description                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |default|
|-------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------|
|`Boost:shared`                 |If `True`, build dynamic link libraries. This option will be ignored when `header_only` is set to `True`.                                                                            |`True` |
|`Boost:header_only`            |If `True`, install boost with header only mode.                                                                                                                                      |`False`|
|`Boost:cxxdefines`             |`;` separated list of preprocessor macros. To define macro with value, escape `=` to `%3D`. ex) `Boost:cxxdefines="FOO;BAR%3D1"`                                                     |       |
|`Boost:cxxflags`               |Additional compile flags, separated with `;`. `=` should be escaped to `%3D`. ex) `Boost::cxxflags=--foo;--bar%3D1`. This option will be ignored when `header_only` is set to `True`.|       |
|`Boost:without_atomic`         |If `True`, exclude the library from build.                                                                                                                                           |`False`|
|`Boost:without_chrono`         |&#12291;|`False`|
|`Boost:without_container`      |&#12291;|`False`|
|`Boost:without_context`        |&#12291;|`False`|
|`Boost:without_coroutine`      |&#12291;|`False`|
|`Boost:without_coroutine2`     |&#12291;|`False`|
|`Boost:without_date_time`      |&#12291;|`False`|
|`Boost:without_exception`      |&#12291;|`False`|
|`Boost:without_fiber`          |&#12291;|`False`|
|`Boost:without_filesystem`     |&#12291;|`False`|
|`Boost:without_graph`          |&#12291;|`False`|
|`Boost:without_graph_parallel` |&#12291;|`True`<sup>[1](#about_excluded_libs)</sup>|
|`Boost:without_iostreams`      |&#12291;|`False`|
|`Boost:without_locale`         |&#12291;|`False`|
|`Boost:without_log`            |&#12291;|`False`|
|`Boost:without_math`           |&#12291;|`False`|
|`Boost:without_metaparse`      |&#12291;|`False`|
|`Boost:without_mpi`            |&#12291;|`True`<sup>[1](#about_excluded_libs)</sup>|
|`Boost:without_program_options`|&#12291;|`False`|
|`Boost:without_python`         |&#12291;|`True`<sup>[1](#about_excluded_libs)</sup>|
|`Boost:without_random`         |&#12291;|`False`|
|`Boost:without_regex`          |&#12291;|`False`|
|`Boost:without_serialization`  |&#12291;|`False`|
|`Boost:without_signals`        |&#12291;|`False`|
|`Boost:without_system`         |&#12291;|`False`|
|`Boost:without_test`           |&#12291;|`False`|
|`Boost:without_thread`         |&#12291;|`False`|
|`Boost:without_timer`          |&#12291;|`False`|
|`Boost:without_type_erasure`   |&#12291;|`False`|
|`Boost:without_wave`           |&#12291;|`False`|

<a name="about_excluded_libs">1</a>: These libraries are excluded by default because they have external library dependecies such as python or mpi.
