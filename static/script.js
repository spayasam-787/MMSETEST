let currentQuestionIndex = 0;
let questions = [];
const nameEle = document.getElementById("name");
const simpleImg = document.getElementById("simple-img");
const chooseWords = document.getElementById("choose-words");
const clockContainer = document.getElementById("clock-container");
const drawContainer = document.getElementById("draw-container");
const endContainer = document.getElementById("end-container");

const viewReportBtn = document.getElementById("view-report-btn");

// Clock!

const hourHand = document.getElementById("hourHand");
const minuteHand = document.getElementById("minuteHand");
const hourAngleInput = document.getElementById("hourAngle");
const minuteAngleInput = document.getElementById("minuteAngle");
const hourValue = document.getElementById("hourValue");
const minuteValue = document.getElementById("minuteValue");

function updateClockHands() {
    const hourAngle = parseInt(hourAngleInput.value);
    const minuteAngle = parseInt(minuteAngleInput.value);

    hourHand.style.transform = `translateX(-2px) translateY(-50px) rotate(${hourAngle}deg)`;
    minuteHand.style.transform = `translateX(-1px)
    translateY(-75px) rotate(${minuteAngle}deg)`;

    hourValue.textContent = hourAngle;
    minuteValue.textContent = minuteAngle;
}

hourAngleInput.addEventListener("input", updateClockHands);
minuteAngleInput.addEventListener("input", updateClockHands);

// Initial update
updateClockHands();

// End of clock

document.getElementById("start-btn").onclick = () => {
    // change start-btn class from btn-primary to btn-warning and change text to "Restart"
    const name = document.getElementById("name").value;
    if (document.getElementById("start-btn").classList.contains("btn-primary")) {
        document.getElementById("start-btn").classList.remove("btn-primary");
        document.getElementById("start-btn").classList.add("btn-warning");
        document.getElementById("start-btn").innerHTML = "Restart";
        document.getElementById("name").outerHTML  = `<h3> <b id='name'> ${document.getElementById("name").value} </b> </h3>`
    }
    // set simple-img, choose-words, clock-container, draw-container classes to no-display if they don't have it already
    if (!simpleImg.classList.contains("no-display")) {
        simpleImg.classList.add("no-display");
    }
    if (!chooseWords.classList.contains("no-display")) {
        chooseWords.classList.add("no-display");
    }
    if (!clockContainer.classList.contains("no-display")) {
        clockContainer.classList.add("no-display");
    }
    if (!drawContainer.classList.contains("no-display")) {
        drawContainer.classList.add("no-display");
    }
    if (!endContainer.classList.contains("no-display")) {
        endContainer.classList.add("no-display");
    }

    if (document.getElementById("start-btn").classList.contains("btn-primary")) {
        // reload the page
        location.reload();
    }
    else{
        fetch("/start",
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ name: name }),
        })
        .then((response) => response.json())
        .then((data) => {
            console.log(data);
            // wait for 2 seconds before calling group2()
            setTimeout(group2, 2000);
        });
    }
    clearCanvas();
};

function group2() {
    fetch("/group2")
    .then((response) => response.json())
    .then((data) => {
        console.log(data);
        group3()
    });
}

function group3() {
    fetch("/group3")
    .then((response) => response.json())
    .then((data) => {
        console.log(data);
        group4()
    });
}

function group4() {
    fetch("/group4")
    .then((response) => response.json())
    .then((data) => {
        console.log(data);
        group5_1()
    });
}

function group5_1() {
    fetch("/group5_1")
    .then((response) => response.json())
    .then((data) => {
        console.log(data);
        // if data['status] exists, do not call group5_2()
        if (data['status']) {
            group6()
        }
        else{
            simpleImg.classList.remove("no-display");
            simpleImg.getElementsByTagName("img")[0].src = data[1];
            group5_2()
        }
    });
}

function group5_2() {
    fetch("/group5_2")
    .then((response) => response.json())
    .then((data) => {
        console.log(data);
        group5_1_repeat()
    });
}

function group5_1_repeat() {
    fetch("/group5_1_repeat")
    .then((response) => response.json())
    .then((data) => {
        console.log(data);
        // remove class called no-display from simple-img
        simpleImg.getElementsByTagName("img")[0].src = data[1];
        group5_2_repeat()
    });
}

function group5_2_repeat() {
    fetch("/group5_2_repeat")
    .then((response) => response.json())
    .then((data) => {
        console.log(data);
        simpleImg.classList.add("no-display");
        group6()
    });
}

function group6() {
    fetch("/group6")
    .then((response) => response.json())
    .then((data) => {
        console.log(data);
        group7_1()
    });
}

function group7_1() {
    fetch("/group7_1")
    .then((response) => response.json())
    .then((data) => {
        console.log(data);
        if (data['status']) {
            group8_1()
        }
        else{
            document.querySelector('#choose-words').classList.remove('no-display')
            document.querySelector('#choose-words-inst').innerHTML = `Click the button with the word "${data[1]}"`
            // create two buttons inside #click-btn div woth the array from data[0]
            let btns = ''
            for (let i = 0; i < data[0].length; i++) {
                btns += `<button id="btn${i}" class="btn btn-primary btn-lg m-2">${data[0][i]}</button>`
            }
            document.querySelector('#click-btn').innerHTML = btns
        }
    });
}

