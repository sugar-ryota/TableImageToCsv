from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse
from .forms import UploadFileForm
# 画像処理ライブラリのimport
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages

import os

def fileUpload(request):
  if request.method == 'POST':
    # ファイルデータの受け取り
    form = UploadFileForm(request.POST, request.FILES)
    if form.is_valid():
      file_obj = request.FILES['file']
      # handle_uploaded_file(file_obj)
      toPdf(file_obj)
      return HttpResponse('成功')
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
  # # 画像をPDFとして保存する
  # pp.savefig(fig)
  # # PDFの保存終了
  # pp.close()
