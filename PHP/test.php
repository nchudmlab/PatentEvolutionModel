

<!DOCTYPE html>
<html>
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <title>bihisankey diagram</title>
    <link href="style.css" rel="stylesheet">
    <script src="https://code.jquery.com/jquery-1.12.0.min.js"></script>
  </head>
  <body>
    <h1> H04W [Wireless communications networks] EVOLUATION WITH PATENTS</h1>
    <div id="chart" ></div>
    <script src="http://d3js.org/d3.v3.min.js"></script>
    <!--<script src="https://cdn.rawgit.com/Neilos/bihisankey/master/bihisankey.js"></script>-->
	<script src="https://maps.googleapis.com/maps/api/js?key=AIzaSyDV5nEkXBMfkm57mVLzw7blZxIi3jBLgxU"></script>
    
    <script>
		var origin1 = new google.maps.LatLng(55.930385, -3.118425);
var origin2 = "Greenwich, England";
var destinationA = "Stockholm, Sweden";
var destinationB = new google.maps.LatLng(50.087692, 14.421150);

var service = new google.maps.DistanceMatrixService();
service.getDistanceMatrix(
  {
    origins: [origin1, origin2],
    destinations: [destinationA, destinationB],
    travelMode: google.maps.TravelMode.DRIVING,
    //transitOptions: TransitOptions,
    //drivingOptions: DrivingOptions,
    //unitSystem: UnitSystem,
    //avoidHighways: Boolean,
    //avoidTolls: Boolean,
  }, callback);

function callback(response, status) {
  // See Parsing the Results for
  // the basics of a callback function.
  alert(response.rows[0].elements[0]);
}
	
	</script>
  </body>
</html>