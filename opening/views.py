from django.shortcuts import render
from .async_scraper import async_scrape
from .sync_scraper import sync_scrape
import time


def index(request):
    context = {}
    
    if request.method == "POST":
        keyword = request.POST["keyword"]
        pages = request.POST["pages"]
        method = request.POST["method"]
        area = []
        jobexp = []
        
        for i in range(6):
            if request.POST.get(f"area{i+1}"):
                area.append(request.POST[f"area{i+1}"])
            if request.POST.get(f"experience{i+1}"):
                jobexp.append(request.POST[f"experience{i+1}"])
                
        area = "%2C".join(area)
        jobexp = "%2C".join(jobexp)
        
        start_time = time.time()
        
        if method == 'async':
            try:
                context["opening"] = async_scrape(keyword, area, int(pages), jobexp)
            except:
                context["opening"] = async_scrape(keyword, area)
        else:
            try:
                context["opening"] = sync_scrape(keyword, area, int(pages), jobexp)
            except:
                context["opening"] = sync_scrape(keyword, area)
            
        end_time = time.time()
        
        interval_time = end_time - start_time
        
        context["result_len"] = len(context["opening"])
        context["time"] = f"{interval_time:.2f}"
    
    return render(request, "index.html", context)