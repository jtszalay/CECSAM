import pdflabels

pdf = pdflabels.PDFLabel('Avery-5160')

pdf.add_page()
pdf.code39("C334030", 1, 1)

import sys
sys.stdout.write(pdf.output(name="" ,dest="S"))
