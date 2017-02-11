import os, re, subprocess, sys, shutil


DEBUG = False

def root_directory():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

def boost_version():
    path = os.path.join(root_directory(), 'conanfile.py')
    pattern = re.compile(r"^[0-9.]*$")
    with open(path, "r") as conanfile:
        for line in conanfile.readlines():
            tokens = line.strip().split("=")
            if len(tokens) != 2:
                continue
            key = tokens[0].strip(' "\n\t')
            value = tokens[1].strip(' "\n\t')
            if key != "version":
                continue
            if pattern.match(value):
                return value
    raise Exception("Cannot detect boost version")

def clean():
    d = root_directory()
    version = boost_version()
    folder_name = "boost_%s" % (version.replace('.', '_'))
    rootdir = os.path.join(d, folder_name)
    for file in ["conanbuildinfo.txt", "conaninfo.txt", "conanenv.txt"]:
        f = os.path.join(d, file)
        if os.path.isfile(f):
            os.unlink(f)

    for dir in ["bin.v2", "stage/lib", "project-config.jam", "user-config.jam"]:
        target = os.path.join(rootdir, dir)
        count = 0
        max_count = 1000
        while True:
            try:
                if os.path.isdir(target):
                    shutil.rmtree(target)
                elif os.path.isfile(target):
                    os.unlink(target)
                break
            except Exception as e:
                count += 1
                if DEBUG:
                    print(e)
                if max_count < count:
                    if not DEBUG:
                        print(e)
                    raise
                continue

def build_only(all_libs, lib, dependencies_txt, options_txt):
    print(lib)
    dependencies_txt.write("        \"%s\": [" % lib)
    dependencies_txt.flush()

    m = None
    if sys.platform == "win32":
        m = re.compile(r"^(lib)?boost_([^\-]*).*lib$")
    elif sys.platform == "darwin":
        m = re.compile(r"^(lib)?boost_([^\-]*)\.a$")

    d = root_directory()
    version = boost_version()
    folder_name = "boost_%s" % (version.replace('.', '_'))

    clean()

    args_str = "conan install -g env -o shared=False "
    args_str += " ".join(["-o without_%s=%s" % (l, l != lib) for l in all_libs])
    args = args_str.split(" ")
    p = subprocess.Popen(args=args, cwd=d, stdout=subprocess.PIPE)
    p.communicate()

    if DEBUG:
        p = subprocess.Popen(args=["conan", "build"], cwd=d)
        p.wait()
    else:
        p = subprocess.Popen(args=["conan", "build"], cwd=d, stdout=subprocess.PIPE)
        p.communicate()

    product_files = []
    try:
        product_files = os.listdir(os.path.join(d, folder_name, 'stage', 'lib'))
    except:
        pass
    product_libs = []
    for p in product_files:
        print("  %s" % p)
        match = m.match(p)
        if match:
            product_libs.append(match.group(2))
    sys.stdout.flush()

    product_libs.sort()

    dependencies_txt.write("\"%s\"],\n" % ('", "'.join(product_libs)))
    dependencies_txt.flush()

    default_excluded_libs = ["python", "mpi", "graph_parallel"]
    default_excluded = lib in default_excluded_libs
    options_txt.write("        \"without_%s\": [%s],\n" % (lib, "True, False" if default_excluded else "False, True"))
    options_txt.flush()

if __name__ == "__main__":
    version = boost_version()
    folder_name = "boost_%s" % (version.replace('.', '_'))
    rootdir = os.path.join(root_directory(), folder_name)

    # Download boost tarball by `conan source`.
    if not os.path.isdir(rootdir):
        p = subprocess.Popen(args=["conan", "source"], cwd=root_directory())
        p.wait()

    # Build Boost.Build if `b2` doesn't exist.
    is_win = sys.platform == "win32"
    b2exe = os.path.join(os.path.join(rootdir, "b2.exe" if is_win else "b2"))
    if not os.path.isfile(b2exe):
        if is_win:
            p = subprocess.Popen(args=["cmd", "/c", "call bootstrap.bat"], cwd=rootdir)
            p.wait()
        else:
            p = subprocess.Popen(args=['./bootstrap.sh'], cwd=rootdir)
            p.wait()

    # Get list of buildable libs by `b2 --show-libraries`
    p = subprocess.Popen(args=[b2exe, '--show-libraries'], cwd=rootdir, stdout=subprocess.PIPE)
    (stdout, _) = p.communicate()
    all_libs = [line.strip().split('-')[1].strip() for line in stdout.split("\n") if line.strip().startswith("-")]
    libs = [] + all_libs
    # libs = ["locale"] # Uncomment this line to make options for specific library.

    with open("dpendencies_%s.txt" % sys.platform, "w") as dependencies_txt:
        with open("options_%s.txt" % sys.platform, "w") as options_txt:
            dependencies_txt.write("    LIB_DEPENDENCIES = {\n")
            options_txt.write("    options = {\n")
            options_txt.write("        \"shared\": [True, False],\n")
            options_txt.write("        \"header_only\": [False, True],\n")
            options_txt.write("        \"cxxdefines\": \"ANY\",\n")
            options_txt.write("        \"cxxflags\": \"ANY\",\n")
            for lib in libs:
                build_only(all_libs, lib, dependencies_txt, options_txt)
            dependencies_txt.write("    }\n")
            options_txt.write("    }\n")

    clean()
