from bs4 import BeautifulSoup
import grequests
import datetime

THIS_YEAR = str(datetime.datetime.today().year)

def sort_by_late_date(open):
    return datetime.datetime.strptime(open['date'], "%Y/%m/%d")
    

def scrape(keyword, pages, area, jobexp):
    links = []
    opening = []
    job_link = []
    
    for page in range(1, pages+1):
        links.append(
            f"https://www.104.com.tw/jobs/search/?keyword={keyword}&area={area}&order=1&page={page}&jobexp={jobexp}&jobsource=2021indexpoc&ro=0")
            
    reqs = [grequests.get(link) for link in links]
    response = grequests.imap(reqs, grequests.Pool(pages))  # Parallel sending requests (grequests)
        
    for r in response:
        soup = BeautifulSoup(r.content, "lxml")
        blocks = soup.find_all("div", {"class": "b-block__left"})  # Job block
        
        for block in blocks:
            job = block.find("a", {"class": "js-job-link"})  # Job title
            if not job or job['href'] in job_link:
                continue
            job_link.append(job['href'])
            
            date = block.find("span", {"class": "b-tit__date"})  # Published date
            
            company = block.find_all("li")[1]  # Company name

            ultag = block.find("ul", {"class": "b-list-inline b-clearfix job-list-intro b-content"})
            litag = ultag.find_all("li")
            city = litag[0]  # City name
            experience =  litag[1]  # Job exp
            education = litag[2]  # At least diploma education
            
            salary = block.find("span", {"class": "b-tag--default"})  # Compensation Package

            if date.getText().strip():
                opening.append(dict(job=job.getText(), date=f"{THIS_YEAR}/{date.getText().strip()}", link=job['href'], company=company.getText().strip(), city=city.getText(), experience=experience.getText(), education=education.getText(), salary=salary.getText()))
            else:
                opening.append(dict(job=job.getText(), date="9999/12/31", link=job['href'], company=company.getText().strip(), city=city.getText(), experience=experience.getText(), education=education.getText(), salary=salary.getText()))

    opening = sorted(opening, reverse=True, key=sort_by_late_date)
    
    return opening
