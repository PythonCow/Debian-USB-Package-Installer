from find_all_dependencies import *
from HTMLParser import HTMLParser
import urllib2
from ftplib import FTP
import re
import os

def ftp_download(url, filename, directory, chunk_size=1024):
    file_to_write = open(directory+filename, "wb")
    r = FTP("ftp.us.debian.org")
    r.login()
    r.cwd("/")
    r.cwd(url)
    print "Downloading..."
    r.retrbinary('RETR ' + filename, file_to_write.write, chunk_size)
    print "Download complete."
    return

class find_file_name(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.h2tag = False
        self.link_found = False
        self.link = ""
        
    def handle_starttag(self, tag, attrs):
        if tag == "h2":
            self.h2tag = True
        elif tag == "kbd" and self.h2tag:
            self.link_found = True
            self.h2tag = False
    def handle_data(self, data):
        if self.link_found:
            print data
            self.link = data
            self.link_found = False

class find_ftp_location(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.ptag = False
        self.tttag = False
        self.ftp_location = ""

    def handle_starttag(self, tag, attrs):
        if tag == 'p':
            self.ptag = True
        if self.ptag == True and tag == 'tt':
            self.tttag = True
            self.ptag = False
    def handle_data(self, data):
        if self.tttag == True:
            self.ftp_location = data
    def handle_endtag(self, tag):
        if tag == 'p':
            self.ptag = False
        if tag == 'tt':
            self.tttag = False

if not os.path.exists("repository"):
    os.mkdir("repository")
if not os.path.exists("repository/binary"):
    os.mkdir("repository/binary")

architechures = ["i386", "amd64", "powerpc", "armhf"]

package_to_install = raw_input("What is the name of the package you want?\n")

arch_to_install_for = input("""Enter number of desired architechure:
[0]: i386
[1]: amd64
[2]: powerpc
[3]: armhf
""")
assert isinstance(arch_to_install_for, (int, long))
arch = architechures[arch_to_install_for]

past_deps = find_installed()
print "Finding dependencies (this may take a while)."
deps = find_deps_for_package(package_to_install, past_deps)

print "Downloading Packages."

for value in deps.values():
    print value
    if "-base" in value:
        new_value = value[:len(value)-5:]
        print new_value
    else:
        new_value = value
    try:
        html_to_parse = urllib2.urlopen("https://packages.debian.org/jessie/"+arch+"/"+value+"/download")
        data = html_to_parse.read()
        html_to_parse.close()
        file_name = find_file_name()
        file_name.feed(data)
        link = file_name.link
        print link
        ftp_location = find_ftp_location()
        ftp_location.feed(data)
        location = ftp_location.ftp_location
        download_url = "debian/"+location
        print download_url
        ftp_download( download_url, link, "repository/binary/")
    except urllib2.HTTPError:
        try:
            html_to_parse = urllib2.urlopen("https://packages.debian.org/jessie/a/"+value+"/download")
            data = html_to_parse.read()
            html_to_parse.close()
            file_name = find_file_name()
            file_name.feed(data)
            link = file_name.link
            print link
            ftp_location = find_ftp_location()
            ftp_location.feed(data)
            location = ftp_location.ftp_location
            download_url = "debian/"+location
            print download_url
            ftp_download( download_url, link, "repository/binary/")
        except urllib2.HTTPError:
            print "Some information you entered must be incorrect."

print "Download completed."
    



