#! /usr/bin/bash

scriptpath=$(readlink -f "$0")
scriptroot=$(dirname "$scriptpath")

pushd $scriptroot

# footer

echo "    running rawmaker restruct oneline"

rawmaker -i restruct/restructuredtext.pdf\
         -o ./restruct\
         --prefix=oneline\
         --font\
         --text\
         --toc\
         --char_margin=100.0\
         --boxes_flow=1.0

echo "    running rawmaker restruct"

rawmaker -i restruct/restructuredtext.pdf\
         -o ./restruct\
         --border\
         --boxes\
         --font\
         --text\
         --toc\
         --char_margin=5.0\
         --boxes_flow=1.0\
         --line_margin=0.3

echo "    running sections restruct"

sections -i restruct/restructuredtext.pdf\
         -o ./restruct\
         --chapter\
         --index\
         --sections\
         --title\
         --toc\
         --whitepage

echo "    running words restruct"

words -i restruct\
       --headlines\
      --boxed\
      --list\
      --text\
      --words\
      -o ./restruct

popd
