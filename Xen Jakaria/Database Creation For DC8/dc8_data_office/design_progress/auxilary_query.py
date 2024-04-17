class design_progress_entry:
    def __init__(self,design_work):
        self.design=design_work
    def add_current_progress(self,milestone):
        self.cuurent_porgess=milestone
from .models import design_work_progress

def create_design_progrss_table_entry(designs):
    progress_entrires=[]
    for d in designs:
        pe=design_progress_entry(d)
        progress_status=design_work_progress.objects.filter(work_name=d).order_by('-update_date','-work_status')            
        #print(progress_status)
        if progress_status:
            #print("adding progress to wqork....")            
            pe.add_current_progress(progress_status[0])
            progress_entrires.append(pe)
    return progress_entrires
from .models import design_work_progress,progress_mile_stone
from django.utils import timezone as tz

def create_first_progress_entry(d_work):
    print("creating first progress entry for work:{}".format(d_work))
    ms=progress_mile_stone.objects.get(id=16)   
    print("Created progress milestone........")
    udate=tz.now
    print("created time..............")
    dwp=design_work_progress()
    print("Created First Progress Entry....................")
    #work_name=d_work,work_status=ms,update_date=udate
    dwp.work_name=d_work
    dwp.work_status=ms
    dwp.save()
    print("Sucessfully Saved First Progress Entry............") 
    
    
    
def get_current_progress(d_work):
    #print("Cursor in get_current_progress")
    progress_status=design_work_progress.objects.filter(work_name=d_work).order_by('-update_date','-work_status')
    #print(progress_status)
    if progress_status:
        cp=progress_status[0].work_status
    else:
        cp=progress_mile_stone.objects.get(id=16)
    #print("\n\n")
    #print("current progress:{}".format(cp))
    return cp
def save_progress_update(progress_form,work_name):
    ms=progress_form.cleaned_data['updated_progress']
    cdate=progress_form.cleaned_data['date']
    dwp=design_work_progress()
    dwp.work_name=work_name
    dwp.work_status=ms
    dwp.save()
    print("sucessfully saved progress form..........")
from .models import design_work
def get_design_for_current_user(user):
    designs=list(design_work.objects.all())
    print("all design:{}".format(designs))
    designs_ongoing=list(design_work.objects.filter(work_completion_status__initial="OG"))
    print("on going design:{}".format(designs_ongoing))
    print(user)
    user_design=[]
    for d in designs_ongoing:
        if d.approver_name.user_name==user:
            print("{} is approver for {}".format(user,d.work_name))
            user_design.append(d)
            
        if d.reviewer_name.user_name==user:
            print("{} is reviewer for {}".format(user,d.work_name))
            user_design.append(d)
            
        if d.checker_name.user_name==user:
            print("{} is checker for {}".format(user,d.work_name))
            user_design.append(d)
            
        if d.designer_name.user_name==user:
            print("{} is designer for {}".format(user,d.work_name))
            user_design.append(d)
        
    return user_design
    pass

from documents.models import document,document_type
from .models import design_document
def create_and_save_design_document(design,pdf_file,document_name,doc_type):
    new_doc=document()
    #instance=document()
    new_doc.doc_description=document_name
    new_doc.pdf_doc=pdf_file
    new_doc.doc_type=doc_type
    new_doc.save()
    
    dd=design_document()
    dd.design=design
    dd.document=new_doc
    dd.save()
    return new_doc
    #new_doc.doc_type=document_type.objects.get(id=request.POST['doc_type']  )           
    
    #print(request.FILES)
    
   
    
    #instance.dxf_drw=request.FILES["dxf_drw"]
    
    

def saveDesignData(request,design):
    print("Saving Design Data for {}".format(design))
    doc_types=list(document_type.objects.all())
    for doc_type in doc_types:
        print("id={} doc_type={}".format(doc_type.id,doc_type))
    pass
    print(request.Files)
    #saving forwarding document
    
    #fl=request.FILES['forwarding_doc']
    #instance.pdf_doc=request.FILES["pdf_doc"]
""" 
 forwarding_doc
 technical_report_doc
 cross_section_doc
 long_section_doc
 bore_log_doc
 instance.doc_description=request.POST['doc_description']
"""


          

    