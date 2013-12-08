from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.loader import get_template
from django.template import RequestContext
from django.contrib import messages

from form import UploadForm, NewPersonForm, SelectPersonForm
from models import UploadFile, TextRecRes, FaceRecRes, Person
from tagit.settings import STATICFILES_DIRS, PROJ_ROOT
from django.views.decorators.csrf import csrf_protect
import text_recognition
import face_detection
import os

@csrf_protect
def mark_person_page(request, face_id):
    template = get_template("mark_person.html")
    img = FaceRecRes.objects.filter(id=face_id).first()
    if request.method == 'POST':
        npf = NewPersonForm(request.POST)
        spf = SelectPersonForm(request.POST)
        if npf.is_valid():
            name = npf.cleaned_data.get('Name',False)
            pers = Person(Name=name)
            pers.save()
            img.Mark = pers
            img.save()
        elif spf.is_valid():
            pers = spf.cleaned_data.get('PersonField',False)
            img.Mark = pers
            img.save()
    to_rec_name = os.path.join(PROJ_ROOT, img.FileName)
    print face_detection.face_dnr.recognize_person(to_rec_name,Person.objects.all())
    context = RequestContext(request, {
        'img' : img,
        'formSelect' : SelectPersonForm(),
        'formNew' : NewPersonForm(),
    })
    return HttpResponse(template.render(context))

@csrf_protect
def welcome_page(request):
    template = get_template("main.html")     
    data = ''
    if request.method == 'POST':
        uploadform = UploadForm(request.POST, request.FILES)
        if uploadform.is_valid():
            f = request.FILES['File']
            new_file = UploadFile(FileName=f.name,File=f)
            new_file.save()
            file_path = os.path.join(PROJ_ROOT, str(new_file.File))
            data = text_recognition.text_recognition.pipline(file_path, os.path.join(STATICFILES_DIRS[0], 'text_rec'))
            text_rec = [TextRecRes(Rects=str(x[0]), Text=x[1], FK_UFile=new_file) for x in data]
            map(lambda x: x.save(), text_rec)
            faces = face_detection.face_dnr.detect_faces(file_path, os.path.join(STATICFILES_DIRS[0], 'face_rec'))
            face_rec = [FaceRecRes(Rects=str(x[1]), FK_UFile=new_file, FileName=x[0][len(STATICFILES_DIRS[0]) - len('static/'):]) for x in faces]
            map(lambda x: x.save(), face_rec)


    uploadform = UploadForm()
    up_files = UploadFile.objects.all().order_by('-id')
    for x in up_files:
        x.info = TextRecRes.objects.filter(FK_UFile=x)
        x.people = FaceRecRes.objects.filter(FK_UFile=x)
        x.num_of_people = len(x.people)
    
    context = RequestContext(request, {
        'form' : uploadform,
        'up_files' : up_files[:10]
    })
    return HttpResponse(template.render(context))

# Create your views here.
