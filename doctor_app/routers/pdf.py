from fpdf import FPDF
import os
from mysql.connector import Error
from ..connection import connection, cursor
from fastapi import APIRouter

#from ..dependecies import get_token_header


router = APIRouter(
    prefix="/Report",
    tags=["Reporte"],
    #dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}})


#@router.post("/pdf")
#def docs(idDoctor:str):
    #page = FPDF()
    #page.add_page()
    #page.set_font('Arial','B',12)
    #page.cell(50,30,align='L', ln=1, link = page.image('logo.png', 10,8,25))

    #page.cell(50,10,"Pregunta1", ln=2)
    #page.cell(50,10,"________________________________________________________",ln=3)
    #page.cell(50,10,"Pregunta2", ln=14)
    #page.cell(50,10,"________________________________________________________",ln=5)
    #page.output('Report.pdf', 'F')
    #os.startfile('Report.pdf', 'Open')

@router.post("/pdf")
def docs(idDoctor: str):
    connection()
    try:
        query = ("select Pregunta from historiaclinica where idDoctor=" + idDoctor + ";")
        cursor.execute(query)
        record = cursor.fetchall()
        page = FPDF()
        page.add_page()
        page.set_font('Arial', 'B', 12)
        c = 1
        page.cell(50, 30, align='L', ln=c, link=page.image('logo.png', 10, 8, 25))
        for p in record:
            c += 1 #
            s = str(p).replace("(","").replace(")","").replace(",","").replace("'","")

            print(s)
            page.cell(50, 10, s, ln=c)
            c += 1
            page.cell(50, 10, "_________________________________________________________________", ln=c)
        page.output('Report.pdf', 'F')
        os.startfile('Report.pdf', 'Open')
        return record
    except Error as e:
        return {"Error: ", e}
