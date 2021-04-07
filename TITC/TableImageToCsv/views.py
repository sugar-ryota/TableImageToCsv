from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse
from .forms import UploadFileForm

import pandas as pd

#pdfからcsvに変換するためのライブラリ
from tabula import read_pdf

def fileUpload(request):
  if request.method == 'POST':
    # ファイルデータの受け取り
    form = UploadFileForm(request.POST, request.FILES)
    if form.is_valid():
      file_obj = request.FILES['file']
      handle_uploaded_file(file_obj)
      toCsv(file_obj)
      context = {
         'success': '成功！',
         }
      return render(request,'TableImageToCsv/result.html',context)
  else:
    form = UploadFileForm()
  return render(request, 'TableImageToCsv/index.html', {'form': form})

# 受け取ったpdfファイルを保存する関数
def handle_uploaded_file(file_obj):
  file_path = file_obj.name
  with open(file_path, 'wb+') as destination:
    for chunk in file_obj.chunks():
      destination.write(chunk)

# 表pdfをcsvにする関数
def toCsv(file_obj):
  file_name = file_obj.name.split('.')[0] + '.pdf'
  df = read_pdf(file_name)
  csv_file = file_obj.name.split('.')[0] + '.csv'
  # １つのページに複数の表があるときはdfの配列番号を指定すると良い
  pd.DataFrame(df[0]).to_csv(csv_file, encoding='shift-jis')
