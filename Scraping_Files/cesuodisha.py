from typing import Optional, Any
from Objects import globalvar
from datetime import datetime
import time
import urllib.request
import urllib.parse
import string
import re
from Insert_data.Insert_data import *
import sys, os
from bs4 import BeautifulSoup
from selenium import webdriver


def Scraping_function(Source):
    Error_text = ''
    source_Done_OR_Not = ''
    Process_End = ''
    browser = webdriver.Chrome('D:\\PycharmProjects\\ALL Exe Project\\chromedriver.exe')
    browser.get('https://cesuodisha.com/new_website/current_tendernew.html')
    time.sleep(2)
    a = 0
    while a < 3:
        try:
            tr_count = 3
            global loop
            loop = 0
            while loop == 0:
                SegField = []
                for data in range(43):
                    SegField.append('')
                # ======================================================================================================

                Tr_details = ''
                for Tr_details in browser.find_elements_by_xpath(
                        '/html/body/div/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[2]/td[2]/table/tbody/'
                        'tr[2]/td/table/tbody/tr[3]/td/table/tbody/tr[2]/td[2]/table/tbody/tr[' + str(tr_count) + ']'):
                    Tr_details = Tr_details.get_attribute('innerHTML')
                    break

                # ======================================================================================================

                Tr_details = re.sub(' +', ' ', str(Tr_details)).replace('\n', '').replace('&amp;', '&').replace(
                    '”', '').replace('&nbsp;', ' ').replace('.,', '')
                soup = BeautifulSoup(Tr_details, 'html.parser')
                soup_td = soup.find_all('td')
                td = []
                for i in soup_td:
                    i = str(i).replace('\n', '').replace('&amp;','&').replace('”', '').replace('&nbsp;', ' ').replace('.,', '')
                    td.append(i)
                # ======================================================================================================

                Submission_date = str(td[3]).partition("<b>")[2].partition("</b>")[0].strip()
                clean = re.compile('<.*?>')  # remove html tag from string
                Submission_date = re.sub(clean, '', Submission_date)
                Submission_date = re.sub('\s+', '', Submission_date)  # remove Multiple spaces from string
                if Submission_date != '':
                    try:
                        Submission_date = datetime.strptime(Submission_date, '%d/%m/%Y')
                        Submission_date = Submission_date.strftime("%Y-%m-%d")
                        SegField[24] = Submission_date
                    except:pass
                else:pass

                # ======================================================================================================

                SegField[1] = 'itadmin@cescoorissa.com'
                SegField[
                    2] = '2nd Floor, Idco Tower, Janpath, Bhubaneswar - 751022\n Tel: 0674-2541575 \n Fax: 0674-2543125'
                SegField[3] = "NA~NA~NA~NA~NA"
                SegField[
                    8] = 'http://www.cescoorissa.com or http://www.cesuodisha.com'  # Enter Here source website Its IMP
                globalvar.Country = 'IN'  # change only Country CODE
                SegField[7] = globalvar.Country
                SegField[20] = "0.0"  # Bid_Amount
                SegField[22] = "0.0"  # doc_cost
                SegField[26] = "0.0"  # earnest_money
                SegField[27] = "0"  # Financier
                SegField[28] = 'http://117.239.112.120/current-tenders_new.html'
                SegField[31] = "cesuodisha.com"  # Source Name IMP
                SegField[14] = "2"  # notice_type
                SegField[12] = "CENTRAL ELECTRICITY SUPPLY UTILITY OF ODISHA"

                # ======================================================================================================

                Tender_code = str(td[2]).partition("<a")[2].partition("</a>")[0]
                Tender_code_href = str(Tender_code).partition('href="')[2].partition('"')[0]
                if Tender_code_href != '':
                    Tender_code_href = 'http://117.239.112.120/' + Tender_code_href
                else:
                    Tender_code_href = ''
                Tender_code_name = str(Tender_code).partition(">")[2].strip()
                SegField[41] = Tender_code_name
                SegField[39] = Tender_code_href

                # ======================================================================================================

                BID_DOC = str(td[4]).partition('href="')[2].partition('"')[0].strip()
                if BID_DOC != '':
                    BID_DOC = 'http://117.239.112.120/' + BID_DOC
                    SegField[40] = BID_DOC
                else:pass

                # ======================================================================================================

                Corrigendum_Doc_list = re.findall(r"(?<=href=\").*?(?=</a>)", str(td[5]))
                try:  # if Document not Found
                    Corrigendum_Doc_link = str(Corrigendum_Doc_list[0]).partition('href="')[2].partition('">')[
                        0].strip()
                    if Corrigendum_Doc_list != '':
                        Corrigendum_Doc_link = 'http://117.239.112.120/' + Corrigendum_Doc_link
                        SegField[42] = Corrigendum_Doc_link
                    else:pass
                except:
                    pass

                # ======================================================================================================

                soup = BeautifulSoup(str(td[0]), 'html.parser')
                p = soup.find_all('p')
                Tender_no = str(p[0]).partition("Tender No")[2].partition("</font>")[0].strip().replace('.', '').\
                    replace(':', '').lstrip()
                SegField[13] = Tender_no
                # print(Tender_no)

                # ======================================================================================================

                Details_date = str(p[0]).partition("dt.")[2].partition("</p>")[0].strip()
                clean = re.compile('<.*?>')  # remove html tag from string
                Details_date = re.sub(clean, '', Details_date)
                Details_date = re.sub('\s+', '', Details_date)  # remove Multiple spaces from string
                SegField[4] = Details_date
                # print(date)

                # ======================================================================================================

                Title = str(p[1]).partition("<p")[2].partition("</p>")[0].strip()
                clean = re.compile('<.*?>')  # remove html tag from string
                Title = re.sub(clean, '', Title)
                Title = re.sub('\s+', ' ', Title)  # remove Multiple spaces from string
                Title = str(Title).partition(">")[2].strip()
                SegField[19] = Title
                # ======================================================================================================
                for Segdata in range(len(SegField)):
                    print(Segdata, end=' ')
                    print(SegField[Segdata])
                Check_DeadLine_Function(SegField,Source)
                Process_End = 'Total: ' + str(globalvar.Total) + " " + "Duplicate: " + str(
                    globalvar.Duplicate) + " " + "Expired: " + str(
                    globalvar.Expired) + " " + "Inserted: " + str(
                    globalvar.Inserted) + " " + "Skipped: " + str(
                    globalvar.Skipped) + " " + "Deadline Not Given: " + str(
                    globalvar.Deadline) + " " + "Qc Tenders: " + str(globalvar.Qc_Tenders)
                print('Source Name: cesuodisha.com ', Process_End)
                loop = 0
                tr_count += 1
            a = 3
            source_Done_OR_Not = 'Done'
            browser.close()
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            Error_text = "Source Name : " + str(Source) + " Error ON : " + str(
                sys._getframe().f_code.co_name) + " ---> " + str(e) + " , " + str(
                exc_type) + " , " + str(fname) + "<br> Error Line Number: " + str(exc_tb.tb_lineno)
            print(Error_text)
            a += 1
            source_Done_OR_Not = 'Error'
            time.sleep(5)
    if source_Done_OR_Not == "Error":
        globalvar.html_string += """<tr bgcolor=\"#e8eff1\" onmouseover=\"this.style.backgroundColor='#d6edf5'\" onmouseout=\"this.style.backgroundColor=''\">
                    <td style=\"padding:7px;\" ><font color=\"#A34DF3\">""" + str(Source) + """</font></td>
                    <td style=\"padding:7px;\"><font color=\"#FF005D\">""" + str(Error_text) + """</td>
                  </tr>"""
        browser.close()
    elif source_Done_OR_Not == "Done":
        globalvar.html_string += """<tr bgcolor=\"#e8eff1\" onmouseover=\"this.style.backgroundColor='#d6edf5'\" onmouseout=\"this.style.backgroundColor=''\">
                        <td style=\"padding:7px;\" ><font color=\"#A34DF3\">""" + str(Source) + """</font></td>
                        <td style=\"padding:7px;\"><font color=\"#007816\">""" + str(Process_End) + """</font></td>
                      </tr>"""


