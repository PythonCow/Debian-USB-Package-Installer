#! /usr/bin/python
#Small script to find the names of all installed packages and put
#them in package_names.txt.
import os

assert os.name == "posix" #You should be running Debian or something close to it.

os.system("dpkg-query -l > packages.txt")

packages_to_read = open("packages.txt", "r")
text = packages_to_read.readlines()
packages_to_read.close()
packages = []

for line in text:
    package_name = []
    if line[:2:] == "ii" or line[:2:] == "rc":
        for char in line[4::]:
            if char == " " or char == ":":
                break
            package_name.append(char)
        packages.append(''.join(package_name))

#print packages
package_names_file = open("package_names.txt", "w")
package_names_file.write("")
package_names_file.close()
package_names_file = open("package_names.txt", "a")
for name in packages:
	package_names_file.write(name + "\n")
package_names_file.close()
print "Finished."
