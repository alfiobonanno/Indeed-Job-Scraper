import nodriver as uc
import asyncio
from bs4 import BeautifulSoup
import json
async def scrape_desc(browser, full_link):
    page = await browser.get(full_link)
    await asyncio.sleep(5)
    html = await page.get_content()
    soup = BeautifulSoup(html, "html.parser")
    description_el = soup.find("div", class_= "jobsearch-JobComponent-description css-wppltw eu4oa1w0")
    descritpion = description_el.get_text(strip=True) if description_el else "N/A"
    return descritpion


async def main():

    base_url = "https://uk.indeed.com"
    current_url = f'{base_url}/jobs?q=data+analyst&start=0'

    browser = await uc.start(headless=False)
    all_jobs = []

    while current_url:

        page = await browser.get(current_url)
        await asyncio.sleep(10)
        html = await page.get_content()
        soup = BeautifulSoup(html, "html.parser")
        jobs = soup.find_all("div", class_ = "job_seen_beacon")

        for job in jobs:
            job_title = job.select_one("h2.jobTitle").get_text()
            print(job_title)
            company_el = job.select_one("span[data-testid='company-name']")
            company = company_el.get_text(strip=True) if company_el else "N/A"
            print(company)
            location_el = job.select_one("div[data-testid= 'text-location']")
            location = location_el.get_text() if location_el else "N/A"
            print(location)
            salary_el = job.select_one("div.metadata.salary-snippet-container")
            salary = salary_el.get_text() if salary_el else "Not Listed"
            print(salary)
            href_element = job.select_one("h2.jobTitle>a")
            href_link = href_element['href'] if href_element else "N/A"
            full_link = base_url + href_link
            print(full_link)
            description = await scrape_desc(browser, full_link)

            all_jobs.append({
            "Job Title": job_title,
            "Company": company,
            "Location": location,
            "Salary": salary,
            "Link": full_link,
            "Description": description
        })
        
            with open("indeed_jobs.json", "w", encoding="utf-8", errors="replace") as f:
                json.dump(all_jobs, f, ensure_ascii=False, indent=4)

        next_link = soup.select_one('a[data-testid="pagination-page-next"]')

        if next_link:
            next_href = next_link['href']
            current_url = base_url + next_href

        else:
            print("\n✅ No more pages.")
            break



if __name__ == '__main__':
    # since asyncio.run never worked (for me)
    uc.loop().run_until_complete(main())