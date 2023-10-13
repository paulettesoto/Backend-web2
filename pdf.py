from fpdf import FPDF
import os


page=FPDF()
page.add_page()
page.set_font('Arial','B',12)
page.cell(50,30,align='L',ln=1, link=page.image('logo.png',10,8,25))
page.cell(50,10,"Pregunta1",ln=2)
page.cell(50,10,"________________________________________________________",ln=3)
page.cell(50,10,"Pregunta2",ln=14)
page.cell(50,10,"________________________________________________________",ln=5)
page.output('Report.pdf', 'F')
os.startfile('Report.pdf', 'Open')
