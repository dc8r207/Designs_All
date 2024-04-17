from django.shortcuts import render,HttpResponse

# Create your views here.
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required

from .models import  document

import datetime
import logging
logger = logging.getLogger('django')

#from .forms import BookForm


from design_progress.models import designer

@login_required
def document_list(request):
    #return HttpResponse("PAGE IS UNDER CONSTRUCTION")
    user=request.user
    log_msg="Documents app was accessed"+str(datetime.datetime.now())+" hours!"
    logger.info(log_msg)
    documents=document.objects.all()
    #designs=get_design_for_current_user(user)
    #progress_entries=create_design_progrss_table_entry(designs)
    context={"documents":documents}
    print("documents ....................")
    print(documents)
    #return HttpResponse("PAGE IS UNDER CONSTRUCTION")
    """"  
    for d in designs:
        print("{}   {} {}".format(d.drawing_no,d.pdf_drw,d.dxf_drw))  
    """    
    post=designer.objects.get(user_name=user).post 
    if post=="Superintending Engineer":
        return  render(request,"documents/index_se.html",context)
    else:
        return  render(request,"documents/index.html",context)
    
    
    designs = document.objects.all()
    return render(request, 'books/book_list.html', {'books': designs})
from .forms import document_form
from .models import document
from .models import document_type
def document_create(request):
    #return HttpResponse("The page is under construction...........")
    data=dict()
    if request.method=="POST":
        print("printing post request.............")
        print(request.POST)
        print("printing file request...............")
        print(request.FILES)
        #print(request.FILES["pdf_drw"])
        #print(request.FILES["dxf_drw"])
        form=document_form(request.POST,request.FILES)
        if form.is_valid:
            #print(form)
            #form.save()                        
            instance=document()
            instance.doc_description=request.POST['doc_description']
            instance.doc_type=document_type.objects.get(id=request.POST['doc_type']  )           
            print(request.FILES)
            instance.pdf_doc=request.FILES["pdf_doc"]
            #instance.dxf_drw=request.FILES["dxf_drw"]
            instance.save()
            data["form_is_valid"]=True
            documents=document.objects.all()
            #designs = design.objects.all()
            data['html_document_list'] = render_to_string('documents/includes/partial_document_list.html', {
                'documents': documents
            })
            log_msg=instance.doc_description+"was created at"+str(datetime.datetime.now())+" hours!"
            logger.info(log_msg)
        else:
            data["form_is_valid"]=False
    else:
        form=document_form()
    context={'form':form}
    data['html_form']=render_to_string('documents/includes/partial_document_create.html',
        context,request=request)
    print(data['html_form'])     
    return JsonResponse(data)

def document_update(request,pk):
    instance = get_object_or_404(document, pk=pk)
    data=dict()
    if request.method=="POST":
        print("printing post request.............")
        print(request.POST)
        print("printing file request...............")
        print(request.FILES)
        #print(request.FILES["pdf_drw"])
        #print(request.FILES["dxf_drw"])
        #form=document_form(request.POST,request.FILES)
        form=document_form(request.POST,instance=instance)
        if form.is_valid:
            #print(form)
            #form.save()                        
            #instance=document()
            instance.doc_description=request.POST['doc_description']
            instance.doc_type=document_type.objects.get(id=request.POST['doc_type']  )           
            print(request.FILES)
            instance.pdf_doc=request.FILES["pdf_doc"]
            #instance.dxf_drw=request.FILES["dxf_drw"]
            instance.save()
            data["form_is_valid"]=True
            documents=document.objects.all()
            #designs = design.objects.all()
            data['html_document_list'] = render_to_string('documents/includes/partial_document_list.html', {
                'documents': documents
            })
            log_msg=instance.doc_description+"was created at"+str(datetime.datetime.now())+" hours!"
            logger.info(log_msg)
        else:
            data["form_is_valid"]=False
    else:
        form=document_form(instance=instance)
    context={'form':form}
    data['html_form']=render_to_string('documents/includes/partial_document_update_form.html',
        context,request=request)
    print(data['html_form'])     
    return JsonResponse(data)
    pass




def document_delete(request,pk):
    instance = get_object_or_404(document,pk=pk)
    data = dict()
    if request.method == 'POST':
        instance.delete()
        data['form_is_valid'] = True
        documents=document.objects.all()
            #designs = design.objects.all()
        data['html_document_list'] = render_to_string('documents/includes/partial_document_list.html', {
                'documents': documents
            })
        
        log_msg=instance.doc_description+"was deleted at"+str(datetime.datetime.now())+" hours!"
        logger.info(log_msg)

    else:
        context = {'document': instance}
        data['html_form'] = render_to_string('documents/includes/partial_document_delete_form.html', context, request=request)
    return JsonResponse(data)
    pass 




  
"""   
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
    




"""


# Create your views here.
