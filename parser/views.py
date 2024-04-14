from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.views.generic import View
from django.contrib import messages
import os

from .models import CV
from .forms import CVUploadForm
from .utils import extract_data_from_cv, generate_xls, extract_data_from_docx, extract_data_from_doc, extract_text



class CVUploadView(View):
    def get(self, request):
        form = CVUploadForm()
        return render(request, 'parser/cv_upload.html', {'form': form})

    def post(self, request):
        form = CVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            cv = form.save(commit=False)
            file_name = request.FILES['file'].name
            with open(f'media/cv_files/{file_name}', 'wb+') as destination:
                for chunk in request.FILES['file'].chunks():
                    destination.write(chunk)
            if file_name.endswith('.pdf'):
                email, phone, text_content = extract_data_from_cv(cv.file)
            elif file_name.endswith('.doc'):
                email, phone, text_content = extract_data_from_doc(cv.file)
            elif file_name.endswith('.docx'):
                email, phone, text_content = extract_data_from_docx(cv.file)
            else:
                messages.error(request, 'Invalid file format. Please upload a PDF or DOCX file.')
                return render(request, 'parser/cv_upload.html', {'form': form})
            cv.email = email
            cv.contact_number = phone
            cv.text_content = text_content
            cv.save()
            messages.success(request, 'CV uploaded successfully!')
            return redirect('cv_upload')
        else:
            messages.error(request, 'Failed to upload CV. Please check the form.')
        return render(request, 'parser/cv_upload.html', {'form': form})
class CVDataView(View):
    def get(self, request):
        cvs = CV.objects.all()
        xls_file = generate_xls(cvs)
        with open(xls_file, 'rb') as file:
            response = HttpResponse(file.read(), content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = f'attachment; filename={os.path.basename(xls_file)}'
            return response