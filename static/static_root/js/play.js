$(document).ready( function() {
  var form =$('#user-attempt');
  var submitted_attempt=form.value;

  form.submit(function() {
    // alert(submitted_attempt);
    $.ajax({
      $("#verb").innerHTML = "ADASADAS";
      type:form.attr('method'),
      url: form.attr('action'),
      data: {attempt:submitted_attempt},
      success: function(data){
        alert("asda0");
      },
      failure: function(data){
        alert("Failed Attempt");
      }
    });
    return false;
  });


});
