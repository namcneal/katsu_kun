var observer = new MutationObserver(ShakeMain);

$(document).ready( function() {
  var form =$('#user-attempt');
  var submitted_attempt=form.attr("attempt")

  form.submit(function() {
    $.ajax({
      type:form.attr('method'),
      url: form.attr('action')
      data: {attempt:submitted_attempt}
    });
    return false;
  });


});
