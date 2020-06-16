from Objects import globalvar
import time
import sys, os
import mysql.connector
from datetime import datetime


def Local_Connection_Function():
    a = 0
    while a == 0:
        try:
            if globalvar.Country == 'IN':
                mydb_Local = mysql.connector.connect(
                    host='192.168.0.202',
                    user='ams',
                    passwd='amsbind',
                    database='Tenders_India')
                print('SQL Local Connection Connected')
                return mydb_Local
            else:
                pass
        except mysql.connector.ProgrammingError as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            Error_text = "Error ON : " + " " + str(sys._getframe().f_code.co_name) + " ---> " + str(e) + " , " + str(
                exc_type) + " , " + str(fname) + "<br> Error Line Number: " + str(exc_tb.tb_lineno)
            print(Error_text)
            a = 0


def L2L_Connection_Function():
    a = 0
    while a == 0:
        try:
            if globalvar.Country == 'IN':
                mydb_L2L = mysql.connector.connect(
                    host='192.168.0.202',
                    user='ams',
                    passwd='amsbind',
                    database='AMS_Master_FinalDB')
                print('SQL Connected L2L_connection')
                print("Live Tender")
                return mydb_L2L
            else:
                pass
        except mysql.connector.ProgrammingError as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            Error_text = "Error ON : " + " " + str(sys._getframe().f_code.co_name) + " ---> " + str(e) + " , " + str(
                exc_type) + " , " + str(fname) + "<br> Error Line Number: " + str(exc_tb.tb_lineno)
            print(Error_text)
            a = 0


def Check_Duplicate_Function(SegField,Source):
    a = 0
    while a == 0:
        try:
            mydb_Local = Local_Connection_Function()
            mycursorLocal = mydb_Local.cursor()
            if SegField[13] != '' and SegField[24] != '' and SegField[7] != '':
                commandText = "SELECT Posting_Id from Tenders where tender_notice_no = '" + str(
                    SegField[13]) + "' and Country = '" + str(SegField[7]) + "' and doc_last= '" + str(
                    SegField[24]) + "'"
            elif SegField[13] != "" and SegField[7] != "":
                commandText = "SELECT Posting_Id from Tenders where tender_notice_no = '" + str(
                    SegField[13]) + "' and Country = '" + str(SegField[7]) + "'"
            elif SegField[19] != "" and SegField[24] != "" and SegField[7] != "":
                commandText = "SELECT Posting_Id from Tenders where short_desc = '" + str(
                    SegField[19]) + "' and doc_last = '" + SegField[24] + "' and Country = '" + SegField[7] + "'"
            else:
                commandText = "SELECT Posting_Id from Tenders where short_desc = '" + str(
                    SegField[19]) + "' and Country = '" + str(SegField[7]) + "'"
            mycursorLocal.execute(commandText)
            results = mycursorLocal.fetchall()
            if len(results) > 0:
                print('Duplicate Tender')
                globalvar.Duplicate += 1
            else:
                print('Live Tender')
                CreateHTMLFileFunction(SegField,Source)
            a = 1
        except Exception as e:
            Local_Connection_Function().close()
            mydb_L2L = L2L_Connection_Function()
            mycursorL2L = mydb_L2L.cursor()
            Function_name: str = sys._getframe().f_code.co_name
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            Error_text = "Source Name : "+str(Source)+" Error ON : " + str(sys._getframe().f_code.co_name) + " ---> " + str(e) + " , " + str(
                exc_type) + " , " + str(fname) + "<br> Error Line Number: " + str(exc_tb.tb_lineno)

            sql1 = "INSERT INTO ErrorLog(Error_Message,Function_Name,Exe_Name) VALUES('" + str(Error_text).replace("'",
                                                                                                                   "") + "','" + str(
                Function_name).replace("'", "") + "','" + str(SegField[31]) + "')"
            mycursorL2L.execute(sql1)
            mydb_L2L.commit()
            print(Error_text)
            a = 0
            time.sleep(10)


