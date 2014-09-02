$(document).ready(function(){

    // Sends information from create project modal to database
    $('#createProject').on('click', function(){
        var newProject = {};
        var title=$('#projectTitle').val();
        var description=$('#projectDescription').val();
        var location=$('#projectZip').val();
        var amount = $('#projectAmount').val();
        newProject.title = title;
        newProject.description = description;
        newProject.location = location;
        newProject.amount = amount;

        // Geocodes the zipcode the user inputs
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
            // Posts the new project to the database
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

    // Creates the modals and tiles on the homepage
    $.ajax({
        url: '/get_project/',
        type: 'GET',
        data: 'json',
        success: function(response){
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

    // Gets the users projects
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
        $('.thanksDonate').fadeIn('slow');
        var donationAmount = $('#donation_amount').val();
        var projectId = $('.projectID').val();
        console.log(donationAmount);
        console.log(projectId);
        StripeCheckout.open({
            key: "pk_test_4V8sFPGyR79fKgbKT2ymeYEE",
            amount: donationAmount*100,
            name: 'Help Up',
            description: 'Make Your Donation Here'
//            image:"/128x128.png"

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


    // Redirects to map centered on zip code the user input
    var zip;
    $('#googleSearch').keypress(function(event){

        var keycode = (event.keyCode ? event.keyCode : event.which);
        if(keycode == '13'){

            zip = $('#googleSearch').val();
            window.location.replace('/project_map/'+zip);
        }
    });



});

