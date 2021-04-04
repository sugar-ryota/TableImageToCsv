from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse
from .forms import UploadFileForm

def fileUpload(request):
  if request.method == 'POST':
    # ファイルデータの受け取り
    form = UploadFileForm(request.POST, request.FILES)
    if form.is_valid():
      handle_uploaded_file(request.FILES['file'])
      file_obj = request.FILES['file']
      return HttpResponse('成功')
  else:
    form = UploadFileForm()
  return render(request,'TableImageToCsv/index.html',{'form':form})

def handle_uploaded_file(file_obj):
  file_path = 'media/documents/' + file_obj.name
  with open(file_path, 'wb+') as destination:
    for chunk in file_obj.chunks():
      destination.write(chunk)
