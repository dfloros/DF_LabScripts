#! /bin/bash
# file 


#get help
#docker --help

# pull proteowizard
if [ "$1" = "pull" ]
then
    docker pull \
    chambm/pwiz-skyline-i-agree-to-the-vendor-licenses
    exit 0
fi
#run ms convert
#$@ passes all cmdline arguments through to msconvert
#use --help for help

if [ "$1" = "-h" ]
then
    docker run -it --rm \
    chambm/pwiz-skyline-i-agree-to-the-vendor-licenses wine \
    msconvert --help
else
    docker run -it --rm -e WINEDEBUG=-all -v /your/data:/data \
    chambm/pwiz-skyline-i-agree-to-the-vendor-licenses \
    wine msconvert $@
fi

##mv *.mzml *_mzmls