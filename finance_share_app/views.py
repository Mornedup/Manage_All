from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from finance_share_app.logic import *
from finance_share_app.forms import *
from finance_share_app.models import *


# Create your views here.
@login_required
def upload_document(request):
    if request.method == 'POST':
        if request.FILES['file']:
            currentdoc = Document(docref=request.POST['docref'], file=request.FILES['file'], owner=request.user, notes=request.POST['notes'], created_date = timezone.now())
            currentdoc.save()
            return redirect('document_list')
    else:
        form = DocUploadForm()

    return render(request, 'finance_share_app/upload_document.html', {'form': form})

@login_required
def view_document_list(request):
    return render(request, 'finance_share_app/document_list.html', {'docs': Document.objects.filter(owner=request.user)})

@login_required
def view_document(request, pk):
    doc = get_object_or_404(Document, pk=pk)
    claims = Claim.objects.filter(docref=doc)
    return render(request, 'finance_share_app/view_document.html', {'doc': doc, 'claims':claims})

@login_required
def make_claim(request):
    if request.method == 'POST':
        claimForm = ClaimUploadForm(request.POST)
        if (claimForm.is_valid()):
            claim = claimForm.save(commit=False)
            claim.owner = request.user
            claim.created_date = timezone.now()
            claim.save()
            for user in CUser.objects.filter(pk__in=request.POST.getlist('checkbox')):
                UserClaimAllocate.objects.create(user=user, claim=claim)
            count = UserClaimAllocate.objects.filter(claim=claim).count()
            UserClaimAllocate.objects.filter(claim=claim).update(share_ammount=claim.ammount/(count))
            return redirect('claim_list')
    else:
        claimform = ClaimUploadForm()

    return render(request, 'finance_share_app/upload_claim.html', {'claimform': claimform, 'users':CUser.objects.all()})

@login_required
def view_claim_list(request):
    return render(request, 'finance_share_app/claim_list.html', {'claims': Claim.objects.filter(docref__owner=request.user)})

@login_required
def view_claim(request, pk):
    claim = get_object_or_404(Claim, pk=pk)
    users = UserClaimAllocate.objects.filter(claim=claim)
    return render(request, 'finance_share_app/view_claim.html', {'claim': claim, 'users':users})


@login_required
def report_select(request):
    if request.method == 'POST':
        pass
        daterange = {'start_date':request.POST['start_date'], 'end_date':request.POST['end_date']}
        owedtouser = calculate_owed_to_user(request.user, daterange)
        owedbyuser = calculate_owed_by_user(request.user, daterange)
        final = calculate_final_out(owedbyuser, owedtouser)
        type='Custom report'
        reportdata = compile_report(request.user, owedbyuser, owedtouser, final)
        return render(request, 'finance_share_app/report.html', {'type':type, 'reportdata':reportdata})
    else:
        return render(request, 'finance_share_app/report_select.html', {})

@login_required
def last_month_report(request):
    owedtouser = calculate_owed_to_user(request.user, get_default_date_range(-1))
    owedbyuser = calculate_owed_by_user(request.user, get_default_date_range(-1))
    final = calculate_final_out(owedbyuser, owedtouser)
    type='Last Complete Month Report'
    reportdata=compile_report(request.user, owedbyuser, owedtouser, final)
    return render(request, 'finance_share_app/report.html', {'type':type, 'reportdata':reportdata})

@login_required
def current_month_report(request):
    owedtouser = calculate_owed_to_user(request.user, get_default_date_range(0))
    owedbyuser = calculate_owed_by_user(request.user, get_default_date_range(0))
    final = calculate_final_out(owedbyuser, owedtouser)
    type='Current month provisional report'
    reportdata=compile_report(request.user, owedbyuser, owedtouser, final)
    return render(request, 'finance_share_app/report.html', {'type':type, 'reportdata':reportdata})

def finance_share_home(request):
    return render(request, 'finance_share_app/finance_share_home.html')

