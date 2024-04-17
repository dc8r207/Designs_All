$(function () {

  $(".js-upload-design").click(function () {
  //  $("#modal-drawing").modal("show");
  console.log("Sucessfully triggered click event of button....... ");
  console.log( "drawing_cabinet/upload_design");
  $.ajax({
    url: 'upload_design/',      
    type: 'get',
    dataType: 'json',
    beforeSend: function () {
      $("#modal-drawing").modal("show");
    },
    success: function (data) {

    //  $("#modal-drawing .modal-content").html(data.html_form);//
    
      //console.log("Sucessfully Returned from ajax request");
     // console.log(data.html_form)
      $("#modal-drawing .modal-content").html(data.html_form);
    }
  });
  
  
  });
  $("#modal-drawing").on("submit",".js-design-upload-form",function()
  {
  console.log("sucessfully Initiated form submission......")
  var form=$(this);
  console.log("submission url:" )
  console.log(form.attr('action') )
  
  $.ajax({
   url:form.attr('action'),
   data: form.serialize(),
  type: form.attr("method"),
  dataType: 'json',
  success:function (data){
    if (data.form_is_valid)
    {
    alert("design uploaded");
     $("#modal-drawing").modal("hode")

    }
  else 
  {

    $("#modal-drawing .modal-content").html(data.html_form);

  }

  },
  error: function (xhr, status, error) {                        
    alert('Your form was not sent successfully.'); 
    console.error(error); 
} 

  });
  return false;
  });






});