document.addEventListener('click', function(e) {
    if (e.target && e.target.classList.contains('btn-lg')) {
        target = e.target.innerHTML
        fetch("/group7_2", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({target: target})
        })
        .then((response) => response.json())
        .then((data) => {
            console.log(data);
            document.querySelector('#choose-words').classList.add('no-display')
            group8_1()
        });
    }
})

function group8_1() {
    fetch("/group8_1")
    .then((response) => response.json())
    .then((data) => {
        console.log(data);
        if (data['status']) {
            group9()
        }
        else{
        document.querySelector('#clock-inst').innerHTML = `Set the clock to ${data['hour']}:${data['minute']}`
        document.querySelector('#clock-container').classList.remove('no-display')
        }
    });
}

document.addEventListener('click', function(e) {
    if (e.target && e.target.id == 'clock-btn') {
        // hourAngle and minuteAngle id input fields values
        hourAngle = document.querySelector('#hourAngle').value
        minuteAngle = document.querySelector('#minuteAngle').value
        fetch("/group8_2", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({hour: hourAngle, minute: minuteAngle})
        })
        .then((response) => response.json())
        .then((data) => {
            console.log(data);
            document.querySelector('#clock-container').classList.add('no-display')
            group9()
        });
    }
})

function group9() {
    fetch("/group9")
    .then((response) => response.json())
    .then((data) => {
        console.log(data);
        group10()
    });
}

function group10() {
    document.querySelector('#draw-container').classList.remove('no-display')
    fetch("/group10_1")
    .then((response) => response.json())
    .then((data) => {
        console.log(data);
    });

}

// drawing
var width = window.innerWidth;
var height = window.innerHeight - 25;

// first we need Konva core things: stage and layer
var stage = new Konva.Stage({
container: 'canvas-container',
width: 600,
height: 500,
});

var layer = new Konva.Layer();
stage.add(layer);

var isPaint = false;
var mode = 'brush';
var lastLine;

stage.on('mousedown touchstart', function (e) {
isPaint = true;
var pos = stage.getPointerPosition();
    lastLine = new Konva.Line({
        stroke: '#000',
        strokeWidth: 5,
        globalCompositeOperation:
        mode === 'brush' ? 'source-over' : 'destination-out',
        // round cap for smoother lines
        lineCap: 'round',
        lineJoin: 'round',
        // add point twice, so we have some drawings even on a simple click
        points: [pos.x, pos.y, pos.x, pos.y],
    });
    layer.add(lastLine);
});

stage.on('mouseup touchend', function () {
    isPaint = false;
});

// and core function - drawing
stage.on('mousemove touchmove', function (e) {
    if (!isPaint) {
        return;
    }

    // prevent scrolling on touch devices
    e.evt.preventDefault();

    const pos = stage.getPointerPosition();
    var newPoints = lastLine.points().concat([pos.x, pos.y]);
    lastLine.points(newPoints);
});

// Clear Canvas Function
function clearCanvas() {
    layer.removeChildren();
    layer.draw();
}

// Save Canvas as Image Function
function saveCanvasAsImage() {
    var tempCanvas = document.createElement('canvas');
    tempCanvas.width = stage.width();
    tempCanvas.height = stage.height();

    var tempContext = tempCanvas.getContext('2d');

    // Draw a white background
    tempContext.fillStyle = '#FFFFFF'; // White color
    tempContext.fillRect(0, 0, tempCanvas.width, tempCanvas.height);

    // Draw the original canvas content on top of the white background
    tempContext.drawImage(stage.toCanvas(), 0, 0);

    // Convert to Data URL
    var dataURL = tempCanvas.toDataURL("image/png");
    // send dataURL to server
    fetch("/group10", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({dataURL: dataURL})
    }).then((response) => response.json())
    .then((data) => {
        console.log(data);

    document.querySelector('.spinner-border').classList.add('no-display')
    document.getElementById('view-report-btn').dataset.folderName = data['folder_name']
});
}

viewReportBtn.addEventListener('click', () => {
    folderName = viewReportBtn.dataset.folderName
    fetch("/open_report", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({folderName: folderName})
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
    });
});


// Download URI Function
function downloadURI(data, filename) {
    var a = document.createElement('a');
    a.setAttribute('download', filename);
    a.setAttribute('href', data);
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
}

// Clear Canvas Button Event Listener
document.getElementById('clear-canvas-btn').addEventListener('click', function () {
    clearCanvas();
});

// Submit Drawing Button Event Listener
document.getElementById('submit-drawing-btn').addEventListener('click', function () {
    saveCanvasAsImage();
    drawContainer.classList.add("no-display");
    endContainer.classList.remove("no-display");
});
