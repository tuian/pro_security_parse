from selenium import webdriver
from pyvirtualdisplay import Display
from selenium import webdriver
import os 
from bs4 import BeautifulSoup
from lxml import html
import time
import glob
import shutil
import os, sys, stat
import time 
import logging
import profile
from datetime import datetime
from lxml import html
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException
import re 
import urllib

logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-10s) %(message)s', )



class pro_similar(object):
    def __init__(self, domain, dte):
        self.domain = domain
	self.dte = dte

        start  = self.domain.find(".com")
        self.dmn = self.domain[:start]
     
        self.mydump = "mydump_pro_similatr"

        try:
            os.makedirs(self.mydump)
        except:
            pass

        self.directory = "dirpro%s" %(time.strftime("%d%m%Y"))

        try:
            os.makedirs(self.directory)
        except:
            pass

        display = Display()
        self.display = display.start()

	fp = webdriver.FirefoxProfile()
	fp.set_preference("browser.download.folderList",2)
        fp.set_preference("browser.download.manager.showWhenStarting",False)
	fp.set_preference("browser.download.dir", os.getcwd())
	fp.set_preference("browser.helperApps.neverAsk.saveToDisk","text/csv")

	self.driver = webdriver.Firefox(firefox_profile=fp)
        self.driver.maximize_window()
	self.driver.implicitly_wait(60)
        self.driver.set_page_load_timeout(120)



    def __del__(self):
        self.driver.delete_all_cookies()
	self.driver.quit()
        self.display.stop()



    def  date_conversion(self):
        page = self.driver.page_source
        soup = BeautifulSoup(page, "html.parser")

	tag_dte_main = soup.find("h5", attrs={"class":"details ng-binding"})
	tag_dte_main = str(tag_dte_main.get_text()).strip()

	my_month = {"Jan":"1", "Feb":"2", "Mar":"3",
	            "Apr":"4", "May":"5", "Jun":"6",
	            "Jul":"7", "Aug":"8", "Sep":"9" ,
	            "Oct":"10", "Nov":"11", "Dec":"12"}

        
	if tag_dte_main.startswith("From") is True:
	    tag_dte = tag_dte_main[5:]
            tag_dte_list = tag_dte.split("to")

	    tag_dte_fst_mn_yr = tag_dte_list[0].strip().split(",")
	    tag_dte_snd_mn_yr = tag_dte_list[1].strip().split(",")

	    tag_dte_fst_mn = tag_dte_fst_mn_yr[0].strip()
	    tag_dte_fst_mn_int = my_month[tag_dte_fst_mn]
	    tag_dte_fst_yr = tag_dte_fst_mn_yr[1].strip()

	    tag_dte_snd_mn =  tag_dte_snd_mn_yr[0].strip()
	    tag_dte_snd_mn_int = my_month[tag_dte_snd_mn]
	    tag_dte_snd_yr =  tag_dte_snd_mn_yr[1].strip()

	else:
	    tag_dte = tag_dte_main[3:]
	    tag_dte_fst_mn_yr = tag_dte.strip().split(",")

	    tag_dte_fst_mn = tag_dte_fst_mn_yr[0].strip()
	    tag_dte_fst_mn_int = my_month[tag_dte_fst_mn]
	    tag_dte_fst_yr = tag_dte_fst_mn_yr[1].strip()

	    tag_dte_snd_mn = tag_dte_fst_mn
	    tag_dte_snd_mn_int = tag_dte_fst_mn_int
	    tag_dte_snd_yr = tag_dte_fst_yr

        self.dte_list = [tag_dte_fst_mn, tag_dte_fst_mn_int, tag_dte_fst_yr, 
	                 tag_dte_snd_mn, tag_dte_snd_mn_int, tag_dte_snd_yr]

        return self.dte_list

            

    def ajax_complete(self, driver):
        try:
            time.sleep(0.5)
            return 0 == driver.execute_script("return jQuery.active")

        except WebDriverException:
            pass



    def wtng_fr_pg_ld(self):
        try:
            WebDriverWait(self.driver, 1000).until(self.ajax_complete,  "Timeout waiting for page to load")

        except WebDriverException:
            pass



    def mystrip(self, x):
        return str(x.get_text()).replace(",", "-").replace("\n", " ").replace("\r", " ").replace("\t", " ").strip()



    def login_fun(self):
        self.driver.get("https://secure.similarweb.com/account/login")
        self.driver.find_element_by_id("UserName").send_keys("kayakashyap213@gmail.com")
        self.driver.find_element_by_id("Password").send_keys("6Tresxcvbhy")
        self.driver.find_element_by_xpath("/html/body/section/div/div/div/form/fieldset/div/button").click()
        self.wtng_fr_pg_ld()
       


    def domain_and_date(self):
        #self.driver.find_element_by_id("enter-website").clear() 
        #self.driver.find_element_by_id("enter-website").send_keys(self.domain)
        #self.wtng_fr_pg_ld()
         
        link ="http://pro.similarweb.com/website/analysis/#/%s/*/999/%s/audience/overview"
        link = link %(self.domain, self.dte)
	
	self.driver.get(link)
        self.wtng_fr_pg_ld()


    
    def web_aud_over(self):
        link = "http://pro.similarweb.com/website/analysis/#/%s/*/999/%s/audience/overview?selectTrendLine=visits&aggDuration=monthly"
	link = link %(self.domain, self.dte)
	
	self.driver.get(link)       
        self.wtng_fr_pg_ld()

        page = self.driver.page_source
        soup = BeautifulSoup(page, "html.parser")

        total_desk_vist = soup.find("div", attrs={"class":"count c-blue ng-binding"})
        self.total_desk_vist = str(total_desk_vist.get_text()).replace(",", "-").strip()

	self.driver.find_element_by_xpath("/html/body/div[2]/div[3]/section/div/div/div[2]/div/div/a").click()  
        self.wtng_fr_pg_ld()

        time.sleep(60)
	self.web_aud_over_file = self.find_file("/tmp", "*.part")
        
        return  [self.total_desk_vist, self.web_aud_over_file]

     
        
    def find_file(self, directory, exten, new_file = None):
        if exten == "*.part":
            direc_exet = "%s/%s" %(directory, exten)
               
            for fle in glob.glob(direc_exet):
                os.chmod(fle, 755)

                start = fle.find(".")
                exten_csv = "%s.xlsx" %(fle[:start])

                shutil.copy(fle, exten_csv)
                filename = filter(None, exten_csv.strip().split("/"))[-1]

                new_file = "%s/%s" %(self.directory, filename)
                shutil.move(exten_csv, new_file)

                shutil.move(fle, self.mydump)
                return new_file

        else:
            dir_file_csv = "%s/%s" %(directory, exten)

            for fle in glob.glob(dir_file_csv):
                os.chmod(fle, 755)
                filename = filter(None, fle.strip().split("/"))[-1]
            
                if new_file is not None:
                    new_file = "%s/%s" %(self.directory, new_file)

                else:
                    new_file = "%s/%s" %(self.directory, filename)

                shutil.move(filename, new_file)
                return new_file



    def web_geo(self):
        web_geo_link = "http://pro.similarweb.com/website/analysis/#/%s/*/999/%s/audience/geography"
	web_geo_link = web_geo_link %(self.domain, self.dte)

	self.driver.get(web_geo_link)
        self.wtng_fr_pg_ld()
	
	self.driver.find_element_by_xpath("/html/body/div[2]/div[3]/section/div/div/div/form/a").click()
        self.wtng_fr_pg_ld()

        time.sleep(60)
	self.web_geo_file = self.find_file(os.getcwd(), "*.csv")
        
        return [self.web_geo_file]
       

    def web_audin(self):
        web_audn_link = "http://pro.similarweb.com/website/analysis/#/%s/*/999/%s/audience/interests"
        web_audn_link = web_audn_link  %(self.domain, self.dte)
       
        self.driver.get(web_audn_link)
        self.wtng_fr_pg_ld()

        self.driver.find_element_by_xpath("/html/body/div[2]/div[3]/section/div/div/div/form[2]/a").click()
        self.wtng_fr_pg_ld()

        time.sleep(60)
        self.web_audn_file = self.find_file(os.getcwd(), "*.csv")
        
        return [self.web_audn_file]



    def trafic_pd_org_all_src(self):
        trafic_pd_org_all_src_link = "http://pro.similarweb.com/website/analysis/#/%s/*/999/%s/traffic/search?selectedTab=all"
        trafic_pd_org_all_src_link = trafic_pd_org_all_src_link %(self.domain, self.dte)         
        link1 = trafic_pd_org_all_src_link

        link1a = "http://pro.similarweb.com/export/analysis/GetTrafficSourcesSearchTsv?selectedTab=all&key="+ self.domain +"&country=999&from=2013|4&to=2014|3&orderby=Share%20desc"
        
        self.trafic_pd_org_all_src_visit = self.trf_srch_grp_1_2_3(link1, link1a)
        self.trafic_pd_org_all_src_file = self.find_file_csv(os.getcwd(), "*.csv", "trafic_pd_org_all_src_file.csv")

        return [self.trafic_pd_org_all_src_file, self.trafic_pd_org_all_src_visit[0].strip()]        



    def trafic_org_all_src(self):
        link1 = "http://pro.similarweb.com/website/analysis/#/" + self.domain + "/*/999/" + self.dte + "/traffic/search?selectedTab=all&Keywords_filters=OP%3B%3D%3D%3B0%2BexcludeBranded%3Bnotcontains_multi%3B" + self.dmn
       
        link1a = "http://pro.similarweb.com/export/analysis/GetTrafficSourcesSearchTsv?selectedTab=all&groupedKeywords_filters=wordCount;==;1&Keywords_filters=OP;==;0&key="+ self.domain +"&country=999&from=2013|4&to=2014|3&filter=OP;==;0&orderby=Share%20desc" 

        visit_xpth = "/html/body/div[2]/div[3]/section/div/div/div/div[2]/div[2]/ul/li/span[2]/text()"
        self.trafic_org_all_src_visit = self.trf_srch_grp_1_2_3(link1, link1a, visit_xpth)
        self.trafic_org_all_src_file = self.find_file_csv(os.getcwd(), "*.csv", "trafic_org_all_src_file.csv")

        return [self.trafic_org_all_src_file, self.trafic_org_all_src_visit[0].strip()]
        
 

    def trafic_p_all_src(self):
        link1= "http://pro.similarweb.com/website/analysis/#/"+ self.domain +"/*/999/"+ self.dte +"/traffic/search?selectedTab=all&Keywords_filters=OP%3B%3D%3D%3B1%2BexcludeBranded%3Bnotcontains_multi%3B"+ self.dmn +"&groupedKeywords_filters=wordCount%3B%3D%3D%3B3%2BexcludeBranded%3Bnotcontains%3B"+ self.dmn

        link1a = "http://pro.similarweb.com/export/analysis/GetTrafficSourcesSearchTsv?selectedTab=all&Keywords_filters=OP;==;1&key="+ self.domain +"&country=999&from=2013|4&to=2014|3&filter=OP;==;1&orderby=Share%20desc"
 
        visit_xpth = "/html/body/div[2]/div[3]/section/div/div/div/div[2]/div[2]/ul/li[2]/span[2]/text()"
        self.trafic_p_all_src_visit = self.trf_srch_grp_1_2_3(link1, link1a, visit_xpth)
        self.trafic_p_all_src_file = self.find_file_csv(os.getcwd(), "*.csv", "trafic_p_all_src_file.csv")

        return [self.trafic_p_all_src_file, self.trafic_p_all_src_visit[0].strip()]



    def trf_po_srch_grp1(self):
        link1 = "http://pro.similarweb.com/website/analysis/#/"+ self.domain +"/*/999/"+ self.dte +"/traffic/search?selectedTab=grouped&groupedKeywords_filters=wordCount%3B%3D%3D%3B1%2BexcludeBranded%3Bnotcontains%3B"+ self.dmn

        link1a = "http://pro.similarweb.com/export/analysis/GetTrafficSourcesGroupedKeywordsTsv?selectedTab=grouped&groupedKeywords_filters=wordCount;==;1+excludeBranded;notcontains;amazon&key=amazon.com&country=999&from=2013|3&to=2014|2&filter=wordCount;==;1,searchTerm;notcontains;%22amazon%22&orderby=Share%20desc"

        self.trafic_srch_grp_visit_1 = self.trf_srch_grp_1_2_3(link1, link1a)
        self.trf_srch_grp1_file = self.find_file_csv(os.getcwd(), "*.csv", "trf_srch_grp1.csv")
 
        return [self.trf_srch_grp1_file, self.trafic_srch_grp_visit_1[0].strip()]



    def trf_o_srch_grp1(self):
        link1 = "http://pro.similarweb.com/website/analysis/#/"+ self.domain +"/*/999/"+ self.dte +"/traffic/search?selectedTab=grouped&Keywords_filters=OP%3B%3D%3D%3B0%2BexcludeBranded%3Bnotcontains_multi%3B"+ self.dmn +"&groupedKeywords_filters=wordCount%3B%3D%3D%3B1%2BexcludeBranded%3Bnotcontains%3B"+ self.dmn

        link1a = "http://pro.similarweb.com/export/analysis/GetTrafficSourcesGroupedKeywordsTsv?selectedTab=grouped&Keywords_filters=OP;==;0+excludeBranded;notcontains_multi;"+ self.dmn +"&groupedKeywords_filters=wordCount;==;1+excludeBranded;notcontains;"+ self.dmn +"&key="+ self.domain +"&country=999&from=2013|3&to=2014|2&filter=wordCount;==;1,searchTerm;notcontains;%22"+ self.dmn +"%22&orderby=Share%20desc"

        visit_xpth = "/html/body/div[2]/div[3]/section/div/div/div/div[2]/div[2]/ul/li/span[2]/text()"    
        self.trafic_o_srch_grp_visit_1 = self.trf_srch_grp_1_2_3(link1, link1a, visit_xpth)
        self.trf_o_srch_grp1_file = self.find_file_csv(os.getcwd(), "*.csv", "trf_0_srch_grp1.csv")

        return [self.trf_o_srch_grp1_file, self.trafic_o_srch_grp_visit_1[0].strip()]



    def trf_p_srch_grp1(self):
        link1 = "http://pro.similarweb.com/website/analysis/#/"+ self.domain +"/*/999/"+ self.dte +"/traffic/search?selectedTab=all&Keywords_filters=OP%3B%3D%3D%3B1%2BexcludeBranded%3Bnotcontains_multi%3B"+ self.dmn +"&groupedKeywords_filters=wordCount%3B%3D%3D%3B1%2BexcludeBranded%3Bnotcontains%3B"+ self.dmn

        link1a = "http://pro.similarweb.com/export/analysis/GetTrafficSourcesGroupedKeywordsTsv?selectedTab=grouped&Keywords_filters=OP;==;1+excludeBranded;notcontains_multi;"+ self.dmn +"&groupedKeywords_filters=wordCount;==;1+excludeBranded;notcontains;"+ self.dmn +"&key="+ self.domain +"&country=999&from=2013|3&to=2014|2&filter=wordCount;==;1,searchTerm;notcontains;%22"+ self.dmn +"%22&orderby=Share%20desc"

        visit_xpth = "/html/body/div[2]/div[3]/section/div/div/div/div[2]/div[2]/ul/li[2]/span[2]/text()"    
        self.trafic_p_srch_grp_visit_1 = self.trf_srch_grp_1_2_3(link1, link1a, visit_xpth)
        self.trf_p_srch_grp1_file = self.find_file_csv(os.getcwd(), "*.csv", "trf_p_srch_grp1.csv")

        return [self.trf_p_srch_grp1_file, self.trafic_p_srch_grp_visit_1[0].strip()]



    def trf_po_srch_grp2(self):
        link2 = "http://pro.similarweb.com/website/analysis/#/"+ self.domain +"/*/999/"+ self.dte +"/traffic/search?selectedTab=grouped&groupedKeywords_filters=wordCount%3B%3D%3D%3B2%2BexcludeBranded%3Bnotcontains%3B"+ self.dmn
 
        link2a = "http://pro.similarweb.com/export/analysis/GetTrafficSourcesGroupedKeywordsTsv?selectedTab=grouped&groupedKeywords_filters=wordCount;==;2+excludeBranded;notcontains;amazon&key=amazon.com&country=999&from=2013|3&to=2014|2&filter=wordCount;==;2,searchTerm;notcontains;%22amazon%22&orderby=Share%20desc"

        self.trafic_srch_grp_visit_2 = self.trf_srch_grp_1_2_3(link2, link2a)
        self.trf_srch_grp1_file_2 = self.find_file_csv(os.getcwd(), "*.csv", "trf_srch_grp2.csv")

        return [self.trf_srch_grp1_file_2, self.trafic_srch_grp_visit_2[0].strip()]



    def trf_o_srch_grp2(self):
        link1 = "http://pro.similarweb.com/website/analysis/#/"+ self.domain +"/*/999/"+ self.dte +"/traffic/search?selectedTab=grouped&Keywords_filters=OP%3B%3D%3D%3B0%2BexcludeBranded%3Bnotcontains_multi%3B"+ self.dmn +"&groupedKeywords_filters=wordCount%3B%3D%3D%3B2%2BexcludeBranded%3Bnotcontains%3B" + self.dmn

        link1a = "http://pro.similarweb.com/export/analysis/GetTrafficSourcesGroupedKeywordsTsv?selectedTab=grouped&Keywords_filters=OP;==;0+excludeBranded;notcontains_multi;"+ self.dmn +"&groupedKeywords_filters=wordCount;==;2+excludeBranded;notcontains;"+ self.dmn +"&key="+ self.domain +"&country=999&from=2013|3&to=2014|2&filter=wordCount;==;2,searchTerm;notcontains;%22"+ self.dmn +"%22&orderby=Share%20desc"
        
        visit_xpth = "/html/body/div[2]/div[3]/section/div/div/div/div[2]/div[2]/ul/li/span[2]/text()"
        self.trafic_o_srch_grp_visit_2 = self.trf_srch_grp_1_2_3(link1, link1a, visit_xpth)
        self.trf_o_srch_grp2_file = self.find_file_csv(os.getcwd(), "*.csv", "trf_0_srch_grp2.csv")

        return [self.trf_o_srch_grp2_file, self.trafic_o_srch_grp_visit_2[0].strip()] 



    def trf_p_srch_grp2(self):
        link1 = "http://pro.similarweb.com/website/analysis/#/"+ self.domain +"/*/999/"+ self.dte +"/traffic/search?selectedTab=all&Keywords_filters=OP%3B%3D%3D%3B1%2BexcludeBranded%3Bnotcontains_multi%3B"+ self.dmn +"&groupedKeywords_filters=wordCount%3B%3D%3D%3B1%2BexcludeBranded%3Bnotcontains%3B"+ self.dmn

        link1a = "http://pro.similarweb.com/export/analysis/GetTrafficSourcesGroupedKeywordsTsv?selectedTab=grouped&Keywords_filters=OP;==;1+excludeBranded;notcontains_multi;"+ self.dmn +"&groupedKeywords_filters=wordCount;==;2+excludeBranded;notcontains;"+ self.dmn +"&key="+ self.domain +"&country=999&from=2013|3&to=2014|2&filter=wordCount;==;2,searchTerm;notcontains;%22"+ self.dmn +"%22&orderby=Share%20desc"

        visit_xpth = "/html/body/div[2]/div[3]/section/div/div/div/div[2]/div[2]/ul/li[2]/span[2]/text()"
        self.trafic_p_srch_grp_visit_2 = self.trf_srch_grp_1_2_3(link1, link1a, visit_xpth)
        self.trf_p_srch_grp2_file = self.find_file_csv(os.getcwd(), "*.csv", "trf_p_srch_grp2.csv")

        return [self.trf_p_srch_grp2_file, self.trafic_p_srch_grp_visit_2[0].strip()]
 


    def trf_po_srch_grp3(self):
         link3 = "http://pro.similarweb.com/website/analysis/#/"+ self.domain +"/*/999/"+ self.dte +"/traffic/search?selectedTab=grouped&groupedKeywords_filters=wordCount%3B%3D%3D%3B3%2BexcludeBranded%3Bnotcontains%3B"+ self.dmn
 
         link3a = "http://pro.similarweb.com/export/analysis/GetTrafficSourcesGroupedKeywordsTsv?selectedTab=grouped&groupedKeywords_filters=wordCount;==;3+excludeBranded;notcontains;amazon&key=amazon.com&country=999&from=2013|3&to=2014|2&filter=wordCount;==;3,searchTerm;notcontains;%22amazon%22&orderby=Share%20desc"

         self.trafic_srch_grp_visit_3 = self.trf_srch_grp_1_2_3(link3, link3a)
         self.trf_srch_grp1_file_3 = self.find_file_csv(os.getcwd(), "*.csv", "trf_srch_grp3.csv")

         return [self.trf_srch_grp1_file_3, self.trafic_srch_grp_visit_3[0].strip()]



    def trf_o_srch_grp3(self):
        link1 = "http://pro.similarweb.com/website/analysis/#/"+ self.domain +"/*/999/"+ self.dte +"/traffic/search?selectedTab=grouped&Keywords_filters=OP%3B%3D%3D%3B0%2BexcludeBranded%3Bnotcontains_multi%3B"+ self.dmn +"&groupedKeywords_filters=wordCount%3B%3D%3D%3B2%2BexcludeBranded%3Bnotcontains%3B" + self.dmn

        link1a = "http://pro.similarweb.com/export/analysis/GetTrafficSourcesGroupedKeywordsTsv?selectedTab=grouped&Keywords_filters=OP;==;0+excludeBranded;notcontains_multi;"+ self.dmn +"&groupedKeywords_filters=wordCount;==;3+excludeBranded;notcontains;"+ self.dmn +"&key="+ self.domain + "&country=999&from=2013|3&to=2014|2&filter=wordCount;==;3,searchTerm;notcontains;%22"+ self.dmn +"%22&orderby=Share%20desc"

        visit_xpth = "/html/body/div[2]/div[3]/section/div/div/div/div[2]/div[2]/ul/li/span[2]/text()"
        self.trafic_o_srch_grp_visit_3 = self.trf_srch_grp_1_2_3(link1, link1a, visit_xpth)
        self.trf_o_srch_grp3_file = self.find_file_csv(os.getcwd(), "*.csv", "trf_0_srch_grp3.csv")

        return  [self.trf_o_srch_grp3_file, self.trafic_o_srch_grp_visit_3[0].strip()]

    

    def trf_p_srch_grp3(self):
        link1 = "http://pro.similarweb.com/website/analysis/#/"+ self.domain +"/*/999/"+ self.dte +"/traffic/search?selectedTab=all&Keywords_filters=OP%3B%3D%3D%3B1%2BexcludeBranded%3Bnotcontains_multi%3B"+ self.dmn +"&groupedKeywords_filters=wordCount%3B%3D%3D%3B1%2BexcludeBranded%3Bnotcontains%3B"+ self.dmn

        link1a = "http://pro.similarweb.com/export/analysis/GetTrafficSourcesGroupedKeywordsTsv?selectedTab=grouped&Keywords_filters=OP;==;1+excludeBranded;notcontains_multi;"+ self.dmn +"&groupedKeywords_filters=wordCount;==;3+excludeBranded;notcontains;"+ self.dmn +"&key="+ self.domain +"&country=999&from=2013|3&to=2014|2&filter=wordCount;==;3,searchTerm;notcontains;%22"+ self.dmn +"%22&orderby=Share%20desc"

        visit_xpth = "/html/body/div[2]/div[3]/section/div/div/div/div[2]/div[2]/ul/li[2]/span[2]/text()"
        self.trafic_p_srch_grp_visit_3 = self.trf_srch_grp_1_2_3(link1, link1a, visit_xpth)
        self.trf_p_srch_grp3_file = self.find_file_csv(os.getcwd(), "*.csv", "trf_p_srch_grp3.csv")

        return [self.trf_p_srch_grp3_file, self.trafic_p_srch_grp_visit_3[0].strip()]



    def trf_srch_grp_1_2_3(self, grp_link, grp_lkn_csv, xpth = None):
        self.driver.get(grp_link)
        self.wtng_fr_pg_ld()

        time.sleep(3)
        page = self.driver.page_source

        tree = html.fromstring(page)

        if xpth is None:
            trafic_srch_grp_visit_1_2_3 = tree.xpath("/html/body/div[2]/div[3]/section/div/div/div/div/div[2]/div/text()")
            #self.driver.find_element_by_xpath("/html/body/div[2]/div[3]/section/div/div[2]/div/div/div/div[2]/div/form/a").click()

	else:
	    trafic_srch_grp_visit_1_2_3 = tree.xpath(xpth)

        self.driver.get(grp_lkn_csv)
        self.wtng_fr_pg_ld()
 
        time.sleep(60)
        return trafic_srch_grp_visit_1_2_3
 
 
 
    def find_file_csv(self, directory, exten, new_filename):
        dir_file_csv = "%s/%s" %(directory, exten)
        loop = True

        while loop is True:
            fles = glob.glob(dir_file_csv)
            fle = fles[0]
            
            if len(fles) != 0:       
                os.chmod(fle, 755)
                filename = filter(None, fle.strip().split("/"))[-1]

                new_file = "%s/%s" %(self.directory, new_filename)
                shutil.move(filename, new_file)
                return new_file



    def traff_dest(self):
        link = "http:/link/pro.similarweb.com/website/analysis/#/%s/*/999/%s/destination/outgoing"
        link = link %(self.domain, self.dte)
        
	link2 = "http://pro.similarweb.com/export/analysis/GetOutgoingTsv?key="+ self.domain +"&country=999&from=2013|3&to=2014|2&orderby=Share%20desc"

  	total_visit_pth ="/html/body/div[2]/div[3]/section/div/div/div/div/div/span/text()"
	self.traff_dest_visit = self.trf_srch_grp_1_2_3(link, link2, total_visit_pth)

        self.traff_dest_file = self.find_file_csv(os.getcwd(), "*.csv", "traff_dest_file.csv")

	return [self.traff_dest_file, self.traff_dest_visit]



    def web_cont_sub(self):
        link1 = "http://pro.similarweb.com/website/analysis/#/%s/*/999/%s/content/subdomains"
	link1 = link1 %(self.domain, self.dte)

	link1a = "http://pro.similarweb.com/export/analysis/GetSubDomainsTsv?key="+ self.domain +"&country=999&from=2013|10&to=2014|3&orderby=Share%20desc"

	self.web_cont_sub_visit = self.trf_srch_grp_1_2_3(link1, link1a)
	self.web_cont_sub_file = self.find_file_csv(os.getcwd(), "*.csv", "web_cont_sub_file.csv")
	
        return [self.web_cont_sub_file]


	
    def web_cont_sub_pop_page(self):
        link1 = "http://pro.similarweb.com/website/analysis/#/%s/*/999/%s/content/popular?selectedTab=pages" 
        link1 = link1 %(self.domain, self.dte)

        link1a = "http://pro.similarweb.com/export/analysis/GetPopularPagesTsv?selectedTab=pages&key="+ self.domain +"&country=999&from=2013|10&to=2014|3&orderby=Share%20desc"

        self.web_cont_sub_pop_page_visit = self.trf_srch_grp_1_2_3(link1, link1a)
        self.web_cont_sub_pop_page_file = self.find_file_csv(os.getcwd(), "*.csv", "web_cont_sub_pop_page_file.csv")

        return [self.web_cont_sub_pop_page_file]

    

    def web_cont_sub_led_folder(self):
        link1 = "http://pro.similarweb.com/website/analysis/#/%s/*/999/%s/content/popular?selectedTab=folders"
	link1 = link1 %(self.domain, self.dte)

	link1a = "http://pro.similarweb.com/export/analysis/GetLeadingFoldersTsv?selectedTab=folders&key="+ self.domain +"&country=999&from=2013|10&to=2014|3&orderby=Share%20desc"

	self.web_cont_sub_led_folder_visit = self.trf_srch_grp_1_2_3(link1, link1a)
	self.web_cont_sub_led_folder_file = self.find_file_csv(os.getcwd(), "*.csv", "web_cont_sub_led_folder_file.csv")

	return [self.web_cont_sub_led_folder_file]


        
    def compititor_simil(self):
        link1 = "http://pro.similarweb.com/website/analysis/#/%s/*/999/%s/competitors/similarsites" 
        link1 = link1 %(self.domain, self.dte)

        link1a = "http://pro.similarweb.com/export/analysis/GetCompetitorsSimilarsitesTsv?key="+ self.domain +"&country=999&from=2013|10&to=2014|3&orderby=Affinity%20desc"

        self.compititor_simil_visit = self.trf_srch_grp_1_2_3(link1, link1a)
        self.compititor_simil_file = self.find_file_csv(os.getcwd(), "*.csv", "compititor_simil_file.csv")

        return [self.compititor_simil_file]



    def compititor_srch_orgnic(self):
        link1 ="http://pro.similarweb.com/website/analysis/#/%s/*/999/%s/competitors/search?selectedTab=organic"
        link1 = link1 %(self.domain, self.dte)

        link1a = "http://pro.similarweb.com/export/analysis/GetOrganicSearchCompetitorsTsv?selectedTab=organic&key="+ self.domain +"&country=999&from=2013|10&to=2014|3&orderby=Score%20desc"

        self.compititor_srch_orgnic_visit = self.trf_srch_grp_1_2_3(link1, link1a)
        self.compititor_srch_orgnic_file = self.find_file_csv(os.getcwd(), "*.csv", "compititor_srch_orgnic_file.csv")

        return [self.compititor_srch_orgnic_file]



    def compititor_srch_pd(self):
        link1 ="http://pro.similarweb.com/website/analysis/#/%s/*/999/%s/competitors/search?selectedTab=paid"
        link1 = link1 %(self.domain, self.dte)

        link1a = "http://pro.similarweb.com/export/analysis/GetPaidSearchCompetitorsTsv?selectedTab=paid&key="+ self.domain +"&country=999&from=2013|10&to=2014|3&orderby=Score%20desc"

        self.compititor_srch_pd_visit = self.trf_srch_grp_1_2_3(link1, link1a)
        self.compititor_srch_pd_file = self.find_file_csv(os.getcwd(), "*.csv", "compititor_srch_pd_file.csv")

        return [self.compititor_srch_pd_file]



