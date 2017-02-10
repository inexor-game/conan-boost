from conans import ConanFile
from conans import tools
import platform, os, sys, urllib


class BoostConan(ConanFile):
    name = "Boost"
    version = "1.63.0"
    description = "Boost provides free peer-reviewed portable C++ source libraries."
    license = "Boost Software License - Version 1.0. http://www.boost.org/LICENSE_1_0.txt"
    url = "https://github.com/kbinani/conan-boost/tree/develop/1.63.0"

    settings = "os", "arch", "compiler", "build_type"
    exports = ["FindBoost.cmake", "OriginalFindBoost*"]
    short_paths = True

    FOLDER_NAME = "boost_%s" % version.replace(".", "_")

    # This dict was automatically created with tool/construct_dependency_tree.sh
    LIB_DEPENDENCIES = {
        "atomic": ["atomic"],
        "chrono": ["chrono", "system"],
        "container": ["container"],
        "context": ["context"],
        "coroutine": ["chrono", "context", "coroutine", "system", "thread"],
        "coroutine2": ["context"],
        "date_time": ["date_time"],
        "exception": ["exception"],
        "fiber": ["context", "fiber"],
        "filesystem": ["filesystem", "system"],
        "graph": ["graph", "regex"],
        "graph_parallel": ["graph_parallel", "mpi", "serialization"],
        "iostreams": ["iostreams"],
        "locale": ["locale", "system"],
        "log": ["atomic", "chrono", "date_time", "filesystem", "log", "log_setup", "regex", "system", "thread"],
        "math": ["math_c99", "math_c99f", "math_c99l", "math_tr1", "math_tr1f", "math_tr1l"],
        "metaparse": ["chrono", "system", "timer", "unit_test_framework"],
        "mpi": ["mpi", "mpi_python", "python", "serialization"],
        "program_options": ["program_options"],
        "python": ["numpy", "python"],
        "random": ["random", "system"],
        "regex": ["regex"],
        "serialization": ["serialization", "wserialization"],
        "signals": ["signals"],
        "system": ["system"],
        "test": ["chrono", "prg_exec_monitor", "system", "test_exec_monitor", "timer", "unit_test_framework"],
        "thread": ["system", "thread"],
        "timer": ["chrono", "system", "timer"],
        "type_erasure": ["chrono", "system", "thread", "type_erasure"],
        "wave": ["chrono", "date_time", "filesystem", "system", "thread", "wave"],
    }

    # The current python option requires the package to be built locally, to find default Python implementation
    options = {
        "shared": [True, False],
        "header_only": [False, True],
        "fPIC": [False, True],
        "without_atomic": [False, True],
        "without_chrono": [False, True],
        "without_container": [False, True],
        "without_context": [False, True],
        "without_coroutine": [False, True],
        "without_coroutine2": [False, True],
        "without_date_time": [False, True],
        "without_exception": [False, True],
        "without_fiber": [False, True],
        "without_filesystem": [False, True],
        "without_graph": [False, True],
        "without_graph_parallel": [False, True],
        "without_iostreams": [False, True],
        "without_locale": [False, True],
        "without_log": [False, True],
        "without_math": [False, True],
        "without_metaparse": [False, True],
        "without_mpi": [False, True],
        "without_program_options": [False, True],
        "without_python": [False, True],
        "without_random": [False, True],
        "without_regex": [False, True],
        "without_serialization": [False, True],
        "without_signals": [False, True],
        "without_system": [False, True],
        "without_test": [False, True],
        "without_thread": [False, True],
        "without_timer": [False, True],
        "without_type_erasure": [False, True],
        "without_wave": [False, True],
        "cxxdefines": "ANY", # '=' should be urlencoded to %3D. example: -o cxxdefines="MACRO1;MACRO2%3D1"
        "cxxflags": "ANY", # '=' should be urlencoded to %3D. example: -o cxxflags="-Werror%3Duninitialized;-Wno-unknown-pragmas"
    }
    default_options = [(key, value[0]) for key, value in options.items() if isinstance(value, list)] \
                    + [(key, "") for key, value in options.items() if value == "ANY"]

    def config_options(self):
        """ First configuration step. Only settings are defined. Options can be removed
        according to these settings
        """
        if self._is_msvc():
            self.options.remove("fPIC")

    def configure(self):
        """ Second configuration step. Both settings and options have values, in this case
        we can force static library if MT was specified as runtime
        """
        if self._is_msvc() and \
           self.options.shared and "MT" in str(self.settings.compiler.runtime):
            self.options.shared = False

        if self.options.header_only:
            # Should be doable in package_id() but the UX is not ready
            self.options.remove("shared")
            self.options.remove("fPIC")
            self.options.without_python = True

        if not self.options.without_iostreams:
            if self.settings.os == "Linux" or self.settings.os == "Macos":
                self.requires("bzip2/1.0.6@lasote/stable")
                if not self.options.header_only:
                    self.options["bzip2/1.0.6"].shared = self.options.shared
            self.requires("zlib/1.2.8@lasote/stable")
            if not self.options.header_only:
                self.options["zlib"].shared = self.options.shared

    def package_id(self):
        """ if it is header only, the requirements, settings and options do not affect the package ID
        so they should be removed, so just 1 package for header only is generated, not one for each
        different compiler and option. This is the last step, after build, and package
        """
        if self.options.header_only:
            self.info.requires.clear()
            self.info.settings.clear()

    def source(self):
        zip_name = "%s.zip" % self.FOLDER_NAME if sys.platform == "win32" else "%s.tar.gz" % self.FOLDER_NAME
        url = "http://sourceforge.net/projects/boost/files/boost/%s/%s/download" % (self.version, zip_name)
        self.output.info("Downloading %s..." % url)
        tools.download(url, zip_name)
        tools.unzip(zip_name, ".")
        os.unlink(zip_name)

    def build(self):
        enabled_libs = [lib for lib, disable in self._without_options().items() if disable == False]
        if len(enabled_libs) == 0 and not self.options.header_only:
            raise Exception("All libs are disabled: consider using `-o header_only=True`" % enabled_libs)

        if self.options.header_only:
            self.output.warn("Header only package, skipping build")
            return
        command = "bootstrap" if self.settings.os == "Windows" else "./bootstrap.sh"
        if self.settings.os == "Windows" and self.settings.compiler == "gcc":
            command += " mingw"
        try:
            self.run("cd %s && %s" % (self.FOLDER_NAME, command))
        except:
            self.run("cd %s && type bootstrap.log" % self.FOLDER_NAME
                     if self.settings.os == "Windows"
                     else "cd %s && cat bootstrap.log" % self.FOLDER_NAME)
            raise

        flags = []

        flags.append('--user-config=user-config.jam')
        with open("%s/user-config.jam" % self.FOLDER_NAME, "w") as user_jam:
            if self.options.without_mpi == False or self.options.without_graph_parallel == False:
                user_jam.write("using mpi ;\n")

        if self._is_msvc():
            flags.append("toolset=msvc-%s.0" % self.settings.compiler.version)
        elif str(self.settings.compiler) in ["clang", "gcc"]:
            flags.append("toolset=%s"% self.settings.compiler)

        flags.append("link=%s" % ("static" if not self.options.shared else "shared"))
        if self.settings.compiler == "Visual Studio" and self.settings.compiler.runtime:
            flags.append("runtime-link=%s" % ("static" if "MT" in str(self.settings.compiler.runtime) else "shared"))
        flags.append("variant=%s" % str(self.settings.build_type).lower())
        flags.append("address-model=%s" % ("32" if self.settings.arch == "x86" else "64"))

        active_without_options = ["--without-%s" % lib.split("without_")[1] for lib, activated in self._without_options().items() if activated]
        flags += active_without_options

        cxx_flags = []

        if not self._is_msvc():
            # fPIC DEFINITION
            if self.options.fPIC:
                cxx_flags.append("-fPIC")

        # LIBCXX DEFINITION FOR BOOST B2
        try:
            if str(self.settings.compiler.libcxx) == "libstdc++":
                flags.append("define=_GLIBCXX_USE_CXX11_ABI=0")
            elif str(self.settings.compiler.libcxx) == "libstdc++11":
                flags.append("define=_GLIBCXX_USE_CXX11_ABI=1")
            if "clang" in str(self.settings.compiler):
                if str(self.settings.compiler.libcxx) == "libc++":
                    cxx_flags.append("-stdlib=libc++")
                    cxx_flags.append("-std=c++11")
                    flags.append('linkflags="-stdlib=libc++"')
                else:
                    cxx_flags.append("-stdlib=libstdc++")
                    cxx_flags.append("-std=c++11")
        except:
            pass

        if self.options.cxxdefines != "":
            flags.extend(["define=%s" % d for d in urllib.unquote(str(self.options.cxxdefines)).split(";")])

        if self.options.cxxflags != "":
            cxx_flags.extend(urllib.unquote(str(self.options.cxxflags)).split(";"))

        cxx_flags = 'cxxflags="%s"' % " ".join(cxx_flags) if cxx_flags else ""
        flags.append(cxx_flags)

        # JOIN ALL FLAGS
        b2_flags = " ".join(flags)

        command = "b2" if self.settings.os == "Windows" else "./b2"

        full_command = "cd %s && %s %s -j%s --abbreviate-paths" % (
            self.FOLDER_NAME,
            command,
            b2_flags,
            tools.cpu_count())
        self.output.warn(full_command)

        envs = self.prepare_deps_options_env()
        with tools.environment_append(envs):
            self.run(full_command)

    def prepare_deps_options_env(self):
        ret = {}
