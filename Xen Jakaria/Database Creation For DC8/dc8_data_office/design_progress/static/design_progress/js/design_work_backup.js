 $(function () {

  /* Functions */

  var loadForm = function () {
    console.log("Sucessfully Triggered  Add design work event.....")
    var btn = $(this);
    console.log(btn.attr("data-url"));
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-drawing .modal-content").html("");
        $("#modal-drawing").modal("show");
      },
      success: function (data) {
        $("#modal-drawing .modal-content").html(data.html_form);
      }
    });
  };

  var loadForm2 = function () {
    //alert("Sucessfully Triggered Delete Design Event")
    var btn = $(this);
    console.log(btn.attr("data-url"));
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-drawing .modal-content").html("");
        $("#modal-drawing").modal("show");
      },
      success: function (data) {
        $("#modal-drawing .modal-content").html(data.html_form);
      }
    }); 
  };



  var saveForm = function () {
    var form = $(this);
    console.log(typeof form)
    console.log(form)
    var fd=new FormData();
    console.log(fd)
    console.log("processing form submit event......");
    console.log($("#id_drawing_no").val());
    var dwg_no=$("#id_drawing_no").val();
    var pdf_drw=$("#id_pdf_drw")[0].files[0];
    var dxf_drw=$("#id_dxf_drw")[0].files[0];
    console.log(pdf_drw)
   // console.log(dwg_no);
    fd.append("drawing_no",dwg_no);
    fd.append("pdf_drw",pdf_drw,pdf_drw.name);
    fd.append("dxf_drw",dxf_drw,dxf_drw.name);
    //getting csrf token
    var csrftoken = $("[name=csrfmiddlewaretoken]").val();
    console.log(fd)
    console.log(fd.pdf_drw)
    $.ajax({
      url: form.attr("action"),
     // data: form.serialize(),
      data:fd,
      type: form.attr("method"),
      headers:{
        "X-CSRFToken": csrftoken
    },
      //dataType: 'json',
      contentType:false,
      processData:false,

    
      success: function (data) {
        if (data.form_is_valid) {
        //  $("#drawing-table tbody").html("");
          $("#drawing-table tbody").html(data.html_design_list);
          $("#modal-drawing").modal("hide");

        }
        else {
          $("#modal-drawing .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };
 var saveDeleteForm =function () 
 
 {
  var form = $(this);
  $.ajax({
    url: form.attr("action"),
    data: form.serialize(),
    type: form.attr("method"),
    dataType: 'json',
    success: function (data) {
      if (data.form_is_valid) {
        $("#drawing-table tbody").html(data.html_design_list);
        $("#modal-drawing").modal("hide");
      }
      else {
        $("#modal-drawing .modal-content").html(data.html_form);
      }
    }
  });
  return true;


 };
var saveDesignWork=function()
{
var form=$(this);
//getting csrf token
var csrftoken = $("[name=csrfmiddlewaretoken]").val();
console.log("Sucessfully Triggered Design Work Creation form Save Event.....");
$.ajax({
  url:form.attr("action"),
  data:form.serialize(),
  type:form.attr("method"),
  dataType:'json',
  headers:{
    "X-CSRFToken": csrftoken
},
  success:function (data) 
  {
    if (data.form_is_valid)
    {   
      
      $("#drawing-table tbody").html(data.html_work_list);
      $("#modal-drawing").modal("hide");
      alert("Design Work created !");
    }
    else
    {
    
      $("#modal-drawing .modal-content").html(data.html_form);

    }


  }


});
return true;
};


var saveProgress=function()
{
var form=$(this);
//getting csrf token
var csrftoken = $("[name=csrfmiddlewaretoken]").val();
console.log("Sucessfully Triggered Progress Form Submission Event.....");
$.ajax({
  url:form.attr("action"),
  data:form.serialize(),
  type:form.attr("method"),
  dataType:'json',
  headers:{
    "X-CSRFToken": csrftoken
},
  success:function (data) 
  {
    if (data.form_is_valid)
    {   
      
      $("#drawing-table tbody").html(data.html_work_list);
      $("#modal-drawing").modal("hide");
      alert("Design Work created !");
    }
    else
    {
    
      $("#modal-drawing .modal-content").html(data.html_form);

    }


  }


});
return false;
};







  /* Binding */
  //create design work
  $(".js-design-create-button").click(loadForm);
  $("#modal-drawing").on("submit",".js-design-work-create-form",saveDesignWork)
  //update design_progress
  //$(".js-update-design-progress-button").click(loadForm);
  //$("#modal-drawing").on("submit",".js-update-design-progress-form",saveDesignWork)
  

 // $(".js-design-create-form").click(loadForm);

  /*
  $(".js-upload-design").click(loadForm);
  $("#modal-drawing").on("submit", ".js-design-upload-form", saveForm);
  
  */
  //js-design-create-form

  // Update Design
  /*
  $("#drawing_table").on("click", ".js-update-design", loadForm );
  $("#modal-drawing").on("submit", ".js-design-update-form", saveForm);
  */
  //js-design-work-create-form

  // Delete book
  //$("#drawing_table").on("click", ".js-delete-design", loadForm);
  /*
  $("#drawing_table").on("click", ".js-delete-design", loadForm2 );  
  $("#modal-drawing").on("submit", ".js-design-delete-form", saveDeleteForm);
  */

});
