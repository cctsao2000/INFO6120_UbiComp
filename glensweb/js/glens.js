function readingSpeedCalibration() {
    var message = "Reading Speed Calibration: After clicking 'OK', You'll see a short paragraph, please read it at your normal speed. Once you have done reading the paragraph, click 'OK' again.";
    var result = window.confirm(message);
    if (result) {
        var startTime = new Date();
        alert("This is a reading speed calibration of the Glens. We kindly ask you to take a moment to read this paragraph at your normal reading speed. Once you have finished reading, please click the 'OK' button to proceed. Your reading speed will assist us in refining the Glens performance and contribute to enhancing future interactions. Thank you for your participation in this calibration exercise.");
        var endTime = new Date();
    } else {
        readingSpeedCalibration();
    }
    return endTime - startTime;
}
var baseline = readingSpeedCalibration();
var readingTimeList = {"p1":0, "p2":0, "p3":0, "p4":0, "p5":0, "p6":0, "p7":0, "p8":0, "p9":0};

function getReadingTimeColor(pid, baseline) {
    var baselineSpeed = baseline / 389;
    var readingTime = readingTimeList[pid]*100;
    var readingSpeed = readingTime / document.getElementById(pid).textContent.length;
    console.log(readingSpeed, baselineSpeed);
    if (readingSpeed < (baselineSpeed*0.3)){
        return "dot";
    } else if (readingSpeed < (baselineSpeed*2)) {
        return "dot green";
    } else if (readingSpeed < (baselineSpeed*3.5)) {
        return "dot yellow";
    } else if (readingSpeed < (baselineSpeed*5)) {
        return "dot orange";
    } else {
        return "dot red";
    };
}

webgazer.setGazeListener(function(data, elapsedTime) {
    if (data == null) {
      return;
    }
    var x_prediction = data.x; //these x coordinates are relative to the viewport
    var y_prediction = data.y; //these y coordinates are relative to the viewport
    var elementLooking = document.elementFromPoint(x_prediction, y_prediction);
    try {
        if (elementLooking.tagName == "P") {
            readingTimeList[elementLooking.id]++;
            console.log(readingTimeList[elementLooking.id]);
        }
    } catch (error) {
        // pass
    }
    // var readingTimeSum = Object.values(readingTimeList).reduce((a, b) => a + b, 0);
    var dot1 = document.getElementById("d1");
    dot1.className = getReadingTimeColor("p1", baseline);
    var dot2 = document.getElementById("d2");
    dot2.className = getReadingTimeColor("p2", baseline);
    var dot3 = document.getElementById("d3");
    dot3.className = getReadingTimeColor("p3", baseline);
    var dot4 = document.getElementById("d4");
    dot4.className = getReadingTimeColor("p4", baseline);
    var dot5 = document.getElementById("d5");
    dot5.className = getReadingTimeColor("p5", baseline);
    var dot6 = document.getElementById("d6");
    dot6.className = getReadingTimeColor("p6", baseline);
    var dot7 = document.getElementById("d7");
    dot7.className = getReadingTimeColor("p7", baseline);
    var dot8 = document.getElementById("d8");
    dot8.className = getReadingTimeColor("p8", baseline);
    var dot9 = document.getElementById("d9");
    dot9.className = getReadingTimeColor("p9", baseline);
}).begin();

// Turn off video
webgazer.showVideoPreview(false); /* shows all video previews */
// webgazer.showPredictionPoints(false); /* shows a square every 100 milliseconds where current prediction is */
  
// Enable smoothing
// webgazer.applyKalmanFilter(true); // Kalman Filter defaults to on.
