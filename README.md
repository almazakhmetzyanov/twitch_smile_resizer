# twitch_smile_resizer
This is simple app for resizing 1 square image to twitch smile sizes(28x28, 56x56, 112x112)

# Has 2 api methods:
/tsr
Support only POST requests with square image in request(need send it with key 'file').
Returns link for prepared .zip file with resized images

/dwnld/<filename>
Support only GET requests with filename.
Returns .zip file with resized images
