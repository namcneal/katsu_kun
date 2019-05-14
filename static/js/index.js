$(document).ready( function() {
    $("#start-btn").click( function(event) {

      if($('.verb-form:checkbox:checked').length == 0){
        alert("Please select at least one verb form.");
        event.preventDefault();
      }

      else if($('.verb-type:checkbox:checked').length == 0){
        alert("Please select at least one type of verb.");
        event.preventDefault();
      }

      else if($('.verb-polarity:checkbox:checked').length == 0){
        alert("Please select positive and/or negative.");
        event.preventDefault();
      }

      else if($('.verb-tense:checkbox:checked').length == 0){
        alert("Please select at least one tense.");
        event.preventDefault();
      }

      else if($('.conjugation:checkbox:checked').length == 0){
        alert("Please select at least one conjugation form to practice.");
        event.preventDefault();
      }
      $('#game-params').serialize();
    });

});

function ToggleLanguage(){
  if(document.getElementById("toggle-en").checked){
    document.body.className ="en";
  }
  else if(document.getElementById("toggle-jp").checked){
    document.body.className ="jp";
  }
}
