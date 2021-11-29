const video = document.getElementById('video');
const RATIO = 100000;
var points=10*RATIO;
var loading = 1;

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
      $('#score_maintainer').html('SCORE='+points)
      if(points>900000){
        $('#score_maintainer').css("color","green");
      }
      else if(points>500000){
        $('#score_maintainer').css("color","orange");
      }
      else{
        $('#score_maintainer').css("color","red");
      }

    }
    if(loading===1)
    {
      $('#start_stop_message').html('You can start the Video now');
      $('#start_stop_message').css("color","green");
      $('#score_maintainer').html('SCORE='+points)
      loading=0
    }
    console.log(detections[0]["expressions"]);
  }, 100)
})



});

function send_data(userID,gameID){
  $.ajax({
    type: 'POST',
    url: '/save_details',
    data: JSON.stringify({'points':points,'game':gameID,'user':userID}), // or JSON.stringify ({name: 'jonas'}),
    success: function(data) { 
        window.location = 'http://127.0.0.1:8000/end/'+gameID+'/'+userID
  
    },
    contentType: "application/json",
    dataType: 'json'
});
}