#         if self.settings.os == "Linux" and "bzip2" in self.requires:
#             include_path = self.deps_cpp_info["bzip2"].include_paths[0]
#             lib_path = self.deps_cpp_info["bzip2"].lib_paths[0]
#             lib_name = self.deps_cpp_info["bzip2"].libs[0]
#             ret["BZIP2_BINARY"] = lib_name
#             ret["BZIP2_INCLUDE"] = include_path
#             ret["BZIP2_LIBPATH"] = lib_path

        return ret

    def package(self):
        # Copy findZLIB.cmake to package
        self.copy("FindBoost.cmake", ".", ".")
        self.copy("OriginalFindBoost*", ".", ".")

        self.copy(pattern="*", dst="include/boost", src="%s/boost" % self.FOLDER_NAME)
        self.copy(pattern="*.a", dst="lib", src="%s/stage/lib" % self.FOLDER_NAME)
        self.copy(pattern="*.so", dst="lib", src="%s/stage/lib" % self.FOLDER_NAME)
        self.copy(pattern="*.so.*", dst="lib", src="%s/stage/lib" % self.FOLDER_NAME)
        self.copy(pattern="*.dylib*", dst="lib", src="%s/stage/lib" % self.FOLDER_NAME)
        self.copy(pattern="*.lib", dst="lib", src="%s/stage/lib" % self.FOLDER_NAME)
        self.copy(pattern="*.dll", dst="bin", src="%s/stage/lib" % self.FOLDER_NAME)

    def package_info(self):
        if not self.options.header_only and self.options.shared:
            self.cpp_info.defines.append("BOOST_ALL_DYN_LINK")
        else:
            self.cpp_info.defines.append("BOOST_USE_STATIC_LIBS")

        if self.options.header_only:
            return

        if not self.options.without_python and not self.options.shared:
            self.cpp_info.defines.append("BOOST_PYTHON_STATIC_LIB")

        if self.options.cxxdefines != "":
            self.cpp_info.defines.extend(str(self.options.cxxdefines).split(";"))

        enabled_libs = [lib.split("without_")[1] for lib, disable in self._without_options().items() if disable == False]
        libs_created = []
        for lib in enabled_libs:
            if lib in self.LIB_DEPENDENCIES:
                libs_created += self.LIB_DEPENDENCIES[lib]

        self.cpp_info.libs.extend([self._linkname(lib) for lib in libs_created])

        if self._is_msvc():
            # DISABLES AUTO LINKING! NO SMART AND MAGIC DECISIONS THANKS!
            self.cpp_info.defines.extend(["BOOST_ALL_NO_LIB"])

    def _options(self):
        option_values = self.options.values.as_list()
        return dict([(k, v) for k, v in option_values])

    def _without_options(self):
        return dict([(lib, disable) for lib, disable in self._options().items() if lib.startswith("without_")])

    def _linkname(self, lib):
        if self._is_msvc():
            # http://www.boost.org/doc/libs/1_55_0/more/getting_started/windows.html
            visual_version = int(str(self.settings.compiler.version)) * 10
            threading = "mt"

            abi_tags = []
            if self.settings.compiler.runtime in ("MTd", "MT"):
                abi_tags.append("s")

            if self.settings.build_type == "Debug":
                abi_tags.append("gd")

            abi_tags = ("-%s" % "".join(abi_tags)) if abi_tags else ""

            version = "_".join(self.version.split(".")[0:2])
            suffix = "vc%d-%s%s-%s" %  (visual_version, threading, abi_tags, version)
            prefix = "" if self.options.shared else "lib"

            if lib in ("exception", "test_exec_monitor"):
                # These libraries have always 'lib' prefix
                win_libs.append("libboost_%s-%s" % (lib, suffix))
            else:
                win_libs.append("%sboost_%s-%s" % (prefix, lib, suffix))
        else:
            libname_template = "boost_%s" if self.options.shared else "libboost_%s.a"
            return libname_template % lib

    def _is_msvc(self):
        return self.settings.compiler == "Visual Studio"
