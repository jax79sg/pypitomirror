
import os
import tqdm
import shutil
import os.path

def extractpypi(packagelist=[], sourceIndex='/mnt/1a216e0c-9bdc-44ac-8f89-bf2cb3efcfd8/repos/pypi4/web/simple/', sourcePackages='/mnt/1a216e0c-9bdc-44ac-8f89-bf2cb3efcfd8/repos/pypi4/web/packages/', dest='/media/user/BIG_WHITE_4/stuff'):
    with tqdm.tqdm(total=len(packagelist)) as pbar:
        for package in packagelist:
            listOfPackages=processIndexHtmls(package, sourceIndex, dest)
            processPackages(listOfPackages,sourcePackages, dest)
            pbar.update()

def processIndexHtmls(package, sourceIndex, dest):
    #Copy it to dest
    indexpath=sourceIndex+package
    indexhtml=sourceIndex+package+'/index.html'
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
        packagesLinks.append(a['href'].split("#")[0].split("packages/")[1])

    return packagesLinks


def processPackages(listOfPackages,sourcePackages, dest):
    #Copy the entire path of packges into dest
    for package in listOfPackages:
        subDir = package.split("/")
        subDir=subDir[:-1]
        currentDir=dest + '/packages'
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
        if not os.path.isfile(dest + '/packages/'+package):
            result = shutil.copy(sourcePackages+package, dest + '/packages/'+package)
            print("Copy completed in {}".format(result))
    pass

extractpypi([
     'virtualenv',
             ])