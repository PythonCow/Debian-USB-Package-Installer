from find_dependencies_debian import *
import urllib2
import os.path
#Code for finding all dependencies of a Debian package.

#Recursive function for finding all dependencies.
#Returns a dictionary where the keys are the links to the dependencies and the values are the names.
def find_deps_for_package(package, past_deps = []):
    dependencies = {}
    find_deps = Dependency_finder(past_deps)
    html_to_parse = urllib2.urlopen("https://packages.debian.org/stable/"+package, "tmp.html")
    data = html_to_parse.read()
    find_deps.feed(data)
    new_deps = dependencies.copy()
    new_deps.update(find_deps.dependencies)
    del dependencies
    dependencies = new_deps.copy()
    html_to_parse.close()
    past_deps = past_deps+dependencies.values()
    for package in dependencies.values():
        new_deps = dependencies.copy()
        new_deps.update(find_deps_for_package(package, past_deps))
        del dependencies
        dependencies = new_deps.copy()
        past_deps = past_deps+dependencies.values()
    return dependencies

#Returns a list of all package names. Only works if package_names.py has been run previously.
def find_installed():
    if not os.path.exists("package_names.txt"):
        print "It looks like you haven't run package_names.py. If you only want to download files you need, you should run that first."
        return []
    package_names_file = open("package_names.txt", "r")
    package_names = package_names_file.readlines()
    for line in range(len(package_names)):
        package_names[line] = package_names[line].strip('\n')
    return package_names

if __name__ == "__main__":
    package_names = find_installed()
    print find_deps_for_package("alien", package_names)

    
    
    
    
