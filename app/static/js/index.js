const video = document.getElementById('video');
const RATIO = 100000
var points=10*RATIO;

$(document).ready(function() {



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
    console.log(detections);
    var expression = detections[0]["expressions"];
    let max_key = Object.keys(expression).reduce(function(a, b){ return expression[a] > expression[b] ? a : b });
    console.log("Max Key = ",max_key)
    if (max_key ==='happy'){
      points = points - 0.05*RATIO
    }
    console.log(detections[0]["expressions"]);
  }, 100)
})



});

function send_data(){
  $.ajax({
    type: 'POST',
    url: '/save_details',
    data: JSON.stringify({'points':points}), // or JSON.stringify ({name: 'jonas'}),
    success: function(data) { 
        window.location = 'http://127.0.0.1:8000/end'
  
    },
    contentType: "application/json",
    dataType: 'json'
});
}