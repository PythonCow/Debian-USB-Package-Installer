import os

usb_dir = os.getcwd()

os.chdir("repository/binary")
#Make Packages.gz file.
os.system("dpkg-scanpackages . > Packages")
os.system("gzip Packages")
os.chdir("/etc/apt")
#Just in case, make a copy.
os.system("cp sources.list ~/copy_of_sources.list")
os.system("apt-cdrom -d "+usb_dir+"/repository add")

os.system("apt-get update")
print "Now use apt-get install [package-name] to install."



