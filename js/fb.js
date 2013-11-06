
function login() {
  FB.login(function(response) {
      if (response.authResponse) {
          // connected
          testAPI()
      } else {
          // cancelled
      }
  });
}

function testAPI() {
  FB.api('/me', function(response) {
    console.log('Good to see you, ' + response.name + '.');
  });
}

function on_post_callback(response) {
  if (response && response.post_id) {
    console.log('Post was published.');
  } else {
    console.log('Post was not published.');
  }
}

function postGoalToWall(userSetPublic) {
  var goalTitle = document.getElementById('tbGoalName').value;
  var goalDesc = document.getElementById('tbGoalDesc').value;

  if (goalTitle == "" || goalDesc == "") {
    return;
  }

  if (userSetPublic == "publicBtnClicked") {
    document.getElementById('userChosePublic').value = "public";
    var username = document.getElementById('hdnUname').value;
    var goalTypeSelect = document.getElementById('ddGoalType').value;
    var pictureLink = "https://improve-facebookapp.appspot.com/bootstrap/img/"; 

    switch(goalTypeSelect){
      case "Fitness Goal":
        pictureLink+="fitness.png";
        break;
      case "Life Goal":
        pictureLink+="life.png";
        break;
      case "Academic Goal":
        pictureLink+="academic.png";
        break;

    }   

    var goalDeadline = document.getElementById('datePickerDL').value;
    var fbDescription = username + " wants to " + goalTitle + " by " + goalDeadline;
    var fbName = username + "has set a new goal";

    // calling the API ...
    //TODO Change picture to pictureLink variable once image hosting works
    var obj = {
      method: 'feed',
      redirect_uri: 'http://apps.facebook.com/improve-app/',
      link: 'http://apps.facebook.com/improve-app/',
      picture: pictureLink, 
      name: fbName,
      caption: goalTypeSelect,
      description: fbDescription
    };

    FB.ui(obj, on_post_callback);
   }
   else {
    // user selected private
    document.getElementById('userChosePublic').value = "private";
   }
}

function postSuccessToWall() {
  var username = document.getElementById('hdnUname').value;
  var pictureLink = "https://improve-facebookapp.appspot.com/bootstrap/img/trophy.png";
  var goalTitle =  document.getElementById('hdnGoalName').value;
  var goalDesc = document.getElementById('hdnGoalDesc').value;
  var fbDescription = username + " has accomplished " + goalTitle + " which was to " + goalDesc;
  var fbName = username + " has accomplished one of their goals!";

  // calling the API ...
  var obj = {
    method: 'feed',
    redirect_uri: 'https://apps.facebook.com/improve-app/goalViewer',
    link: 'http://apps.facebook.com/improve-app',
    picture: pictureLink,
    name: fbName,
    caption: 'Congratulations!',
    description: fbDescription
  };

  FB.ui(obj, on_post_callback);
}

function postUpdateToWall() {
  var username = document.getElementById('hdnUname').value;
  var pictureLink = "https://improve-facebookapp.appspot.com/bootstrap/img/logo.png";
  var goalTitle =  document.getElementById('hdnGoalName').value;
  var goalDesc = document.getElementById('hdnGoalDesc').value;
  var fbDescription = username + " wants to tell you about " + goalTitle + " which was to " + goalDesc;
  var fbName = username + " has an update on one of their goals!";

  // calling the API ...
  var obj = {
    method: 'feed',
    redirect_uri: 'https://apps.facebook.com/improve-app/goalViewer',
    link: 'http://apps.facebook.com/improve-app',
    picture: pictureLink,
    name: fbName,
    caption: 'Improve!',
    description: fbDescription
  };

  FB.ui(obj, on_post_callback);

}

