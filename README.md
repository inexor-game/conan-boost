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

    ```cmake
    project(example)
    cmake_minimum_required(VERSION 2.8)
    set(CMAKE_MODULE_PATH ${CMAKE_CURRENT_BINARY_DIR})
    include(conanbuildinfo)
    conan_basic_setup()
    add_executable(example main.cpp)
    target_link_libraries(example ${CONAN_LIBS})
    ```

1. create out-of-source build directory

	```bash
    mkdir debug32
    ```

1. install packages

    ```bash
    cd debug32
    conan install .. --update --build missing -s build_type=Debug -s arch=x86
    ```

1. generate project file

    ```bash
    cd debug32
    cmake .. -G "Visual Studio 14 2015"
    ```
    or
    ```bash
    cd debug32
    cmake .. -G Xcode
    ```
    etc.

1. build the project

	```bash
    cd debug32
    cmake --build . --config Debug
    ```

## package specific options

|option                         |default|description|
|-------------------------------|-------|-----------|
|`Boost:shared`                 |`True` |If `True`, build dynamic link libraries. This option will be ignored when `header_only` is set to `True`.|
|`Boost:header_only`            |`False`|If `True`, install boost with header only mode.|
|`Boost:cxxdefines`             |       |`;` separated list of preprocessor macros. To define macro with value, escape `=` to `%3D`. ex) `Boost:cxxdefines="FOO;BAR%3D1"`|
|`Boost:cxxflags`               |       |Additional compile flags, separated with `;`. `=` should be escaped to `%3D`. ex) `Boost::cxxflags=--foo;--bar%3D1`. This option will be ignored when `header_only` is set to `True`.|
|`Boost:without_atomic`         |`False`|If `True`, exclude the library from build.|
|`Boost:without_chrono`         |`False`|&#12291;|
|`Boost:without_container`      |`False`|&#12291;|
|`Boost:without_context`        |`False`|&#12291;|
|`Boost:without_coroutine`      |`False`|&#12291;|
|`Boost:without_coroutine2`     |`False`|&#12291;|
|`Boost:without_date_time`      |`False`|&#12291;|
|`Boost:without_exception`      |`False`|&#12291;|
|`Boost:without_fiber`          |`False`|&#12291;|
|`Boost:without_filesystem`     |`False`|&#12291;|
|`Boost:without_graph`          |`False`|&#12291;|
|`Boost:without_graph_parallel` |`True`<sup>[1](#about_excluded_libs)</sup>|&#12291;|
|`Boost:without_iostreams`      |`False`|&#12291;|
|`Boost:without_locale`         |`False`|&#12291;|
|`Boost:without_log`            |`False`|&#12291;|
|`Boost:without_math`           |`False`|&#12291;|
|`Boost:without_metaparse`      |`False`|&#12291;|
|`Boost:without_mpi`            |`True`<sup>[1](#about_excluded_libs)</sup>|&#12291;|
|`Boost:without_program_options`|`False`|&#12291;|
|`Boost:without_python`         |`True`<sup>[1](#about_excluded_libs)</sup>|&#12291;|
|`Boost:without_random`         |`False`|&#12291;|
|`Boost:without_regex`          |`False`|&#12291;|
|`Boost:without_serialization`  |`False`|&#12291;|
|`Boost:without_signals`        |`False`|&#12291;|
|`Boost:without_system`         |`False`|&#12291;|
|`Boost:without_test`           |`False`|&#12291;|
|`Boost:without_thread`         |`False`|&#12291;|
|`Boost:without_timer`          |`False`|&#12291;|
|`Boost:without_type_erasure`   |`False`|&#12291;|
|`Boost:without_wave`           |`False`|&#12291;|

<a name="about_excluded_libs">1</a>: These libraries are excluded by default because they have external library dependecies such as python or mpi.
