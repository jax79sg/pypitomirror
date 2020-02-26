# Purpose of this module
# When you used bandersnatch to download packages, they are primarily saved in 2 spots.
# First, a html named after the package is created in the 'simple' folder, this html will list the paths to the actual versioned packages
# Second, a series of indepth folders are created to store the actual version packages in the packaged folder.
# If you just want to selectively take out some packages, it is humanely difficult due to the complex folder structure. 
# This module is developed to handled the last point.

# How to use
# Assuming that you only need torch and torchvision, then run the following.
# extractpypi(['torch','torchvision'],ssh="user/password/123.22.112.2") 
```
import os
import tqdm
import shutil

def extractpypi(packagelist=[], sourceIndex='/mnt/1a216e0c-9bdc-44ac-8f89-bf2cb3efcfd8/repos/pypi6/web/simple/', sourcePackages='/mnt/1a216e0c-9bdc-44ac-8f89-bf2cb3efcfd8/repos/pypi6/web/packages/', dest='/media/user/BIG_WHITE_4/pypi6', ssh=None):
    with tqdm.tqdm(total=len(packagelist)) as pbar:
        for package in packagelist:
            listOfPackages=processIndexHtmls(package, sourceIndex, dest, ssh=ssh)
            processPackages(listOfPackages,sourcePackages, dest, ssh=ssh)
            pbar.update()

def processIndexHtmls(package, sourceIndex, dest, ssh):
    #Copy it to dest
    indexpath=sourceIndex+package
    indexhtml=sourceIndex+package+'/index.html'
    if (ssh is not None):
        user=ssh.split("/")[0]
        password=ssh.split("/")[1]
        host==ssh.split("/")[2]
        import subprocess
        subprocess.run(["scp", indexpath, user+"@"+host+":"+dest+'/simple/'+package])
#         subprocess.run(["scp", "foo.bar", "joe@srvr.net:/path/to/foo.bar"])
    else:
        try:
            result = shutil.copytree(indexpath, dest+'/simple/'+package)
            # print("Copy completed in {}".format(result))
        except FileExistsError:
            print("File {} exists, skip!".format(dest+'/simple/'+package))


    #Get the index.html
    from bs4 import BeautifulSoup
    htmlfile = open(indexhtml, 'r')
    soup = BeautifulSoup(htmlfile, 'html.parser')


    #Get all the packages links
    packagesLinks=[]
    for a in soup.find_all('a', href=True):
        # print("Found the URL:", a['href'].split("#")[0].split("packages/")[1])
        packagesLinks.append(a['href'].split("#")[0].  split("packages/")[1])

    return packagesLinks


def processPackages(listOfPackages,sourcePackages, dest, ssh=None):
    #Copy the entire path of packges into dest
    for package in listOfPackages:
        subDir = package.split("/")
        subDir=subDir[:-1]
        currentDir=dest + '/packages'
        
        if (ssh is not None):
            user=ssh.split("/")[0]
            password=ssh.split("/")[1]
            host==ssh.split("/")[2]
            import subprocess
            subprocess.run(["scp", sourcePackages+package, user+"@"+host+":"+dest + '/packages/'+package])
        else:        
            try:
                os.mkdir(currentDir)
            except FileExistsError:
                pass

            for dir in subDir:
                currentDir=currentDir+"/"+dir
                try:
                    os.mkdir(currentDir)
                except FileExistsError:
                    pass
            result = shutil.copy(sourcePackages+package, dest + '/packages/'+package)
            print("Copy completed in {}".format(result))
    pass

extractpypi(['torch','torchvision'])
