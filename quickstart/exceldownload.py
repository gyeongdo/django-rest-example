from io import BytesIO
from openpyxl import Workbook
from rest_framework.renderers import BaseRenderer

class ExcelRenderer(BaseRenderer):
    """
    Excel Renderer
    """
    media_type = 'application/ms-excel'
    format = 'xlsx'
    level_sep = '.'

    def render(self, data, media_type=None, renderer_context=None):
        """
        Renders serialized *data* into Excel. For a dictionary:
        """
        try:
            if data is None:
               return False

            stream = BytesIO()
            wb = Workbook(write_only=True)
            ws = wb.create_sheet()

            print('data2 : ', data)

            if 'header' in data:
                headers = data['header']
                ws.append(headers)

            if 'rows' in data:
                for item in data['rows']:
                    ws.append([item.get(key, None) for key in headers])

            wb.save(stream)
            value = stream.getvalue()
            stream.close()

        except Exception as e:
            print(str(e))

        return value