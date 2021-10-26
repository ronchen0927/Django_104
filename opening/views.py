from django.shortcuts import render
from .scraper import scrape


def index(request):
    context = {}
    
    if request.method == "POST":
        keyword = request.POST["keyword"]
        area = []
        jobexp = []
        
        for i in range(6):
            if request.POST.get(f'area{i+1}'):
                area.append(request.POST[f'area{i+1}'])
            if request.POST.get(f"experience{i+1}"):
                jobexp.append(request.POST[f'experience{i+1}'])
                
        area = "%2C".join(area)
        jobexp = "%2C".join(jobexp)
        
        context["opening"] = scrape(keyword, area, jobexp)
    
    return render(request, "opening/index.html", context)