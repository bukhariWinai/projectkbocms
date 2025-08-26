import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class CustomCharacterPasswordValidator:
    def validate(self, password, user=None):
        if not re.findall('[A-Z]', password):
            raise ValidationError(_("รหัสผ่านต้องมีตัวพิมพ์ใหญ่อย่างน้อย 1 ตัว (A-Z)"))
        if not re.findall('[a-z]', password):
            raise ValidationError(_("รหัสผ่านต้องมีตัวพิมพ์เล็กอย่างน้อย 1 ตัว (a-z)"))
        if not re.findall('[0-9]', password):
            raise ValidationError(_("รหัสผ่านต้องมีตัวเลขอย่างน้อย 1 ตัว (0-9)"))
        if not re.findall('[^A-Za-z0-9]', password):
            raise ValidationError(_("รหัสผ่านต้องมีอักขระพิเศษอย่างน้อย 1 ตัว (!@#...)"))

    def get_help_text(self):
        return _(
            "รหัสผ่านต้องประกอบด้วยตัวพิมพ์ใหญ่ ตัวพิมพ์เล็ก ตัวเลข และอักขระพิเศษอย่างน้อยอย่างละ 1 ตัว"
        )
