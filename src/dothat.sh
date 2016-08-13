sleep 1m
python april.py
gst-launch v4l2src device=/dev/video0 ! queue ! videoscale ! video/x-raw-yuv,width=640,height=480 ! ffmpegcolorspace ! theoraenc ! queue ! oggmux name=m ! filesink location=output.ogv &
sleep 2s
echo | nc lab-machine 1234  &
sleep 1s
killall nc
sleep 30m
killall  gst-launch-0.10