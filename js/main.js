
function checkCookie(){
  // create a cookie and to check if browser has cookies enabled
  document.cookie="testcookie";
  cookieEnabled=(document.cookie.indexOf("testcookie")!=-1)? true : false;
  
  return (cookieEnabled)?true:showCookieFail();
}

function showCookieFail(){
  // redirects to page showing that cookies are disabled
  if(document.URL.indexOf("cookiesDisabled") == -1)
    window.location = "cookiesDisabled";

}

function validateNewGoalForm() {
  var goalTitleVal=document.forms["newGoalForm"]["tbGoalName"].value;
  var goalDescVal=document.forms["newGoalForm"]["tbGoalDesc"].value;

  if (goalTitleVal==null || goalTitleVal=="") {
    document.getElementById('tbGoalName').placeholder="Please enter a title";
    document.getElementById("divRowTitle").className="control-group error";
    return false;
  }

  if(goalDescVal==null || goalDescVal==""){
    document.getElementById('tbGoalDesc').placeholder="Please enter a description";
    document.getElementById("divRowDesc").className="control-group error";
    return false;
  }
}