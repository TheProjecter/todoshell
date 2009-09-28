import sqlite3
import sys
import datetime

def org2sqlite(fp_org,fp_db):
    fp_org = file(fp_org)
    conn = sqlite3.connect(fp_db)                                                                                                   
    c = conn.cursor()
    while True:
        ln = fp_org.readline()
        if len(ln) == 0:
            break
        sql = str()
        if cmp(ln[0],"*") == 0:
            #print ln
            if cmp(ln[2:6],"DONE") == 0:
            	
                dt_create = str(datetime.date.today())[0:10]
                dt_end = str(datetime.date.today())[0:10]
                str_subject = ln[7:]
                sql = "insert into task values (NULL,'%s','%s','%s',NULL,1);" % (dt_create, dt_end, str_subject)
            else:
                dt_create = str(datetime.date.today())[0:10]
                str_subject = ln[2:len(ln)-1]
                sql = "insert into task values (NULL,'%s',NULL,'%s',NULL,0);" % (dt_create,str_subject)
            print sql
            c.execute(sql)
            conn.commit()
            print '----------------'
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "Programme parameter is not suitable."
        sys.exit(0)
    fp_org = sys.argv[1]
    fp_db = sys.argv[2]
    org2sqlite(fp_org,fp_db)
