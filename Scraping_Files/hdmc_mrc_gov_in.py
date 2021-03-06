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


def Scraping_function(Source):
    Error_text = ''
    source_Done_OR_Not = ''
    Process_End = ''
    a = 0
    while a < 3:
        try:
            user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
            headers = {'User-Agent': user_agent}
            request = urllib.request.Request('http://www.hdmc.mrc.gov.in/en/Tenders', None, headers)  # The assembled request
            response = urllib.request.urlopen(request)
            html_data = response.read().decode('utf-8')
            soup = BeautifulSoup(html_data, 'html.parser')
            table = soup.find("table", attrs={"class": "table-striped"})
            tr_list = table.find_all("tr")
            del tr_list[0]  # Remove First List From td_list
            # del tr_list[-1]  # Remove last List From td_list
            for td in tr_list:
                SegField = []
                for data in range(42):
                    SegField.append('')
                SegField[1] = 'commissioner.hdmc@gmail.com'
                SegField[2] = 'Hubballi-Dharwad City Corporation, Sir Siddappa Kambali Road, Hubballi - 580020<br>\n Tel: 0836-2213888'
                SegField[3] = "NA~NA~NA~NA~NA"
                SegField[8] = 'http://www.hdmc.mrc.gov.in'  # Enter Here source website Its IMP
                globalvar.Country = 'IN'  # change only Country CODE
                SegField[7] = globalvar.Country
                SegField[20] = "0.0"  # Bid_Amount
                SegField[22] = "0.0"  # doc_cost
                SegField[26] = "0.0"  # earnest_money
                SegField[27] = "0"  # Financier
                SegField[28] = 'http://www.hdmc.mrc.gov.in/en/Tenders'
                SegField[31] = "hdmc.mrc.gov.in"
                SegField[14] = "2"  # notice_type

                # ======================================================================================================

                td = str(td).replace('\n', '').replace('&amp;', '&').replace('”', '').replace('&nbsp;', ' ').replace('.,', '')
                soup = BeautifulSoup(td, 'html.parser')
                td = soup.find_all('td')
                # print(td)
                # ======================================================================================================

                clean = re.compile('<.*?>')
                Publish_Date = re.sub(clean, '', str(td[3]))
                SegField[6] = Publish_Date.strip()
                # print(Publish_Date)

                clean = re.compile('<.*?>')
                submission_date = re.sub(clean, '', str(td[4])).strip()
                if submission_date != '':
                    submission_date = datetime.strptime(submission_date, '%d-%m-%Y')
                    submission_date = submission_date.strftime("%Y-%m-%d")
                    SegField[24] = submission_date
                    # print(submission_date)
                # ==============================================================================================

                Title = str(td[1]).partition(">")[2].partition("</td>")[0].strip()
                Title = string.capwords(str(Title)).strip()
                SegField[19] = Title
                # print(Title)

                # ==============================================================================================

                Department = str(td[2]).partition(">")[2].partition("</td>")[0].strip()
                if 'EE North' in Department:
                    SegField[12] = 'HUBBALLI-DHARWAD CITY CORPORATION-EE NORTH'
                elif 'EE Dharwad' in Department :
                    SegField[12] = 'HUBBALLI-DHARWAD CITY CORPORATION-EE DHARWAD'
                # print(SegField[12])

                Document = str(td[5]).partition("href=\"")[2].partition('"')[0].strip()
                Document = 'http://www.hdmc.mrc.gov.in'+Document
                # print(Document)

                # ======================================================================================================
                SegField[5] = Document
                SegField[18] = str(SegField[19]) + '<br>\n Department: ' + str(SegField[12]) + '<br>\nPublish Date : ' + str(SegField[6]) + '<br>\nSubmission Date : ' + str(SegField[24])
                SegField[18] = string.capwords(str(SegField[18]))

                for Segdata in range(len(SegField)):
                    print(Segdata, end=' ')
                    print(SegField[Segdata])
                Check_DeadLine_Function(SegField,Department,Source)
                globalvar.Total += 1
                Process_End = 'Total: ' + str(globalvar.Total) + " " + "Duplicate: " + str(
                    globalvar.Duplicate) + " " + "Expired: " + str(globalvar.Expired) + " " + "Inserted: " + str(
                    globalvar.Inserted) + " " + "Skipped: " + str(globalvar.Skipped) + " " + "Deadline Not Given: " + str(
                    globalvar.Deadline) + " " + "Qc Tenders: " + str(globalvar.Qc_Tenders)
                print('Source Name: hdmc.mrc.gov.in ', Process_End)
                if str(globalvar.Expired) == '1':
                    break
            a = 3
            source_Done_OR_Not = 'Done'
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
                    <td style=\"padding:7px;\" ><font color=\"#A34DF3\">"""+str(Source)+"""</font></td>
                    <td style=\"padding:7px;\"><font color=\"#FF005D\">"""+str(Error_text)+"""</td>
                  </tr>"""
    elif source_Done_OR_Not == "Done":
        globalvar.html_string += """<tr bgcolor=\"#e8eff1\" onmouseover=\"this.style.backgroundColor='#d6edf5'\" onmouseout=\"this.style.backgroundColor=''\">
                        <td style=\"padding:7px;\" ><font color=\"#A34DF3\">"""+str(Source)+"""</font></td>
                        <td style=\"padding:7px;\"><font color=\"#007816\">""" + str(Process_End) + """</font></td>
                      </tr>"""


