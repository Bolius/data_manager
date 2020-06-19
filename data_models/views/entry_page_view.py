from django.shortcuts import render


def EntryPage(request):
    return render(request, "data_models/entry_page.html", {})
