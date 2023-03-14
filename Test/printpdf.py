import os
from pyhtml2pdf import converter

path = os.path.abspath('../sendmails/今日分享 - 2023-02-16.html')
print(path)
converter.convert(f'file:///{path}', 'sample.pdf')