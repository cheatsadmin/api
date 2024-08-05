from django.db.models import QuerySet

from cheatgame.issue.filter import IssueReportFilter
from cheatgame.issue.filters import IssueFilter
from cheatgame.issue.models import Issue, Tag, IssueReport
from cheatgame.users.models import BaseUser


def issue_list(*, filters=None) -> QuerySet[Issue]:
    filters = filters or {}
    qs = Issue.objects.all()
    return IssueFilter(filters, qs).qs


def get_tag_list(*, issue_type) -> QuerySet[Tag]:
    return Tag.objects.filter(issue_type=issue_type)

def issue_report_user(* , user: BaseUser) -> QuerySet[IssueReport]:
    return IssueReport.objects.filter(user=user)



def get_tag_list_of_issue(* , issue_id:int)-> QuerySet[Tag]:
    return Tag.objects.filter(issue_id=issue_id)
def issue_report_list(* , filters=None) -> QuerySet[IssueReport]:
    filters = filters or {}
    qs = IssueReport.objects.all()
    return IssueReportFilter(filters , qs).qs


