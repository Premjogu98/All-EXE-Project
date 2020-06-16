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
    global source_Done_OR_Not
    source_Done_OR_Not = ''
    Process_End = ''
    a = 0
    while a < 3:
        try:
            user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
            headers = {'User-Agent': user_agent, }
            request = urllib.request.Request('https://agri.py.gov.in/tenders.html', None, headers)  # The assembled request
            response = urllib.request.urlopen(request)
            html_data = response.read().decode('utf-8')
            updated_date = str(html_data).partition("<tbody>")[2].partition("</tbody>")[0].strip()
            tr_list = updated_date.split('</tr>')

            for td in tr_list:
                SegField = []
                for data in range(42):
                    SegField.append('')
                SegField[1] = 'agri.pon@nic.in'
                SegField[2] = 'New Light House Road, Directorate Of Agriculture, Vambakeerapalayam, Puducherry-1.intercom No.214<br>\nTel: 0413-2336945, 2336543, 2336061<br>\nFax: 0413-2337121'
                SegField[3] = "NA~NA~NA~NA~NA"
                SegField[8] = 'https://agri.py.gov.in'  # Enter Here source website Its IMP
                # =======================================================================================
                globalvar.Country = 'IN'  # change only Country CODE
                SegField[7] = globalvar.Country
                # ========================================================================================
                SegField[20] = "0.0"  # Bid_Amount
                SegField[22] = "0.0"  # doc_cost
                SegField[26] = "0.0"  # earnest_money
                SegField[27] = "0"  # Financier
                SegField[28] = 'https://agri.py.gov.in/tenders.html'
                SegField[31] = "agri.py.gov.in"
                SegField[14] = "2"  # notice_type

                td = str(td).replace('\n', '').replace('&amp;', '&').replace('”', '').replace('&nbsp;', ' ').replace('.,', '')

                td_list = BeautifulSoup(td, 'html.parser')
                td_list = td_list.findAll('td')
                # print(td_list)

                clean = re.compile('<.*?>')
                Title = re.sub(clean, '', str(td_list[0]))
                Title = string.capwords(str(Title))
                Title = Title.partition("- Visit")[0].strip()
                SegField[19] = Title
                # print(Title)

                SegField[12] = 'DEPARTMENT OF AGRICULTURE AND FARMERS WELFARE'

                clean = re.compile('<.*?>')
                Time = re.sub(clean, '', str(td_list[2]))  # remove html tags
                SegField[6] = Time
                # print(Time)

                Document = str(td_list[0]).partition("href=\"")[2].partition("\"")[0].strip()
                Document = 'https://agri.py.gov.in/'+Document
                # print(Document)
                SegField[5] = Document

                clean = re.compile('<.*?>')
                Closing_Date = re.sub(clean, '', str(td_list[1])).strip()
                # print(Closing_Date)
                if Closing_Date != '':
                    Submission_date = datetime.strptime(Closing_Date, '%d-%m-%Y')
                    Submission_date = Submission_date.strftime("%Y-%m-%d")
                    SegField[24] = Submission_date
                    # print(Submission_date)
                SegField[18] = str(Title) + '<br>\n Updated Date: ' + str(SegField[6]) + '<br>\nClosing Date : ' + str(SegField[24]) + '<br>\nTime : ' + str(SegField[6])
                SegField[18] = string.capwords(str(SegField[18]))

                for Segdata in range(len(SegField)):
                    print(Segdata, end=' ')
                    print(SegField[Segdata])
                Check_DeadLine_Function(SegField,Source)
                globalvar.Total += 1
                Process_End = 'Total: ' + str(globalvar.Total) + " " + "Duplicate: " + str(
                    globalvar.Duplicate) + " " + "Expired: " + str(
                    globalvar.Expired) + " " + "Inserted: " + str(
                    globalvar.Inserted) + " " + "Skipped: " + str(
                    globalvar.Skipped) + " " + "Deadline Not Given: " + str(
                    globalvar.Deadline) + " " + "Qc Tenders: " + str(globalvar.Qc_Tenders)+'\n'
                print('Source Name: agri_py_gov_in   ', Process_End)
                if str(globalvar.From_Date) == '1':
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
    elif source_Done_OR_Not == 'Done':
        globalvar.html_string += """<tr bgcolor=\"#e8eff1\" onmouseover=\"this.style.backgroundColor='#d6edf5'\" onmouseout=\"this.style.backgroundColor=''\">
                        <td style=\"padding:7px;\" ><font color=\"#A34DF3\">""" + str(Source) + """</font></td>
                        <td style=\"padding:7px;\"><font color=\"#007816\">""" + str(Process_End) + """</font></td>
                      </tr>"""
        print(Process_End)


