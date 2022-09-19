var canvas;
var context;
var img;

// load 이벤트 리스너 등록. 웹페이지가 로딩된 후 실행
window.addEventListener("load", function() {
        canvas = document.getElementById("myCanvas");
        context = canvas.getContext("2d");

        img = new Image();
        img.onload = function () {
                context.drawImage(img, 0, 0); // (0,0) 위치에 img의 크기로 그리기
        }
});

// drawImage()는 "image' 토픽이 도착하였을 때 onMessageArrived()에 의해 호출된다.
function drawImage(imgUrl) { // imgUrl은 이미지의 url
        img.src = imgUrl; // img.onload에 등록된 코드에 의해 그려짐
}

var isImageSubscribed = false;
function recognize() {
        if(!isImageSubscribed) {
                subscribe('image'); // 토픽 image 등록
                isImageSubscribed = true;
        }
        publish('facerecognition', 'action'); // 토픽: facerecognition, action 메시지 전송
}

(myEnv) pi@raspberrypi:~/myEnv/static $ ^C
(myEnv) pi@raspberrypi:~/myEnv/static $ cat humChart.js
// Chart 객체에 넘겨줄 차트에 대한 정보들을 정의한 객체
var config = {
        type: 'line', //출력되는 차트 종류 라인으로
        // data는 차트에 출력될 전체 데이터 표현
        data: {
                // labels는 배열로 데이터의 레이블들
                labels: [],
                // datasets 배열로 습도에 관한 그래프 하나만 있다
                datasets: [{
                        label: '실시간 데이터 흐름',
                        backgroundColor: 'yellow',
                        borderColor: 'rgb(255, 99, 132)',
                        borderWidth: 2,
                        data: [], //각 레이블에 해당하는 데이터
                        fill : false,
                }]
        },
        //  차트의 속성 지정
        options: {
                responsive : false, // 크기 조절 금지
                scales: {
                        xAxes: [{
                                display: true,
                                scaleLabel: { display: true, labelString: '시간' }, //x축에는 시간의 흐름
                        }],
                        yAxes: [{
                                display: true,
                                scaleLabel: { display: true, labelString: '습도(%)' } //퍼센트단위로 습도 나타냄
                        }]
                }
        }
};
var ctx = null
var chart = null
var LABEL_SIZE = 20; // 차트에 그려지는 데이터의 개수
var tick = 0; // 도착한 데이터의 개수임, tick의 범위는 0에서 99까지만
var canvas = document.getElementById("canvas");
function drawChart() {
        ctx = document.getElementById('canvas').getContext('2d');
        chart = new Chart(ctx, config);
        init();
} // end of drawChart()


// chart의 차트에 labels의 크기를 LABEL_SIZE로 만들고 0~19까지 레이블 붙이기
function init() {
        for(let i=0; i<LABEL_SIZE; i++) {
                chart.data.labels[i] = i;
        }
        chart.update();
}

function addChartData(value) {
        tick++; // 도착한 데이터의 개수 증가
        tick %= 100; // tick의 범위는 0에서 99까지만. 100보다 크면 다시 0부터 시작
        let n = chart.data.datasets[0].data.length; // 현재 데이터의 개수
        if(n < LABEL_SIZE)
                chart.data.datasets[0].data.push(value);
        else {
                // 새 데이터 value 삽입
                chart.data.datasets[0].data.push(value);
                chart.data.datasets[0].data.shift();
                // 레이블 삽입
                chart.data.labels.push(tick);
                chart.data.labels.shift();
        }
        chart.update();
}

function hideshow() { // 차트 보이기 숨기기
        if(canvas.style.display == "none")      canvas.style.display = "block"
        else canvas.style.display = "none"
}

window.addEventListener("load", drawChart); // load 이벤트가 발생하면 drawChart() 호출하도록 등록
