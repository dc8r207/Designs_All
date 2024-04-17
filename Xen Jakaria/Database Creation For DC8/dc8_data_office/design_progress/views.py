from io import BytesIO
from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from django.template.loader import render_to_string
from .forms import design_work_form
#logging related setup
import datetime
import logging

from .models import design_work,design_work_progress,designer
# Get an instance of a logger
logger = logging.getLogger('django')

# Create your views here.
from .auxilary_query import *
#importing loginrequired authentication
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    #return HttpResponse("PAGE IS UNDER CONSTRUCTION")
    user=request.user
    log_msg="Progress was accessed at"+str(datetime.datetime.now())+" hours!"
    logger.info(log_msg)
    designs=design_work.objects.all()
    designs=get_design_for_current_user(user)
    progress_entries=create_design_progrss_table_entry(designs)
    context={"designs":designs,"pes":progress_entries}
    print("progress of design::::::::::::::")
    #return HttpResponse("PAGE IS UNDER CONSTRUCTION")
    """"  
    for d in designs:
        print("{}   {} {}".format(d.drawing_no,d.pdf_drw,d.dxf_drw))  
    """    
    post=designer.objects.get(user_name=user).post 
    if post=="Superintending Engineer":
        return  render(request,"design_progress/index_se.html",context)
    else:
        return  render(request,"design_progress/index.html",context)
      

    



from .auxilary_query import *
from .models import design_work_progress,progress_mile_stone

def create_design_work(request):
    data =dict()
    if request.method =="POST":
        form=design_work_form(request.POST)
        if form.is_valid():
            new_work=form.save()                
            create_first_progress_entry(new_work) #creating first progress entry
            data['form_is_valid']=True
            designs=design_work.objects.all()
            progress_entries=create_design_progrss_table_entry(designs)
            #data['html_work_list']=render_to_string('design_progress/includes/partial_work_list.html', {'designs':designs})
            data['html_work_list']=render_to_string('design_progress/includes/partial_work_list.html', 
                                                    {"designs":designs,"pes":progress_entries})
            
        else:
            data['form_is_valid']=False
    else:
        form=design_work_form()
        
    
    
    context={'form':form}
    data['html_form']=render_to_string("design_progress/includes/create_design_work.html",
                 context,request=request)
    #return JsonResponse({'html_form':html_form})
    return JsonResponse(data)


from .forms import design_work_progress_form  
from .auxilary_query import get_current_progress,save_progress_update
#(progress_form,work_name) 
def update_design_progress(request,pk):
    print(request)
    data=dict()
    #print("getting design desig work..............")
    design=design_work.objects.get(pk=pk)
    #print(design)
    cp=get_current_progress(design)
    
    if request.method=="POST":
        print("processing post reques....................")        
        form=design_work_progress_form(request.POST)
        #print(form)
        if form.is_valid():
            print("Form is valid...........") 
            #new_work=form.save()                
            #create_first_progress_entry(new_work) #creating first progress entry
            save_progress_update(form,design)
            data['form_is_valid']=True
            designs=design_work.objects.all()
            progress_entries=create_design_progrss_table_entry(designs)
            #data['html_work_list']=render_to_string('design_progress/includes/partial_work_list.html', {'designs':designs})
            data['html_work_list']=render_to_string('design_progress/includes/partial_work_list.html', 
                                                  {"designs":designs,"pes":progress_entries})
            
        else:
            print("Form is invalid")
            data['form_is_valid']=False
        
        
    else:
        #design_work_name=forms.ModelChoiceField(design_work.objects.all())
        #current_progress=forms.ModelChoiceField(progress_mile_stone.objects.all(),widget=forms.TextInput(attrs={'readonly': 'readonly'}))
        #updated_progress=forms.ModelChoiceField(progress_mile_stone.objects.all())    
        #date=forms.DateField(initial=tz.now)
        intial_values={"current_progress":cp,"design_work_name":design}
        print("This is a get request...............")
        form=design_work_progress_form(initial=intial_values)
        #print(form)
    context={'form':form,"design":design}
    data['html_form']=render_to_string("design_progress/includes/update_design_progress_form.html",
                 context,request=request)
    #print(data['html_form'])
    return JsonResponse(data)    
    #return HttpResponse("The page is under construction........")

