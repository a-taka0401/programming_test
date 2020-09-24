from django.db import models

class AiAnalysisLog(models.Model):
    """
    APIから吐き出されるAIが解析した画像のデータをログとして保存するテーブル
    """
    class Meta:
        db_table = 'ai_analysis_log'
        verbose_name_plural = 'AI解析ログ'

    image_path = models.CharField(
        verbose_name='image_path', max_length=255,
        default=None, blank=True, null=True
    )
    success = models.CharField(
        verbose_name='success', max_length=255,
        null=True, default=None
    )
    message = models.CharField(
        verbose_name='message', max_length=255,
        null=True, default=None
    )
    _class = models.IntegerField(
        db_column='class', verbose_name='class',
        null=True, default=None
    )
    confidence = models.DecimalField(
        verbose_name='confidence', max_digits=5,
        decimal_places=4, null=True, default=None
    )
    request_timestamp = models.PositiveIntegerField(
        verbose_name='request_timestamp',
        null=True, default=None
    )
    response_timestamp = models.PositiveIntegerField(
        verbose_name='request_timestamp',
        null=True, default=None
    )
