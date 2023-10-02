from ironpdf import *

pdf = PdfDocument.FromFile(r"C:\Users\lenovo\Desktop\ملف ٣ جديد.pdf")
# Extract all pages to a folder as image files
pdf.RasterizeToImageFiles("out/images/*.png",DPI=96)