def CreateHTMLFileFunction(SegField,Source):
    a = 0
    while a == 0:
        try:
            basename = 'PY'
            Current_dateTime = datetime.now().strftime("%Y%m%d%H%M%S%f")
            Fileid = "".join([basename, Current_dateTime])
            File_path = 'D:\\' + Fileid + '.html'
            file1 = open(File_path, "w", encoding='utf-8')
            file1.write(str(globalvar.HTML_File_String))
            file1.close()
            time.sleep(2)
            Insert_In_Local_Function(SegField, Fileid,Source)
            a = 1
        except Exception as e:
            mydb_L2L = L2L_Connection_Function()
            mycursorL2L = mydb_L2L.cursor()
            Function_name: str = sys._getframe().f_code.co_name
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            Error_text = "Source Name : " + str(Source) + " Error ON : " + str(
                sys._getframe().f_code.co_name) + " ---> " + str(e) + " , " + str(
                exc_type) + " , " + str(fname) + "<br> Error Line Number: " + str(exc_tb.tb_lineno)

            sql1 = "INSERT INTO ErrorLog(Error_Message,Function_Name,Exe_Name) VALUES('" + str(Error_text).replace("'",
                                                                                                                   "") + "','" + str(
                Function_name).replace("'", "") + "','" + str(SegField[31]) + "')"
            mycursorL2L.execute(sql1)
            mydb_L2L.commit()
            print(Error_text)
            a = 0
            time.sleep(10)


def Insert_In_Local_Function(SegField, Fileid,Source):
    a = 0
    while a == 0:
        try:
            mydb_Local = Local_Connection_Function()
            mycursorLocal = mydb_Local.cursor()
            sql = "INSERT INTO Tenders(EMail,add1,Country,Maj_Org,tender_notice_no,notice_type,Tenders_details,short_desc,est_cost,currency,doc_cost,doc_last,earnest_money,Financier,tender_doc_file,source)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "
            val = (str(SegField[1]), str(SegField[2]), str(SegField[7]), str(SegField[12]), str(SegField[13]),
                   str(SegField[14]),
                   str(SegField[18]), str(SegField[19]), str(SegField[20]), str(SegField[21]), str(SegField[22]),
                   str(SegField[24]), str(SegField[26]), str(SegField[27]),
                   str(SegField[28]), str(SegField[31]))
            mycursorLocal.execute(sql, val)
            mydb_Local.commit()
            globalvar.Inserted += 1
            print("Code Reached On insert_in_Local")
            Insert_In_L2L_Function(SegField, Fileid)
            a = 1
        except Exception as e:
            mydb_L2L = L2L_Connection_Function()
            mycursorL2L = mydb_L2L.cursor()
            Function_name: str = sys._getframe().f_code.co_name
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            Error_text = "Source Name : " + str(Source) + " Error ON : " + str(
                sys._getframe().f_code.co_name) + " ---> " + str(e) + " , " + str(
                exc_type) + " , " + str(fname) + "<br> Error Line Number: " + str(exc_tb.tb_lineno)

            sql1 = "INSERT INTO ErrorLog(Error_Message,Function_Name,Exe_Name) VALUES('" + str(Error_text).replace("'",
                                                                                                                   "") + "','" + str(
                Function_name).replace("'", "") + "','" + str(SegField[31]) + "')"
            mycursorL2L.execute(sql1)
            mydb_L2L.commit()
            print(Error_text)
            a = 0
            time.sleep(10)