def supermain():
    f = open("nexusdialer_entry.txt", "a+")

    obj = pro_similar("amazon.com", "12m")
    obj.login_fun()
    obj.domain_and_date()

    print >>f, obj.date_conversion() 
    '''print >>f, obj.web_aud_over()
    print >>f, obj.web_geo()
    print >>f, obj.web_audin() 
    print >>f, obj.trafic_pd_org_all_src()
    print >>f, obj.trf_po_srch_grp1()
    print >>f, obj.trf_po_srch_grp2()
    print >>f, obj.trf_po_srch_grp3()
    print >>f, obj.trafic_org_all_src()
    print >>f, obj.trf_o_srch_grp1()
    print >>f, obj.trf_o_srch_grp2()
    print >>f, obj.trf_o_srch_grp3()    
    print >>f, obj.trafic_p_all_src()
    print >>f, obj.trf_p_srch_grp1()
    print >>f, obj.trf_p_srch_grp2()
    print >>f, obj.trf_p_srch_grp3()
    print >>f, obj.traff_dest()
    print >>f, obj.web_cont_sub()
    print >>f, obj.web_cont_sub_pop_page()
    print >>f, obj.web_cont_sub_led_folder()
    print >>f, obj.compititor_simil()
    print >>f, obj.compititor_srch_orgnic()
    print >>f, obj.compititor_srch_pd()'''

    f.close()
    
       

if __name__=="__main__":
    s = datetime.now()
    supermain()
    e = datetime.now()
    print [e - s]

