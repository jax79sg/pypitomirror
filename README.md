# Prerequisite.

A running setup of bandersnatch (https://github.com/pypa/bandersnatch).
Bandersnatch's whitelisting is encouraged to be active

```
```
# Purpose of this module
When you used bandersnatch to download packages, they are primarily saved in 2 spots.
- First, a html named after the package is created in the 'simple' folder, this html will list the paths to the actual versioned packages
- Second, a series of indepth folders are created to store the actual version packages in the packaged folder.
If you just want to selectively take out some packages, it is humanely difficult due to the complex folder structure. 
This module is developed to handled the last point.

# How to use
 Assuming that you only need torch and torchvision, then run the following.
```python
extractpypi(['torch','torchvision'])
```

# How this works
- It will parse the selceted files downloaded by bandersnatch and then place it in a structure suitable for http mirror.
- packagelist refers to the packages desired 
- sourceIndex refers to the simple folder that contains the index.html
- sourcePackages refers to the packages folder that contains the actual library files.
