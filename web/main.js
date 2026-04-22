
function startProgram(){
    image_pathArray = []
    document_pathArray = []

    var contactSheet = document.getElementById("contactSheet").value;
    console.log("Excel contact sheet : " +contactSheet);
    var contactSheetList = contactSheet.split('\\');
    var contactSheetName = contactSheetList[2];
    console.log("Excel File Name : " +contactSheetName);


    var message  = document.getElementById("message").value;
    console.log("Message : " + message);


    var img   = document.getElementById("image");
    for (var i = 0; i < img.files.length; i++){
      var imgFile = img.files[i];
      var imageFileSize = img.files[i].size;
      var imageFileSizeInMb = Math.round((imageFileSize / (1024*1024)));
      if (imageFileSizeInMb < 64){
        image_pathArray.push(imgFile.name);
      }
      else {
        alert("Uploaded Media File " + imgFile.name + "is larger than the 64MB limit." );
        nextPrev(0);
      }
    }
    image_path = image_pathArray.toString();
    console.log("Image Path : " + image_path);
    

    var docs = document.getElementById('docs');
    for (var i = 0; i < docs.files.length; i++){
      var docFile = docs.files[i];
      var docFileSize = docs.files[i].size;
      var docFileSizeInMb = Math.round((docFileSize / (1024*1024)));
      if (docFileSizeInMb < 64){
        document_pathArray.push(docFile.name);
      }
      else {
        alert("Uploaded Document File " + docFile.name + "is larger than the 64MB limit." );
        nextPrev(0);
      }
    }
    document_path = document_pathArray.toString();
    console.log("Document Path : " + document_path)


    document.getElementById("showContactNo").innerHTML = "";
    document.getElementById("contactList").innerHTML = "";  
    eel.load_whatsapp(contactSheetName,message,image_path,document_path)(get_data);
}


function get_data(contactInfo) {
    console.log("into get_data")
    console.log(contactInfo);
    document.getElementById("loading").innerHTML=""
    document.getElementById("showContactNo").innerHTML = contactInfo[0];
    document.getElementById("contactList").innerHTML = contactInfo[1];

}
function sendMessages(){
    eel.send_msg()
}

function update(){
  var x = document.getElementsByClassName("tab");
  x[currentTab].style.display = "none";
  updatetab = document.getElementById("updatepage")
  updatetab.style.display="block";
}

eel.expose(notify_js)
function notify_js(text) {
    var p = document.getElementById("notify_bar");
    p.innerHTML += "<br>" + text;
}

eel.expose(notify_fail)
function notify_fail(text) {
    var f = document.getElementById("notifyFail")
    f.innerHTML += "<br>" + text;
}

eel.expose(update_msg_text)
function update_msg_text(content){
  msg = document.getElementById("msg")
  msg.innerHTML=content
}

function closeBrowser() {
    eel.terminate()

}


var currentTab = 0; // Current tab is set to be the first tab (0)
showTab(currentTab); // Display the current tab

function showTab(n) {
  // This function will display the specified tab of the form ...
  var x = document.getElementsByClassName("tab");
  x[n].style.display = "block";
  // ... and fix the Previous/Next buttons:
  if (n == 0) {
    document.getElementById("prevBtn").style.display = "none";
  } else {
    document.getElementById("prevBtn").style.display = "inline";
  }
  if (n == (x.length - 1)) {
    document.getElementById("nextBtn").innerHTML = "Submit";
  } else {
    document.getElementById("nextBtn").innerHTML = "Next";
  }
  // ... and run a function that displays the correct step indicator:
  fixStepIndicator(n)
}

function nextPrev(n) {
  // This function will figure out which tab to display
  var x = document.getElementsByClassName("tab");
  // Exit the function if any field in the current tab is invalid:
  // if (n == 1 && !validateForm()) return false;
  // Hide the current tab:
  x[currentTab].style.display = "none";
  // Increase or decrease the current tab by 1:
  currentTab = currentTab + n;
  // if you have reached the end of the form... :
  if (currentTab >= x.length) {
    //...the form gets submitted:
    document.getElementById("regForm").submit();
    return false;
  }
  // Otherwise, display the correct tab:
  showTab(currentTab);
}

function validateForm() {
  // This function deals with validation of the form fields
  var x, y, i, valid = true;
  x = document.getElementsByClassName("tab");
  y = x[currentTab].getElementsByTagName("input");
  // A loop that checks every input field in the current tab:
  for (i = 0; i < y.length; i++) {
    // If a field is empty...
    if (y[i].value == "") {
      // add an "invalid" class to the field:
      y[i].className += " invalid";
      // and set the current valid status to false:
      valid = false;
    }
  }
  // If the valid status is true, mark the step as finished and valid:
  if (valid) {
    document.getElementsByClassName("step")[currentTab].className += " finish";
  }
  return valid; // return the valid status
}

function fixStepIndicator(n) {
  // This function removes the "active" class of all steps...
  var i, x = document.getElementsByClassName("step");
  for (i = 0; i < x.length; i++) {
    x[i].className = x[i].className.replace(" active", "");
  }
  //... and adds the "active" class to the current step:
  x[n].className += " active";
}

function updateEnviron(){
  username = document.getElementById("username").value
  msg = document.getElementById("msg")
  msg.innerHTML="Updating..... Please Wait"
  eel.update(username)
}






