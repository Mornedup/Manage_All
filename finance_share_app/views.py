from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from finance_share_app.logic import *
from finance_share_app.models import *

# Create your views here.
util = ClaimUtils()
reportutil = ReportUtils()

@login_required
def manage_claims_view(request):
    documents = util.get_documents(request.user)
    docs = []
    for document in documents:
        current = {'pk': document.pk, 'claims': util.claims_to_text(Claim.objects.filter(docref=document)), 'docref': document.docref,
                   'purchasedate': document.purchasedate}
        docs.append(current)
    context = {
        'docs': docs
    }
    return render(request, 'finance_share_app/manage_claims.html', context)


@login_required
def view_claim(request, document_pk):
    document = util.get_document(document_pk)
    context = {
        'document': document,
        'claims': util.get_claims(document)
    }
    return render(request, 'finance_share_app/view_claim.html', context)


@login_required
def report_select(request):
    if request.method == 'POST':
        enddate=datetime.datetime.strptime(request.POST['end_date'], '%Y-%m-%d')
        daterange = {'start_date': request.POST['start_date'], 'end_date': enddate.replace(day=enddate.day+1)}
        context = {
            'type': 'Custom report',
            'reportdata': reportutil.generate_report_data(request.user, daterange),
        }
        return render(request, 'finance_share_app/report.html', context)
    return render(request, 'finance_share_app/report_select.html', {})


@login_required
def last_month_report(request):
    owedtouser = reportutil.calculate_owed_to_user(request.user, get_default_date_range(months=-1))
    owedbyuser = reportutil.calculate_owed_by_user(request.user, get_default_date_range(months=-1))
    final = reportutil.calculate_final_out(owedbyuser, owedtouser)
    reportdata = reportutil.compile_report(owedbyuser, owedtouser, final)
    type = 'Last Complete Month Report'
    # reportdata = reportutil.generate_report_data(request.user, get_default_date_range(-1))
    return render(request, 'finance_share_app/report.html', {'type': type, 'reportdata': reportdata})


@login_required
def current_month_report(request):
    # owedtouser = calculate_owed_to_user(request.user, get_default_date_range(0))
    # owedbyuser = calculate_owed_by_user(request.user, get_default_date_range(0))
    # final = calculate_final_out(owedbyuser, owedtouser)
    # reportdata = compile_report(owedbyuser, owedtouser, final)

    owedtouser = reportutil.calculate_owed_to_user(request.user, get_default_date_range())
    owedbyuser = reportutil.calculate_owed_by_user(request.user, get_default_date_range())
    final = reportutil.calculate_final_out(owedbyuser, owedtouser)
    reportdata = reportutil.compile_report(owedbyuser, owedtouser, final)
    type = 'Current month provisional report'
    return render(request, 'finance_share_app/report.html', {'type': type, 'reportdata': reportdata})


def finance_share_home(request):
    return render(request, 'finance_share_app/finance_share_home.html')


@login_required
def upload_new_claim(request):
    if request.method == 'POST':
        dateoffset = datetime.datetime.now() - datetime.datetime.strptime(request.POST['purchasedate'], '%Y-%m-%d')
        if dateoffset.days > 45:
            return render(request, 'finance_share_app/upload_new_claim.html', {'requestdata': request.POST})

        currentdoc = Document(docref=request.POST['docref'], file=request.FILES['file'], owner=request.user,
                              notes=request.POST['notes'], created_date=timezone.now(),
                              purchasedate=request.POST['purchasedate'])
        currentdoc.save()
        if 'saveadd' in request.POST:
            return redirect('add_claim', document_pk=currentdoc.pk)
        elif 'save' in request.POST:
            return redirect('view_claim', document_pk=currentdoc.pk)
    return render(request, 'finance_share_app/upload_new_claim.html')


@login_required
def add_claim(request, document_pk):
    document = get_object_or_404(Document, pk=document_pk)
    claims = Claim.objects.filter(docref=document)
    subcontext = {
        'description': '',
        'amount': '',
        'notes': ''
    }
    if request.method == 'POST':
        subcontext = {
            'description': request.POST['description'],
            'amount': request.POST['amount'],
            'notes': request.POST['notes']
        }

        currentclaim = Claim(docref=Document.objects.get(pk=document_pk), description=request.POST['description'],
                             amount=request.POST['amount'], notes=request.POST['notes'])
        currentclaim.save()

        share_list = CUser.objects.filter(pk__in=request.POST.getlist('checkbox'))
        add_edit_claim_share(currentclaim, share_list)

        if 'save' in request.POST:
            return redirect('view_claim', document_pk=document.pk)
        elif 'saveadd' in request.POST:
            return render(request, 'finance_share_app/edit_add_claim.html',
                          {'document': document, 'claims': claims, 'users': CUser.objects.all(),
                           'document_pk': document_pk, 'page': 'Add'})
    context = {
        'document': document,
        'claims': claims,
        'users': CUser.objects.all(),
        'context': subcontext,
        'page': 'Add'
    }
    return render(request, 'finance_share_app/edit_add_claim.html', context)


@login_required
def edit_claim(request, claim_pk, document_pk):
    document = get_object_or_404(Document, pk=document_pk)
    claims = Claim.objects.filter(docref=document).exclude(pk=claim_pk)
    edit_claim = Claim.objects.get(pk=claim_pk)
    shares = UserClaimAllocate.objects.filter(claim=edit_claim)
    shareusers = []
    for share in UserClaimAllocate.objects.filter(claim=edit_claim):
        shareusers.append(share.user)

    context = {
        'description': edit_claim.description,
        'amount': edit_claim.amount,
        'notes': edit_claim.notes,
        'shareusers': shareusers,
    }

    if request.method == 'POST':
        context = {'description': request.POST['description'],
                   'amount': request.POST['amount'],
                   'notes': request.POST['notes']}

        edit_claim.description = request.POST['description']
        edit_claim.amount = request.POST['amount']
        edit_claim.notes = request.POST['notes']
        edit_claim.save()

        share_list = CUser.objects.filter(pk__in=request.POST.getlist('checkbox'))
        add_edit_claim_share(edit_claim, share_list)

        if 'save' in request.POST:
            return redirect('view_claim', document_pk=document.pk)
        elif 'saveadd' in request.POST:
            claims = Claim.objects.filter(docref=document)
            return redirect('edit_add_claim', document=document, claims=claims, users=CUser.objects.all(), page='Add')
    context = {
        'document': document,
        'claims': claims,
        'shares': shares,
        'users': CUser.objects.all(),
        'page': 'Edit',
        'context': context
    }
    return render(request, 'finance_share_app/edit_add_claim.html', context)


@login_required
def info_claim(request, claim_pk):
    context ={
        'claim': util.get_claim(claim_pk),
        "users_shares": util.get_shares(claim_pk)
    }
    return render(request, 'finance_share_app/info_claim.html', context)
