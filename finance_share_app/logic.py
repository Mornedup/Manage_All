from finance_share_app.models import *
import datetime


def get_default_date_range(offset=0):
    # offset will be the amount of months back you want to move your range
    startdate = datetime.datetime.now()
    startdate = startdate.replace(month=startdate.month + offset)
    if startdate.month == 1:
        startdate.replace(year=startdate.year - 1, month=12, day=26)
    else:
        startdate = startdate.replace(month=startdate.month - 1, day=26)


    enddate = datetime.datetime.now()
    enddate = enddate.replace(month=startdate.month + offset)
    if enddate.month == 1:
        enddate = enddate.replace(year=enddate.year - 1, month=12, day=25)
    else:
        enddate = enddate.replace(day=25)
    daterange = {'start_date': startdate.date(), 'end_date': enddate.date()}
    return (daterange)


def calculate_owed_to_user(user, daterange):
    docs = Document.objects.filter(owner=user,
                                   created_date__range=[daterange.get('start_date'), daterange.get('end_date')])
    totals = {}
    for doc in docs:
        claims = Claim.objects.filter(docref=doc)
        for claim in claims:
            for share in UserClaimAllocate.objects.filter(claim=claim):
                if share.user != user:
                    if share.user in totals:
                        totals[share.user] += share.share_amount
                    else:
                        totals[share.user] = share.share_amount
    return (totals)


def calculate_owed_by_user(user, daterange):
    toshare = UserClaimAllocate.objects.filter(user=user,
                                               claim__docref__created_date__range=[daterange.get('start_date'),
                                                                                   daterange.get('end_date')])
    totals = {}
    for share in toshare:
        if user != share.claim.docref.owner:
            if share.claim.docref.owner in totals:
                totals[share.claim.docref.owner] += share.share_amount
            else:
                totals[share.claim.docref.owner] = share.share_amount
    return (totals)


def calculate_final_out(owedbyuser, owedtouser):
    finalout = {}
    for user in owedbyuser:
        if user in owedtouser:
            result = owedtouser[user] - owedbyuser[user]
        else:
            result = owedbyuser[user] * (-1)
        finalout[user] = result

    for user in owedtouser:
        if user not in finalout:
            finalout[user] = owedtouser[user]

    return (finalout)


def compile_report(owedbyuser, owedtouser, finalout):
    return ({'owedbyuser': owedbyuser, 'owedtouser': owedtouser, 'finalout': finalout})


def add_edit_claim_share(claim, shares):
    #clear current shares for the current claim
    UserClaimAllocate.objects.filter(claim=claim).delete()


    #write new sahre entries
    for user in shares:
        UserClaimAllocate.objects.create(user=user, claim=claim)
    count = UserClaimAllocate.objects.filter(claim=claim).count()
    UserClaimAllocate.objects.filter(claim=claim).update(share_amount=int(claim.amount) / count)
