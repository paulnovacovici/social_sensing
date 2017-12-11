var config = {
  apiKey: "AIzaSyCYH4k6zlm044XGGBa2iRQDKgdFO3qo1x0",
  authDomain: "social-sensing-6d403.firebaseapp.com",
  databaseURL: "https://social-sensing-6d403.firebaseio.com",
  projectId: "social-sensing-6d403",
  storageBucket: "social-sensing-6d403.appspot.com",
  messagingSenderId: "374226843039"
};

firebase.initializeApp(config);
var database = firebase.database();
var dbRef = firebase.database().ref('/');

google.charts.load('current', {'packages':['corechart','line','imagelinechart']});
google.charts.setOnLoadCallback(updateGraph);

dates = {
  "January" : 0, 
  "February" : 1,
  "March" : 2,
  "April" : 3,
  "May" : 4,
  "June" : 5,
  "July" : 6,
  "August" : 7,
  "September" : 8,
  "October" : 9,
  "November" : 10,
  "December" : 11
}

/*
Update chart in real time once new 
values are added to database
*/
function updateGraph(val){
  var data = [
  ['Time','Account Balance']
  ]

  for (var _day in val){
    var arr = _day.split(" ");
    var month = dates[arr[0]];
    var day = parseInt(arr[1].replace(',',''));
    var year = parseInt(arr[2]);
    for (var time in val[_day]){
      arr = time.split(":");
      var hours = parseInt(arr[0]);
      var minutes = arr[1];
      if (minutes.length == 1){
        minutes = "0" + minutes;
      }
      minutes = parseInt(minutes)
      data.push([new Date(year, month, day, hours, minutes), val[_day][time]])
    }
  }
  drawChart(data);
}

function drawChart(stock_data) {
  console.log(stock_data);
  var data = google.visualization.arrayToDataTable(stock_data);

  var options = {
    title: 'Algorithm Performance',
    curveType: 'function',
    legend: { position: 'top' },
    width: '1000',
    height: '1000'
  };

  var chart = new google.visualization.ImageLineChart(document.getElementById('curve_chart'));

  chart.draw(data, options);
}

dbRef.on('value', function(snapshot) {
  updateGraph(snapshot.val());
});