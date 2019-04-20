from bs4 import BeautifulSoup
import requests, sys, os, datetime
'''
Download all the searching information for 
all the job openings for "Computational Biologist"
from indeed.com
'''
class downloader(object):
    '''
    Initialzation
    '''
    def __init__(self, num_per_page, start_idx):
        self.server = "http://www.indeed.com"
        self.source = "https://www.indeed.com/jobs?q=%22computational%20biologist%22&limit=" + \
        str(num_per_page) + "&radius=25&start=" + \
        str(start_idx) + "&vjk=9bdec5d77cafc659"
        self.names = []
        self.ulrs = []
        self.nums = 0
        self.job_info = []
    
    '''
    get basic job info including job title, salary, location
    and detailed job description
    '''
    def get_download_url(self):
        
        req = requests.get(url=self.source)
        html = req.text
        bf = BeautifulSoup(html, "lxml")
        
        tables = bf.find_all('div', class_="jobsearch-SerpJobCard unifiedRow row result")
        
        for each_idx in range(len(tables)):
            item = tables[each_idx]
            each =  item.find_all('a', class_="jobtitle turnstileLink ")[0]
            #get url
            ulrs_link = str(self.server + each.get('href'))
            self.ulrs.append(ulrs_link)
            self.names.append(str(each_idx))
            self.nums += 1
        
            #get job info, including title, salary and job location
            #get job title
            try:
                job_title = item.contents[1].find_all("a", class_="jobtitle turnstileLink ")[0].get("title", []).strip("\n")
            except:
                job_title = 'NA'
                pass
            #get company name
            try:
                company_name = item.contents[3].find_all("span", class_="company")[0].text.strip("\n")
            except:
                company_name = 'NA'
                pass
            #get job location
            try:
                job_location = item.contents[3].find_all("span", class_="location")[0].text.strip("\n")
            except:
                job_location = 'NA'
                pass
            #get salary information
            try:
                salary_info = item.contents[5].find_all("span", class_="salary no-wrap")[0].text.strip("\n")
            except:
                salary_info = 'NA'
                pass
            self.job_info.append("job title: " + job_title + "\n" + \
                                 "company name: " + company_name + "\n" + \
                                 "job location: " + job_location +"\n" + \
                                 "salary info: " + salary_info)
            
    '''
    Parse the content of each job posts and return as a text string
    '''
            
    def get_contents(self, target):
        req = requests.get(url=target)
        
        soup = BeautifulSoup(req.content)
        bf = soup.find_all('div', class_="jobsearch-JobComponent-description icl-u-xs-mt--md")
        try:
            only_texts = bf[0].text
        except:
            only_texts = 'NA'
        
        
           
        return only_texts
   
    
    
        
        
if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding('utf-8')
    total_pages = 3
    num_per_page = 50
    start_ind = [i*num_per_page for i in range(total_pages)]
    
    now = datetime.datetime.now()
    fname = now.strftime("%Y-%m-%d")+"_indeed_jobs_for_compuational_biologists.txt"
    '''
    write all the information into one text file for further processing
    '''
    f = open(fname, "a")
    for start_idx in start_ind:
        dl = downloader(num_per_page, start_idx)
    
        
        dl.get_download_url()
        print "Start Processing " + "Page"+ str(start_idx / 50+1) 
       
        for i in range(dl.nums):
            #fname = dl.names[i].upper()+'.txt'
            #os.mkdir(dl.names[i].upper())
            #path = './'+dl.names[i].upper()+'/' + fname
            #print dl.ulrs[i]
            f.write(dl.job_info[i])
            f.write("\n\n*****DETAILS BELOW*****\n\n")
            f.write(dl.get_contents(dl.ulrs[i]).rstrip())
            f.write("\n\n\n\n\n**************************************\n\n\n\n\n")
            sys.stdout.write("\n Now writing record %s\n" % str(dl.names[i]) + '\r')
            sys.stdout.write("\n Finished %.2f%%\n" % (float(i)/dl.nums*100) + '\r')
            sys.stdout.flush()
        print ("\n "+ "Page"+ str(start_idx / 50+1) + " Finished 100%!")
    
    f.close()
    sys.stdout.write("\n ALL FINISHED! \n")
    