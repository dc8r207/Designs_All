from django.shortcuts import render,redirect
from.models import design
from django.core.files.storage import FileSystemStorage
from .forms import design_form
def index(request):
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
    
    if request.method=="POST":
        form=design_form(request.POST,request.FILES)
        if form.is_valid:
            form.save()
            redirect("drawing_list")
    else:
        form=design_form()
                
    return render(request,"drawing_cabinet/upload_design.html",{"form":form})
    
# Create your views here.