def Check_DeadLine_Function(SegField,Source):

    nowdate = datetime.now()
    date2 = nowdate.strftime("%Y-%m-%d")
    try:
        current_date = time.strptime(date2, "%Y-%m-%d")
        if str(SegField[24]) != '':
            if str(SegField[24]) > str(current_date):
                Create_HTML_string(SegField,Source)
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
                        "<tr bgcolor=\"#ffffff\" onmouseover=\"this.style.backgroundColor='#def3ff'\" onmouseout=\"this.style.backgroundColor=''\"><td style=\"padding:7px;\">Purchaser</td><td style=\"padding:7px;\">" + str(
            SegField[12]) + "</td></tr>" + \
                        "<tr bgcolor=\"#ffffff\" onmouseover=\"this.style.backgroundColor='#def3ff'\" onmouseout=\"this.style.backgroundColor=''\"><td style=\"padding:7px;\">Title</td><td style=\"padding:7px;\">" + str(
            SegField[19]) + "</td></tr>" + \
                        "<tr bgcolor=\"#ffffff\" onmouseover=\"this.style.backgroundColor='#def3ff'\" onmouseout=\"this.style.backgroundColor=''\"><td style=\"padding:7px;\">Closing Date</td><td style=\"padding:7px;\">" + str(
            SegField[24]) + "</td></tr>" + \
                        "<tr bgcolor=\"#ffffff\" onmouseover=\"this.style.backgroundColor='#def3ff'\" onmouseout=\"this.style.backgroundColor=''\"><td style=\"padding:7px;\">Time</td><td style=\"padding:7px;\">" + str(
            SegField[6]) + "</td></tr>" + \
                        "<tr bgcolor=\"#ffffff\" onmouseover=\"this.style.backgroundColor='#def3ff'\" onmouseout=\"this.style.backgroundColor=''\"><td style=\"padding:7px;\">Document </td><td style=\"padding:7px;\">""<a href=" + str(
            SegField[5]) + " target=\"_blank\">View</a>""</td></tr>" + "</tr></table>"

        globalvar.HTML_File_String = "<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Transitional//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\"><html xmlns=\"http://www.w3.org/1999/xhtml\">" + \
                           "<head><link rel=\"shortcut icon\" type=\"image/png\" href=\"https://www.tendersontime.com/favicon.ico\"/></head>" + \
                           "<body>" + str(Html_wala_Tag) + "</body></html>"

        # ========================================================================================================
        # L2L Object add value very carefully

        globalvar.ncb_icb = 'ncb'
        globalvar.search_id = '1'
        globalvar.cpv_userid = ""
        globalvar.dms_entrynotice_tblquality_status = '1'
        globalvar.quality_id = '1'
        globalvar.quality_addeddate = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        globalvar.Col1 = 'https://agri.py.gov.in'
        globalvar.Col2 = str(SegField[26]) + " * " + str(SegField[20])  # For India Only Other Wise Blank
        globalvar.Col3 = ''
        globalvar.Col4 = ''
        globalvar.Col5 = str(SegField[3])
        globalvar.dms_downloadfiles_tbluser_id = 'DWN00541021'
        # Europe-DWN2554488,India-DWN00541021,Asia-DWN5046627,Africa-DWN302520,North America-DWN1011566,
        # South America-DWN1456891,Semi-Auto-DWN30531073,MFA-DWN0654200
        globalvar.selector_id = ''
        Check_Duplicate_Function(SegField, Source)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        Error_text = "Source Name : " + str(Source) + " Error ON : " + str(
            sys._getframe().f_code.co_name) + " ---> " + str(e) + " , " + str(
            exc_type) + " , " + str(fname) + "<br> Error Line Number: " + str(exc_tb.tb_lineno)
        print(Error_text)