def Insert_In_L2L_Function(SegField, Fileid,Source):
    ncb_icb = globalvar.ncb_icb
    added_on = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    search_id = globalvar.search_id
    cpv_userid = globalvar.cpv_userid
    dms_entrynotice_tblquality_status = globalvar.dms_entrynotice_tblquality_status
    quality_id = globalvar.quality_id
    Col1 = SegField[4]
    Col2 = str(SegField[26]) + " * " + str(SegField[20])  # For India Only Other Wise Blank
    Col3 = globalvar.Col3
    Col4 = globalvar.Col4
    Col5 = SegField[3]
    file_name = "D:\\Tide\\DocData\\" + Fileid + ".html"
    dms_downloadfiles_tbluser_id = globalvar.dms_downloadfiles_tbluser_id
    # Europe-DWN2554488,India-DWN00541021,Asia-DWN5046627,Africa-DWN302520,North America-DWN1011566,
    # South America-DWN1456891,Semi-Auto-DWN30531073,MFA-DWN0654200
    selector_id = globalvar.selector_id
    select_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    quality_addeddate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if SegField[36] == "":
        dms_entrynotice_tblstatus = "1"
        dms_downloadfiles_tblsave_status = '1'
        dms_downloadfiles_tblstatus = '1'
        dms_entrynotice_tbl_cqc_status = '1'
    else:
        dms_entrynotice_tblstatus = "2"
        dms_downloadfiles_tblsave_status = '2'
        dms_downloadfiles_tblstatus = '1'
        dms_entrynotice_tbl_cqc_status = '2'
    dms_downloadfiles_tbldatatype = "A"
    dms_entrynotice_tblnotice_type = '2'
    mydb_L2L = L2L_Connection_Function()
    mycursorL2L = mydb_L2L.cursor()
    if SegField[12] != "" and SegField[19] != "" and SegField[24] != "" and SegField[7] != "" and SegField[2] != "":
        dms_entrynotice_tblcompulsary_qc = "2"
    else:
        dms_entrynotice_tblcompulsary_qc = "1"
        b = 0
        while b == 0:
            try:
                mydb_L2L = L2L_Connection_Function()
                mycursorL2L = mydb_L2L.cursor()
                globalvar.Qc_Tenders += 1
                sql = "INSERT INTO QCTenders (Source,tender_notice_no,short_desc,doc_last,Maj_Org,Address,doc_path,Country)VALUES(%s,%s,%s,%s,%s,%s,%s,%s) "
                val = (
                    str(SegField[31]), str(SegField[13]), str(SegField[19]), str(SegField[24]), str(SegField[12]),
                    str(SegField[2]),
                    "http://tottestupload3.s3.amazonaws.com/" + Fileid + ".html", str(SegField[7]))
                mycursorL2L.execute(sql, val)
                mydb_L2L.commit()
                print("Code Reached On insert_L2L")
                b = 1
            except Exception as e:
                mydb_L2L = L2L_Connection_Function()
                mycursorL2L = mydb_L2L.cursor()
                Function_name: str = sys._getframe().f_code.co_name
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                Error_text = "Source Name : " + str(Source) + " Error ON : " + str(
                    sys._getframe().f_code.co_name) + " ---> " + str(e) + " , " + str(
                    exc_type) + " , " + str(fname) + "<br> Error Line Number: " + str(exc_tb.tb_lineno)
                sql1 = "INSERT INTO ErrorLog(Error_Message,Function_Name,Exe_Name) VALUES('" + str(Error_text).replace(
                    "'",
                    "") + "','" + str(
                    Function_name).replace("'", "") + "','" + str(SegField[31]) + "')"
                mycursorL2L.execute(sql1)
                mydb_L2L.commit()

                print(Error_text)
                b = 0
                time.sleep(10)
    a = 0
    while a == 0:
        try:
            mydb_L2L = L2L_Connection_Function()
            mycursorL2L = mydb_L2L.cursor()
            sql = "INSERT INTO Final_Tenders(notice_no,file_id,purchaser_name,deadline,country,description,purchaser_address,purchaser_email,purchaser_url,purchaser_emd,purchaser_value,financier,deadline_two,tender_details,ncbicb,status,added_on,search_id,cpv_value,cpv_userid,quality_status,quality_id,quality_addeddate,source,tender_doc_file,Col1,Col2,Col3,Col4,Col5,file_name,user_id,status_download_id,save_status,selector_id,select_date,datatype,compulsary_qc,notice_type,cqc_status,DocCost,DocLastDate)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "
            val = (str(SegField[13]), Fileid, str(SegField[12]), str(SegField[24]), str(SegField[7]), str(SegField[19]),
                   str(SegField[2]), str(SegField[1]), str(SegField[8]), str(SegField[26]), str(SegField[20]),
                   str(SegField[27]), str(SegField[24]), str(SegField[18]), ncb_icb, dms_entrynotice_tblstatus,
                   str(added_on),
                   search_id, str(SegField[36]), cpv_userid, dms_entrynotice_tblquality_status, quality_id,
                   str(quality_addeddate), str(SegField[31]), str(SegField[28]), Col1, Col2, Col3, Col4, Col5, file_name,
                   dms_downloadfiles_tbluser_id, dms_downloadfiles_tblstatus, dms_downloadfiles_tblsave_status, selector_id,
                   str(select_date), dms_downloadfiles_tbldatatype, dms_entrynotice_tblcompulsary_qc,
                   dms_entrynotice_tblnotice_type, dms_entrynotice_tbl_cqc_status, str(SegField[22]), str(SegField[41]))
            mycursorL2L.execute(sql, val)
            mydb_L2L.commit()
            a = 1
        except Exception as e:
            mydb_L2L = L2L_Connection_Function()
            mycursorL2L = mydb_L2L.cursor()
            Function_name: str = sys._getframe().f_code.co_name
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            Error_text = "Source Name : " + str(Source) + " Error ON : " + str(
                sys._getframe().f_code.co_name) + " ---> " + str(e) + " , " + str(
                exc_type) + " , " + str(fname) + "<br> Error Line Number: " + str(exc_tb.tb_lineno)
            sql1 = "INSERT INTO ErrorLog(Error_Message,Function_Name,Exe_Name) VALUES('" + str(Error_text).replace("'",
                                                                                                                   "") + "','" + str(
                Function_name).replace("'", "") + "','" + str(SegField[31]) + "')"
            mycursorL2L.execute(sql1)
            mydb_L2L.commit()
            print(Error_text)
            a = 0
            time.sleep(10)
