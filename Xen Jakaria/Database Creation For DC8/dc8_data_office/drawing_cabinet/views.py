from django.shortcuts import render,redirect,get_object_or_404
from.models import design
from django.core.files.storage import FileSystemStorage
from .forms import design_form
from django.template.loader import render_to_string
from django.http import JsonResponse
from .models import design

#logging related setup
import datetime
import logging
# Get an instance of a logger
logger = logging.getLogger('django')



def index(request):
    log_msg="Homepage was accessed at"+str(datetime.datetime.now())+" hours!"
    logger.info(log_msg)
    designs=design.objects.all()
    context={"designs":designs}
    print("printing drawing list::::::::::::::")
    for d in designs:
        print("{}   {} {}".format(d.drawing_no,d.pdf_drw,d.dxf_drw))
      
    #return render()
    return  render(request,"drawing_cabinet/index.html",context)

def upload_pdf(request):
    context={}
    if request.method=="POST":                
        pdf_file=request.FILES["drwg_pdf"]
        fs=FileSystemStorage()
        name=fs.save(pdf_file.name,pdf_file)
        url=fs.url(name)
        print("uploaded files url.....")
        print(url)
        #print(pdf_file.name)
        #print(pdf_file.size) 
        context['url']=fs.url(name)   
    return  render(request,"drawing_cabinet/upload_pdf.html",context) 

def upload_design(request):    
    data=dict()
    if request.method=="POST":
        print("printing post request.............")
        print(request.POST)
        print("printing file request...............")
        print(request.FILES)
        #print(request.FILES["pdf_drw"])
        #print(request.FILES["dxf_drw"])
        form=design_form(request.POST,request.FILES)
        if form.is_valid:
            #print(form)
            #form.save()                        
            instance=design()
            instance.drawing_no=request.POST['drawing_no']            
            print(request.FILES)
            instance.pdf_drw=request.FILES["pdf_drw"]
            instance.dxf_drw=request.FILES["dxf_drw"]
            instance.save()
            data["form_is_valid"]=True
            
            designs = design.objects.all()
            data['html_design_list'] = render_to_string('drawing_cabinet/partial_drawing_list.html', {
                'designs': designs
            })
            log_msg=instance.drawing_no+"was created at"+str(datetime.datetime.now())+" hours!"
            logger.info(log_msg)
        else:
            data["form_is_valid"]=False
    else:
        form=design_form()
    context={'form':form}
    data['html_form']=render_to_string('drawing_cabinet/includes/partial_design_upload_form.html',
        context,request=request)
            
    return JsonResponse(data)

def update_design(request,pk):
    print(request)
    instance = get_object_or_404(design, pk=pk)
    data=dict()
    if request.method=="POST":
        print("printing post request.............")
        print(request.POST)
        print("printing file request...............")
        print(request.FILES)
        #print(request.FILES["pdf_drw"])
        #print(request.FILES["dxf_drw"])
        form=design_form(request.POST,instance=instance)
        if form.is_valid:
            #print(form)
            #form.save()                        
            
            instance.drawing_no=request.POST['drawing_no']            
            print(request.FILES)
            instance.pdf_drw=request.FILES["pdf_drw"]
            instance.dxf_drw=request.FILES["dxf_drw"]
            instance.save()
            data["form_is_valid"]=True            
            designs = design.objects.all()
            data['html_design_list'] = render_to_string('drawing_cabinet/partial_drawing_list.html', {
                'designs': designs
            })
            log_msg=instance.drawing_no+"was updated at"+str(datetime.datetime.now())+" hours!"
            logger.info(log_msg)
        else:
            data["form_is_valid"]=False
    else:
        form=design_form(instance=instance)
    context={'form':form}
    data['html_form']=render_to_string('drawing_cabinet/includes/partial_design_update_form.html',
        context,request=request)
            
    return JsonResponse(data) 


def delete_design(request,pk):
    instance = get_object_or_404(design,pk=pk)
    data = dict()
    if request.method == 'POST':
        instance.delete()
        data['form_is_valid'] = True
        designs = design.objects.all()
        data['html_design_list'] = render_to_string('drawing_cabinet/partial_drawing_list.html', {
                'designs': designs            })
        
        log_msg=instance.drawing_no+"was deleted at"+str(datetime.datetime.now())+" hours!"
        logger.info(log_msg)

    else:
        context = {'design': instance}
        data['html_form'] = render_to_string('drawing_cabinet/includes/partial_design_delete_form.html', context, request=request)
    return JsonResponse(data)
    
    pass

    form=design_form()
    context={'form':form}
    html_form=render_to_string('drawing_cabinet/includes/partial_design_upload_form.html',
        context,
        request=request,)
    #print(JsonResponse({html_form:'html_form'}))
    return JsonResponse({'html_form': html_form})
    
    
# Create your views here.
