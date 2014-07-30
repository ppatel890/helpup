$(document).ready(function(){

    $('#newProjectBtn').on('click', function(){
        $('#newProject').toggle()
    });

    $('#createProject').on('click', function(){
        var newProject = {};
        var title=$('#projectTitle').val();
        var description=$('#projectDescription').val();
        var location=$('#projectZip').val();
        newProject.title = title;
        newProject.description = description;
        newProject.location = location;
        console.log(title);
        console.log(description);
        console.log(location);


        $.ajax({
            url:'https://maps.googleapis.com/maps/api/geocode/json?address=+'+location,
            type: 'GET',
            dataType: 'json',
            success: function(response){
                console.log(response);
                newProject.lat=response.results[0].geometry.location.lat;
                newProject.lng=response.results[0].geometry.location.lng;
                console.log(newProject.lat);
                console.log(newProject.lng);
            },
            error: function(response){
                console.log(response)
            }

        }).complete(function(){
            var dataObj = JSON.stringify(newProject);
            $.ajax({
                url: '/new_project/',
                type: 'POST',
                dataType: 'json',
                data: dataObj,
                success: function(response){
                    console.log(response);
                    $('#projectTitle').val('');
                    $('#projectDescription').val('');
                    $('#projectZip').val('');
                    $('#newProject').hide()
                },
                error: function(response){
                    console.log(response)
                }
        })

        });
    });

    var locationArray = [];
    $.ajax({
        url: '/get_location/',
        type: 'GET',
        data: 'json',
        success:function(response){
            console.log(response);
            locationArray = response.project_list
        },
        error: function(response){
            console.log(response)

        }

    });
    var geocoder;

    var map;
    $('#searchBtn').on('click',function codeAddress(){
        var sAddress = document.getElementById('searchVal').value;

        geocoder.geocode({'address': sAddress}, function(results, status) {
            if (status == google.maps.GeocoderStatus.OK){
                map.setCenter(results[0].geometry.location);
                console.log(results);
                for(i=0; i<locationArray.length; i++){
                    var markers = [];
                    var infowindows = [];

                    var content = locationArray[i].description;
                    var infowindow = new google.maps.InfoWindow({
                        content: content
                    });

                    var marker = new google.maps.Marker({
                        map: map,
                        position: new google.maps.LatLng(locationArray[i].lat,locationArray[i].lng),
                        title: locationArray[i].title,
                        infowindow: infowindow
                    });

                    infowindows.push(infowindow);


                    google.maps.event.addListener(marker, 'click', function(){
                        this.infowindow.open(map, this);
                    });

                    markers.push(marker);


                }

            }
            else{

                alert("Geocode was not successful because: " + status);
            }

        });
    });


    function initialize() {
        var mapOptions = {
            zoom: 11,
            center: new google.maps.LatLng(37.7833, -122.4167)
        };
        map = new google.maps.Map(document.getElementById('map-canvas'),
            mapOptions);
        geocoder = new google.maps.Geocoder();
    }


    google.maps.event.addDomListener(window, 'load', initialize);

});

