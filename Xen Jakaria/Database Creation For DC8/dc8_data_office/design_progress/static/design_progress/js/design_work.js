 $(function () {
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

  var loadDesignDataForm = function () {
    console.log("Sucessfully Triggered Add Design Data.....")
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
  var saveDesignDataForm = function () {
    var form = $(this);
    console.log(typeof form)
    //console.log(form)
    var fd=new FormData();
    //console.log(fd)
    console.log("processing Design Data  form submit event......");
    //console.log($("#id_doc_description").val());
    var url_send=form.attr("action")
    //print(url_send)
    //id_technical_report
    //id_cross_section
    //id_long_section
    //id_bore_log
    var forwarding_doc=$("#id_forawarding")[0].files[0];
    var technical_report_doc=$("#id_technical_report")[0].files[0];
    var cross_section_doc=$("#id_technical_report")[0].files[0];
    var long_section_doc=$("#id_technical_report")[0].files[0];
    var bore_log_doc=$("#id_technical_report")[0].files[0];
    
    
    fd.append("forwarding_doc",forwarding_doc,forwarding_doc.name);
    fd.append("technical_report_doc",technical_report_doc,technical_report_doc.name);
    fd.append("cross_section_doc",cross_section_doc,cross_section_doc.name);
    fd.append("long_section_doc",long_section_doc,long_section_doc.name);
    fd.append("bore_log_doc",bore_log_doc,bore_log_doc.name);
    //getting csrf token
    var csrftoken = $("[name=csrfmiddlewaretoken]").val();
   
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
          
          alert("Drawing is Saved")
          $("#modal-drawing").modal("hide");
          $("#drawing_table tbody").html(data.html_document_list);

        }
        else {
          $("#modal-drawing .modal-content").html(data.html_form);
        }
      },
      timeout: 6000
    });
    return false;
  };

 //Binding create design work
 $(".js-design-create-button").click(loadForm);
 $("#modal-drawing").on("submit",".js-design-work-create-form",saveDesignWork);

 //Binding update progress
 $(".js-update-design-progress-button").click(loadForm);
 $("#modal-drawing").on("submit",".js-update-design-progress-form",saveDesignProgress);
 
 //Binding add Design Data Form
 $(".js-add-design-data-button").click(loadDesignDataForm);
 $("#modal-drawing").on("submit",".js-add-design-data-form",saveDesignDataForm);


});
