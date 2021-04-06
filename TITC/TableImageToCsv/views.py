from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse
from .forms import UploadFileForm
from django.views.generic import TemplateView
# 画像処理ライブラリのimport
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
import pandas as pd

#pdfからcsvに変換するためのライブラリ
from tabula import read_pdf

def fileUpload(request):
  if request.method == 'POST':
    # ファイルデータの受け取り
    form = UploadFileForm(request.POST, request.FILES)
    if form.is_valid():
      file_obj = request.FILES['file']
      # handle_uploaded_file(file_obj)
      df = toPdf(file_obj)
      context = { 'df' : df}
      return render(request,'TableImageToCsv/result.html',context)
  else:
    form = UploadFileForm()
  return render(request,'TableImageToCsv/index.html',{'form':form})

# アップロードされた画像を保存する関数
def handle_uploaded_file(file_obj):
  file_path = 'media/documents/' + file_obj.name
  with open(file_path, 'wb+') as destination:
    for chunk in file_obj.chunks():
      destination.write(chunk)

# 画像をpdfにする関数
def toPdf(file_obj):
  # 画像をファイルから読み込む
  image = Image.open(file_obj)
  # 画像をNumpy配列に変換する
  image = np.asarray(image)


  # 画像のプロット先の準備
  fig = plt.figure()
  # グリッドの表示をOFFにする
  plt.axis('off')
  # Numpy配列を画像として表示する
  plt.imshow(image)

  # 保存するPDFファイル名
  pp = PdfPages(file_obj.name.split('.')[0]+'.pdf')
  # 画像をPDFとして保存する
  pp.savefig(fig)
  # PDFの保存終了
  pp.close()
  file_name = file_obj.name.split('.')[0] + '.pdf'

  df = read_pdf(file_name)
  pd.DataFrame(df[0]).to_csv(file_obj.name.split('.')[0]+'.csv',encoding='shift-jis')
  return df