def Check_DeadLine_Function(SegField,Department,Source):
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
            globalvar.Deadline +=1
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        Error_text = "Source Name : " + str(Source) + " Error ON : " + str(
            sys._getframe().f_code.co_name) + " ---> " + str(e) + " , " + str(
            exc_type) + " , " + str(fname) + "<br> Error Line Number: " + str(exc_tb.tb_lineno)
        print(Error_text)


def Create_HTML_string(SegField,Department,Source):

    try:
        Html_wala_Tag = "<table align=\"center\" border=\"1\" style=\"width:98%;border-spacing:0;border-collapse: collapse;border:1px solid #666666; margin-top:5px; margin-bottom:5px;\">" + \
                        "<tr><td colspan=\"2\"; style=\"background-color:#146faf; font-weight: bold; padding:7px;border-bottom:1px solid #666666; color:white;\">Tender Details</td></tr>" + \
                        "<tr bgcolor=\"#ffffff\" onmouseover=\"this.style.backgroundColor='#def3ff'\" onmouseout=\"this.style.backgroundColor=''\"><td style=\"padding:7px;\">Title</td><td style=\"padding:7px;\">" + str(SegField[19]) + "</td></tr>" + \
                        "<tr bgcolor=\"#ffffff\" onmouseover=\"this.style.backgroundColor='#def3ff'\" onmouseout=\"this.style.backgroundColor=''\"><td style=\"padding:7px;\">Department</td><td style=\"padding:7px;\">" + str(Department) + "</td></tr>" + \
                        "<tr bgcolor=\"#ffffff\" onmouseover=\"this.style.backgroundColor='#def3ff'\" onmouseout=\"this.style.backgroundColor=''\"><td style=\"padding:7px;\">Purchaser Name</td><td style=\"padding:7px;\">" + str('HUBBALLI-DHARWAD CITY CORPORATION') + "</td></tr>" + \
                        "<tr bgcolor=\"#ffffff\" onmouseover=\"this.style.backgroundColor='#def3ff'\" onmouseout=\"this.style.backgroundColor=''\"><td style=\"padding:7px;\">Publish Date</td><td style=\"padding:7px;\">" + str(SegField[6]) + "</td></tr>" + \
                        "<tr bgcolor=\"#ffffff\" onmouseover=\"this.style.backgroundColor='#def3ff'\" onmouseout=\"this.style.backgroundColor=''\"><td style=\"padding:7px;\">Submission Date</td><td style=\"padding:7px;\">" + str(SegField[24]) + "</td></tr>" + \
                         "<tr bgcolor=\"#ffffff\" onmouseover=\"this.style.backgroundColor='#def3ff'\" onmouseout=\"this.style.backgroundColor=''\"><td style=\"padding:7px;\">Document </td><td style=\"padding:7px;\">""<a href=" + str(SegField[5]) + " target=\"_blank\">View</a>""</td></tr>" + "</tr></table>"

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
        globalvar.Col1 = 'http://www.hdmc.mrc.gov.in/'
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
