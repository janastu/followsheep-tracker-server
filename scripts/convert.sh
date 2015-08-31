cd $1
if command -v avconv 2> /dev/null; then
    for i in *.3gpp ; do
        avconv -i "$i" -codec:a libmp3lame -qscale:a 2 $(basename $i).mp3 > /dev/null & 2> /dev/null
        echo "converted $i"
    done
else
    for i in *.3gpp ; do
        ffmpeg -i "$i" -codec:a libmp3lame -qscale:a 2 $(basename $i).mp3 > /dev/null & 2> /dev/null
        echo "converted $i"
    done
fi
