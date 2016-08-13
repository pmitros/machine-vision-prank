nc -l 1234
aplay meeting.wav
gst-launch v4l2src  ! queue ! videoscale ! video/x-raw-yuv,width=640,height=480 ! ffmpegcolorspace ! theoraenc ! queue ! oggmux name=m ! filesink location=output.ogv alsasrc ! queue ! audioconvert ! vorbisenc ! m.&
sleep 30m
killall  gst-launch-0.10