#! /bin/bash


#get help
#docker --help

# pull proteowizard
#docker pull chambm/pwiz-skyline-i-agree-to-the-vendor-licenses

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
