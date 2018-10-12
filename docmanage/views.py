from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from docmanage.forms import DocUploadForm
from django.utils import timezone
from .models import Doc

# Create your views here.
@login_required
def upload_doc(request):
    if request.method == 'POST':
        if request.FILES['file']:
            currentdoc = Doc(docref=request.POST['docref'], file=request.FILES['file'], owner=request.user, notes=request.POST['notes'], created_date = timezone.now())
            currentdoc.save()
            return redirect('doc_list')
    else:
        form = DocUploadForm()
        return render(request, 'docmanage/uploaddoc.html', {'form': form})

@login_required
def view_doc(request):
    return render(request, 'docmanage/doclist.html', {'docs': Doc.objects.filter(owner=request.user)})
