from django import forms
from .models import AiAnalysisLog

class ImagePathForm(forms.ModelForm):
    """MockViewとPostAiViewで利用しているpathを入力するform
    Fields
    ------
        image_path : CharField
    """
    class Meta:
        model = AiAnalysisLog
        fields = ('image_path',)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image_path'].required = True
