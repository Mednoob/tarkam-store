from django.shortcuts import render

def show_main(request):
    context = {
        "app_name": "Tarkam Store",
        "name": "Ahmad Yaqdhan",
        "class": "PBP A",
        "npm": 2406399081,
        "message": "Coming soon!"
    }

    return render(request, "main.html", context)
