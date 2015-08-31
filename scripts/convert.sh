# !/usr/bin/env bash
cd $1
for i in *.3gpp ; do
    ffmpeg -i "$i" -codec:a libmp3lame -qscale:a 2 $(basename $i).mp3 > /dev/null & 2> /dev/null
    echo "converted $i"
done
