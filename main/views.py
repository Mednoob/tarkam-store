from django.shortcuts import render

def show_main(request):
    context = {
        "message": "Coming soon!"
    }

    return render(request, "main.html", context)
