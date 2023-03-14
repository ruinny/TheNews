from xhtml2pdf import pisa
import pdfkit
# pdfkit.from_file('templates/今日分享 - 2023-02-21.html','templates/今日分享 - 2023-02-21.pdf')
config_pdf = pdfkit.configuration(
    wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')
pdfkit.from_file(
    'templates/今日分享 - 2023-02-21.html',
    output_path='templates/今日分享 - 2023-02-21.pdf',
    configuration=config_pdf)

# def convert_html_to_pdf(source_html, output_filename):
#     # open output file for writing (truncated binary)
#     result_file = open(output_filename, "w+b")
#
#     # convert HTML to PDF
#     pisa_status = pisa.CreatePDF(
#             source_html,                # the HTML to convert
#             dest=result_file)           # file handle to recieve result
#
#     # close output file
#     result_file.close()                 # close output file
#
#     # return False on success and True on errors
#     return pisa_status.err
#
# f = open('sendmails/今日分享 - 2023-02-21.html', 'r', encoding='utf-8')
# source_html = f.read()
#
# output_filename = "test.pdf"
#
# pisa.showLogging()
# convert_html_to_pdf(source_html, output_filename)
#
# f.close()

# pdf = pisa.CreatePDF(open('templates/今日分享 - 2023-02-21.html', 'rb'), open('templates/今日分享 - 2023-02-21.html.pdf', 'wb'))

# if not pdf.err:
# print("pdf is build")
