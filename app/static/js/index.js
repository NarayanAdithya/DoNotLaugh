const video = document.getElementById('video');

var socket = io.connect('http://127.0.0.1:5000/');
socket.on( 'connect', function() {
  console.log("SOCKET CONNECTED")
})

navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia || navigator.msGetUserMedia;
Promise.all([
  faceapi.loadFaceLandmarkModel("../../static/models/face_landmark_68_model-weights_manifest.json"),
  faceapi.loadFaceRecognitionModel("../../static/models/face_recognition_model-weights_manifest.json"),
  faceapi.loadTinyFaceDetectorModel("../../static/models/tiny_face_detector_model-weights_manifest.json"),
  faceapi.loadFaceLandmarkTinyModel("../../static/models/face_landmark_68_tiny_model-weights_manifest.json"),
  faceapi.loadFaceExpressionModel("../../static/models/face_expression_model-weights_manifest.json"),
])
  .then(startVideo)
  .catch(err => console.error(err));

function startVideo() {
  console.log("access");
  navigator.getUserMedia(
    {
      video: {}
    },
    stream => video.srcObject = stream,
    err => console.error(err)
  )
}

video.addEventListener('play', () => {
  // console.log('thiru');


  setInterval(async () => {
    const detections = await faceapi
      .detectAllFaces(video, new faceapi.TinyFaceDetectorOptions())
      .withFaceLandmarks()
      .withFaceExpressions();
    console.log(detections)
    socket.emit( 'my event', {
      data: detections,
      game: '{{game}}',
    })
    console.log(detections);
  }, 100)
})
