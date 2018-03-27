from .forms import BugReportForm


def bug_report_form(request):
    return {
        'bug_report_form': BugReportForm(initial={
            'source_url': request.path,
            'source': 'wheredoivote',
        })
    }
