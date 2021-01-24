# Video stream with flask and trigger GPIO when someone watching


Based on the following tutorial [video streaming with Flask](http://blog.miguelgrinberg.com/post/video-streaming-with-flask) A python script to stream a webcam and activate a GPIO pin when this stream is watched.

# How to use

Start the flask app with following params:
```sh
FLASK_APP=path-to/app.py CAMERA=opencv flask run
```
The camera variable can be:
- opencv
- v4l2
- pi
