#! /usr/bin/python
from HTMLParser import HTMLParser
import string

#Class that finds dependencies of a Package when fed URL from Debian Packages site.
class Dependency_finder(HTMLParser):
    def __init__(self, past_dependencies=[]):
        HTMLParser.__init__(self)
        self.past_dependencies = past_dependencies
        #dependencies is a dictionary where the key is the link to the dependency and the value is the name.
        self.dependencies = {}
        self.dt = False
        self.dep = False
        self.link = False
    def handle_starttag(self, tag, attrs):
        if tag == "dt":
            self.dt = True
            self.dep = False
        elif tag == "a" and self.dep:
            self.link = True
            self.dependencies[attrs[0][1]] = "If you see this, there was probably a bug."
            self.newest_link = attrs[0][1]
            self.dt = False
        elif tag != "span" and self.dep:
            self.dep = False
            
            
    def handle_data(self, data):
        if self.dt:
            if data == "dep:":
                self.dep = True
                self.dt = False
        elif self.link:
            #If data is in self.past_dependencies, remove corresponding key and value from dependencies.
            if not [i for i in self.past_dependencies if compare_package_names(i, data)] == []:
                new_dependencies = {i: self.dependencies[i] for i in self.dependencies if i != self.newest_link}
                del self.dependencies
                self.dependencies = new_dependencies
            else:
                self.dependencies[self.newest_link] = data
            self.link = False

#Takes two strings and sees if they are close enough to be the same package.
def compare_package_names(pkg1, pkg2):
    return [i for i in pkg1 if i in string.lowercase or i == "-"] == [i for i in pkg2 if i in string.lowercase or i == "-"]

if __name__ == "__main__":

    import urllib
    find_depends = Dependency_finder(["make"])
    html_to_parse = urllib.urlretrieve("https://packages.debian.org/stable/alien", "alien.html")
    data = open("alien.html", "r").read()
    find_depends.feed(data)
    print find_depends.dependencies
    
    
