

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