def Check_DeadLine_Function(SegField,Source):
    nowdate = datetime.now()
    date2 = nowdate.strftime("%Y-%m-%d")
    try:
        current_date = time.strptime(date2, "%Y-%m-%d")
        if str(SegField[24]) != '':
            if str(SegField[24]) > str(current_date):
                Create_HTML_string(SegField, Source)
            else:
                print("Expired")
                globalvar.Expired += 1
        else:
            print('Deadline Not Given')
            globalvar.Deadline += 1
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        Error_text = "Source Name : " + str(Source) + " Error ON : " + str(
            sys._getframe().f_code.co_name) + " ---> " + str(e) + " , " + str(
            exc_type) + " , " + str(fname) + "<br> Error Line Number: " + str(exc_tb.tb_lineno)
        print(Error_text)


def Create_HTML_string(SegField,Source):
    try:
        Html_wala_Tag = "<table align=\"center\" border=\"1\" style=\"width:98%;border-spacing:0;border-collapse: collapse;border:1px solid #666666; margin-top:5px; margin-bottom:5px;\">" + \
                        "<tr><td colspan=\"2\"; style=\"background-color:#146faf; font-weight: bold; padding:7px;border-bottom:1px solid #666666; color:white;\">Tender Details</td></tr>" + \
                        "<tr bgcolor=\"#ffffff\" onmouseover=\"this.style.backgroundColor='#def3ff'\" onmouseout=\"this.style.backgroundColor=''\"><td style=\"padding:7px;\">Purchaser Name</td><td style=\"padding:7px;\">" + str(
            SegField[12]) + "</td></tr>" + \
                        "<tr bgcolor=\"#ffffff\" onmouseover=\"this.style.backgroundColor='#def3ff'\" onmouseout=\"this.style.backgroundColor=''\"><td style=\"padding:7px;\">Tender ID</td><td style=\"padding:7px;\">" + str(
            SegField[13]) + "</td></tr>" + \
                        "<tr bgcolor=\"#ffffff\" onmouseover=\"this.style.backgroundColor='#def3ff'\" onmouseout=\"this.style.backgroundColor=''\"><td style=\"padding:7px;\">Title</td><td style=\"padding:7px;\">" + str(
            SegField[19]) + "</td></tr>" + \
                        "<tr bgcolor=\"#ffffff\" onmouseover=\"this.style.backgroundColor='#def3ff'\" onmouseout=\"this.style.backgroundColor=''\"><td style=\"padding:7px;\">Update Date</td><td style=\"padding:7px;\">" + str(SegField[4]) + "</td></tr>" + \
                        "<tr bgcolor=\"#ffffff\" onmouseover=\"this.style.backgroundColor='#def3ff'\" onmouseout=\"this.style.backgroundColor=''\"><td style=\"padding:7px;\">Opening</td><td style=\"padding:7px;\">" + str(SegField[24]) + "</td></tr>" + \
                        "<tr bgcolor=\"#ffffff\" onmouseover=\"this.style.backgroundColor='#def3ff'\" onmouseout=\"this.style.backgroundColor=''\"><td style=\"padding:7px;\">Tender Code</td><td style=\"padding:7px;\"><a href=" + str(SegField[39]) + " target=\"_blank\">"+str(SegField[41])+"</a>""</td></tr>" \
                        "<tr bgcolor=\"#ffffff\" onmouseover=\"this.style.backgroundColor='#def3ff'\" onmouseout=\"this.style.backgroundColor=''\"><td style=\"padding:7px;\">Corrigendum</td><td style=\"padding:7px;\"><a href=" + str(SegField[42]) + " target=\"_blank\">View</a>""</td></tr>" \
                        "<tr bgcolor=\"#ffffff\" onmouseover=\"this.style.backgroundColor='#def3ff'\" onmouseout=\"this.style.backgroundColor=''\"><td style=\"padding:7px;\">Bid Doc </td><td style=\"padding:7px;\"><a href=" + str(SegField[40]) + " target=\"_blank\">View</a>""</td></tr>" + "</tr></table>"

        globalvar.HTML_File_String = "<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Transitional//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\"><html xmlns=\"http://www.w3.org/1999/xhtml\">" + \
                                     "<head><link rel=\"shortcut icon\" type=\"image/png\" href=\"https://www.tendersontime.com/favicon.ico\"/></head>" \
                                     "<body>" + Html_wala_Tag + "</body></html>"

        # ========================================================================================================
        # L2L Object's add value very carefully

        globalvar.ncb_icb = 'ncb'
        globalvar.search_id = '1'
        globalvar.cpv_userid = ""
        globalvar.dms_entrynotice_tblquality_status = '1'
        globalvar.quality_id = '1'
        globalvar.quality_addeddate = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        globalvar.Col1 = 'http://www.cesuodisha.com'
        globalvar.Col2 = str(SegField[26]) + " * " + str(SegField[20])  # For India Only Other Wise Blank
        globalvar.Col3 = ''
        globalvar.Col4 = ''
        globalvar.Col5 = str(SegField[3])
        globalvar.dms_downloadfiles_tbluser_id = 'DWN00541021'
        # Europe-DWN2554488,India-DWN00541021,Asia-DWN5046627,Africa-DWN302520,North America-DWN1011566,
        # South America-DWN1456891,Semi-Auto-DWN30531073,MFA-DWN0654200
        globalvar.selector_id = ''
        Check_Duplicate_Function(SegField,Source)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        Error_text = "Source Name : " + str(Source) + " Error ON : " + str(
            sys._getframe().f_code.co_name) + " ---> " + str(e) + " , " + str(
            exc_type) + " , " + str(fname) + "<br> Error Line Number: " + str(exc_tb.tb_lineno)
        print(Error_text)
Scraping_function('Source')