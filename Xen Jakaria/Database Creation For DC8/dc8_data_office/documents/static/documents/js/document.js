 $(function () {
  var loadForm = function () {
    console.log("Sucessfully Triggered Add Document Event........")
    var btn = $(this);
    console.log(btn.attr("data-url"));
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      
      beforeSend: function () {
        $("#modal-document .modal-content").html("");
        $("#modal-document").modal("show");
      },
      success: function (data) {
        $("#modal-document .modal-content").html(data.html_form);
      }
    });
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
        alert("Design Work created !");
        $("#modal-drawing").modal("hide");
        $("#drawing-table tbody").html(data.html_work_list);
        
        
      }
      else
      {
      
        $("#modal-drawing .modal-content").html(data.html_form);
  
      }
  
  
    }
  
  
  });
  return false;
  };
  var saveForm = function () {
    var form = $(this);
    console.log(typeof form)
    console.log(form)
    var fd=new FormData();
    console.log(fd)
    console.log("processing form submit event......");
    console.log($("#id_doc_description").val());
    var doc_description=$("#id_doc_description").val();
    var doc_type=$("#id_doc_type").val();
    var pdf_doc=$("#id_pdf_doc")[0].files[0];
    //var dxf_drw=$("#id_dxf_drw")[0].files[0];
    //console.log(pdf_drw)
   // console.log(dwg_no);
    fd.append("doc_description",doc_description);
    fd.append("doc_type",doc_type);
    fd.append("pdf_doc",pdf_doc,pdf_doc.name);
    //getting csrf token
    var csrftoken = $("[name=csrfmiddlewaretoken]").val();
    console.log(fd)
    console.log(fd.pdf_doc)
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
          
          alert("Document is Saved")
          $("#modal-document").modal("hide");
          $("#document_table tbody").html(data.html_document_list);

        }
        else {
          $("#modal-document .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };

  var saveDesignProgress=function()
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
        alert("Design Work created !");
        $("#modal-drawing").modal("hide");
        $("#drawing-table tbody").html(data.html_work_list);
        
        
      }
      else
      {
      
        $("#modal-drawing .modal-content").html(data.html_form);
  
      }
  
  
    }
  
  
  });
  return false;
  };
  var saveDeleteForm =function () 
 
  {
   //alert("sending ajax request at .........")
  
   var form = $(this);
   //alert(form.attr("action"))
   $.ajax({
     url: form.attr("action"),
     data: form.serialize(),
     type: form.attr("method"),
     dataType: 'json',
     success: function (data) {
       if (data.form_is_valid) {
        $("#modal-document").modal("hide");
         alert("Document is deleted")
         
       $("#document_table tbody").html(data.html_document_list);


       }
       else {
         $("#modal-document .modal-content").html(data.html_form);
       }
     }
   });
   return false;
 
 
  }
 
  var loadDeleteForm = function () {
    console.log("Sucessfully Triggered Document Delete Event........")
    var btn = $(this);
    console.log(btn.attr("data-url"));
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      
      beforeSend: function () {
        $("#modal-document .modal-content").html("");
        $("#modal-document").modal("show");
      },
      success: function (data) {
        $("#modal-document .modal-content").html(data.html_form);
      }
    });
  };


 //Binding Document Create Button 
 $(".js-document-create-button").click(loadForm);
 $("#modal-document").on("submit",".js-document-create-form",saveForm);

 //Binding update document
 $(".js-update-document-button").click(loadForm);
 $("#modal-document").on("submit",".js-document-update-form",saveForm);

//Binding delete document
//js-document-delete-button
//js-document-delete-form
$(".js-document-delete-button").click(loadDeleteForm );
$("#modal-document").on("submit",".js-document-delete-form",saveDeleteForm);


});
