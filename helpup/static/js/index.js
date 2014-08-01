$(document).ready(function(){

    $('#newProjectBtn').on('click', function(){
        $('#newProject').toggle()
    });

    $('#createProject').on('click', function(){
        var newProject = {};
        var title=$('#projectTitle').val();
        var description=$('#projectDescription').val();
        var location=$('#projectZip').val();
        var ammount = $('#projectAmount').val();
        newProject.title = title;
        newProject.description = description;
        newProject.location = location;
        newProject.amount = ammount;

        console.log(title);
        console.log(description);
        console.log(location);
        console.log(ammount);



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


    $.ajax({
        url: '/get_project/',
        type: 'GET',
        data: 'json',
        success: function(response){
            console.log(response);
//            $('#projectTitle1').html(response.title);
//            $('#projectName1').html(response.title);
//            $('#projectDescription1').html(response.description);
            for (i=0; i<6; i++) {
                project = response.project_list[i];
                panel = i + 1;
                $('#projectTitle' + panel).html(project.title);
                $('#projectName' + panel).html(project.title);
                $('#projectDescription' + panel).html(project.description);
                console.log(project.image);
                var imgsrc= "{% static 'media/project_images/drose.jpg' %}";
                $('#projectImg'+ panel).html("<img src='media/"+project.image+"' class='img-responsive thumImg' alt=''>");
                $('#projectImgModal'+ panel).html("<img src='media/"+project.image+"' class='img-responsive' alt=''>");
                $('#studentModal' + panel).html(project.first_name);
                $('#donate' + panel).html("<a href='/view_project/" + project.id + "'><button class='btn btn-success btnCustom'>Get More Info</button></a><br><br>")



            }
        },
        error:function(response){
            console.log(response)
        }

    });

    $.ajax({
        url: '/get_user_project/',
        type: 'GET',
        dataType: 'json',
        success: function(response){
            console.log(response);
            for(i=0; i<response.project_list.length; i++){
                project = response.project_list[i];
                $('#projectList').append("<a href='/view_project/"+project.id+"' class='list-group-item'>"+project.title+"</a>")
            }

        },
        error: function(response){
            console.log(response)
        }
    });

    $(document).on('click', '#movePayment', function(){
        $('.donationInput').hide();
//        $('#donateModal').modal('toggle');
        $('.thanksDonate').fadeIn('slow');
        var donationAmount = $('#donation_amount').val();
        var projectId = $('.projectID').val();
        console.log(donationAmount);
        console.log(projectId);
        StripeCheckout.open({
            key: "pk_test_4V8sFPGyR79fKgbKT2ymeYEE",
            amount: donationAmount*100,
            name: 'Demo Site',
            description: '2 widgets ($20.00)',
            image:"/128x128.png"

        });


        var projectInfo={'donationAmount': donationAmount, 'projectId': projectId};
        projectInfo = JSON.stringify(projectInfo);
        $.ajax({
            url: '/make_donation/',
            type: 'POST',
            data: projectInfo,
            dataType: 'json',
            success: function(response){
                console.log(response)
            },
            error: function(response){
                console.log(response)
            }
        })
    });

    var zip;
    $('#googleSearch').keypress(function(event){

        var keycode = (event.keyCode ? event.keyCode : event.which);
        if(keycode == '13'){

            zip = $('#googleSearch').val();
            window.location.replace('/project_map/'+zip);
        }
    });




//    var locationArray = [];
//    $.ajax({
//        url: '/get_location/',
//        type: 'GET',
//        data: 'json',
//        success:function(response){
//            console.log(response);
//            locationArray = response.project_list
//        },
//        error: function(response){
//            console.log(response)
//
//        }
//
//    });
//    var geocoder;
//
//    var map;
//    $('#searchBtn').on('click',function codeAddress(){
//        var sAddress = document.getElementById('searchVal').value;
//
//        geocoder.geocode({'address': sAddress}, function(results, status) {
//            if (status == google.maps.GeocoderStatus.OK){
//                map.setCenter(results[0].geometry.location);
//                console.log(results);
//                for(i=0; i<locationArray.length; i++){
//                    var markers = [];
//                    var infowindows = [];
//
//                    var content = "<h2>"+locationArray[i].title+"</h2><p>"+locationArray[i].description+"</p><p><a href='/view_project/"+locationArray[i].id+"'>See More</a></p>";
//                    var infowindow = new google.maps.InfoWindow({
//                        content: content
//                    });
//
//                    var marker = new google.maps.Marker({
//                        map: map,
//                        position: new google.maps.LatLng(locationArray[i].lat,locationArray[i].lng),
//                        title: locationArray[i].title,
//                        infowindow: infowindow
//                    });
//
//                    infowindows.push(infowindow);
//
//
//                    google.maps.event.addListener(marker, 'click', function(){
//                        this.infowindow.open(map, this);
//                    });
//
//                    markers.push(marker);
//
//
//                }
//
//            }
//            else{
//
//                alert("Geocode was not successful because: " + status);
//            }
//
//        });
//    });
//
//
//    function initialize() {
//        var mapOptions = {
//            zoom: 11,
//            center: new google.maps.LatLng(37.7833, -122.4167)
//        };
//        map = new google.maps.Map(document.getElementById('map-canvas'),
//            mapOptions);
//        geocoder = new google.maps.Geocoder();
//    }
//
//
//    google.maps.event.addDomListener(window, 'load', initialize);






});

