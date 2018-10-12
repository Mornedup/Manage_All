from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .logic import CalcOwedToUser, CalcOwedByUser, GetDefaultDateRange, CalcFinalout, CompileReport
from authapp.models import CUser

# Create your views here.
@login_required
def reportselect(request):
    if request.method == 'POST':
        pass
        daterange = {'start_date':request.POST['start_date'], 'end_date':request.POST['end_date']}
        owedtouser = CalcOwedToUser(request.user, daterange)
        owedbyuser = CalcOwedByUser(request.user, daterange)
        final = CalcFinalout(owedbyuser, owedtouser)
        type='Custom report'
        reportdata=CompileReport(request.user, owedbyuser, owedtouser, final)
        return render(request, 'allocations/report.html', {'type':type, 'reportdata':reportdata})
    else:
        return render(request, 'allocations/reportsellect.html', {})

@login_required
def lastmonthreport(request):
    owedtouser = CalcOwedToUser(request.user, GetDefaultDateRange(-1))
    owedbyuser = CalcOwedByUser(request.user, GetDefaultDateRange(-1))
    final = CalcFinalout(owedbyuser, owedtouser)
    type='Last Complete Month Report'
    reportdata=CompileReport(request.user, owedbyuser, owedtouser, final)
    return render(request, 'allocations/report.html', {'type':type, 'reportdata':reportdata})

@login_required
def currentmonthreport(request):
    owedtouser = CalcOwedToUser(request.user, GetDefaultDateRange(0))
    owedbyuser = CalcOwedByUser(request.user, GetDefaultDateRange(0))
    final = CalcFinalout(owedbyuser, owedtouser)
    type='Current month provisional report'
    reportdata=CompileReport(request.user, owedbyuser, owedtouser, final)
    return render(request, 'allocations/report.html', {'type':type, 'reportdata':reportdata})