def update_design_progress2(request,pk):
    data=dict()
    #print("getting design desig work..............")
    design=design_work.objects.get(pk=pk)
    cp=get_current_progress(design)
    if request.method=="POST":
        form=design_work_progress_form(request.POST)
        data['form_is_valid']=True
        designs=design_work.objects.all()
        progress_entries=create_design_progrss_table_entry(designs)
        #data['html_work_list']=render_to_string('design_progress/includes/partial_work_list.html', {'designs':designs})
        data['html_work_list']=render_to_string('design_progress/includes/partial_work_list.html', 
                                                    {"designs":designs,"pes":progress_entries})
        
    else:
        intial_values={"current_progress":cp,"design_work_name":design}
        print("This is a get request...............")
        form=design_work_progress_form(initial=intial_values)
    context={'form':form,"design":design}
    data['html_form']=render_to_string("design_progress/includes/update_design_progress_form.html",
                 context,request=request)
    #print(data['html_form'])
    return JsonResponse(data)

from .forms import design_data_add_form
from .auxilary_query import saveDesignData,create_and_save_design_document
def add_design_data(request,pk):
    data=dict()
    #print("getting design desig work..............")
    design=design_work.objects.get(pk=pk)
    #cp=get_current_progress(design)
    if request.method=="POST":
        #form=design_work_progress_form(request.POST)        
        print("processing post request........")
        print(request.FILES['forwarding_doc'])
        doc_types=list(document_type.objects.all())
        
        
        """ 
        forwarding_doc
        technical_report_doc
        cross_section_doc
        long_section_doc
        bore_log_doc
        instance.doc_description=request.POST['doc_description']
        """
        #design,pdf_file,document_name,doc_type
        #saving forwarding
        forwarding=request.FILES['forwarding_doc']        
        doc_name="Forawrding for"+str(design)
        create_and_save_design_document(design,forwarding,doc_name,doc_types[1])
        
        #saving Technical Reports        
        technical_report=request.FILES['technical_report_doc']
        #saveDesignData(request,design)
        doc_name="Technical Report for"+str(design)
        create_and_save_design_document(design,technical_report,doc_name,doc_types[2])        
        
        #saving cross_section       
        cross_section =request.FILES['cross_section_doc']
        #saveDesignData(request,design)
        doc_name="Cross Section for"+str(design)
        create_and_save_design_document(design,cross_section ,doc_name,doc_types[3])
        
        #saving Long Section     
        long_section =request.FILES['long_section_doc']
        #saveDesignData(request,design)
        doc_name="Long Section for"+str(design)
        create_and_save_design_document(design,long_section ,doc_name,doc_types[4])
        
        #saving Bore Log    
        bore_log =request.FILES['bore_log_doc']        
        doc_name="Bore Log for"+str(design)
        create_and_save_design_document(design,bore_log ,doc_name,doc_types[5])    
        
        form=design_data_add_form()
        data['form_is_valid']=True
        designs=design_work.objects.all()
        progress_entries=create_design_progrss_table_entry(designs)
        #data['html_work_list']=render_to_string('design_progress/includes/partial_work_list.html', {'designs':designs})
        data['html_work_list']=render_to_string('design_progress/includes/partial_work_list.html', 
                                                    {"designs":designs,"pes":progress_entries})
        
    else:
        #intial_values={"current_progress":cp,"design_work_name":design}
        #print("This is a post request..............")
        form=design_data_add_form()
        #form=design_work_progress_form()
        #print(form)
    context={'form':form,"design":design}
     
    data['html_form']=render_to_string("design_progress/includes/add_design_data_form.html",
                 context,request=request)
    
    """  
    data['html_form']=render_to_string("design_progress/includes/update_design_progress_form.html",
                 context,request=request)
    """
    
    #print(data['html_form'])
    return JsonResponse(data)
from django.http import FileResponse
from PyPDF2 import PdfWriter 
def download_design_data(request,pk):
    #img = open('images/bojnice.jpg', 'rb')
    #response = FileResponse(img)
    design=design_work.objects.get(pk=pk)
    print(design)
    docs=design_document.objects.filter(design=design)
    print(docs)
    buffer = BytesIO()
    merger = PdfWriter()
    if docs:
        for doc in docs:
            pdf=doc.document.pdf_doc
            merger.append(pdf)
            #print(doc.document)
    #pdf_file=docs[0].document.pdf_doc
    merger.write(buffer)
    merger.close()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename="dessign_data.pdf")
    return HttpResponse("Page is under construction")
    pass