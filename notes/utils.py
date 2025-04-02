from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from django.conf import settings
import os

def font_patch():
    # 注册中文字体
    font_path = os.path.join(settings.STATIC_ROOT, 'font', 'msyh.ttf')  # 中文字体文件路径
    print(font_path)
    if not os.path.exists(font_path):
        raise FileNotFoundError(f"字体文件不存在: {font_path}")
    pdfmetrics.registerFont(TTFont('yh', font_path))
    # 设置默认字体
    from xhtml2pdf.default import DEFAULT_FONT
    DEFAULT_FONT['helvetica'] = 'yh'