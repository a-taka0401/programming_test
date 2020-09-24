import datetime
import random
import requests
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import View, TemplateView, ListView
from .forms import ImagePathForm
from .models import AiAnalysisLog


class IndexView(TemplateView):
    """
    トップページの表示(モックと実際のシステムへのリンクを表示)
    """
    template_name = './app/index.html'

class MockView(View):
    """
    モック用Viewランダムで資料でいただいたAPIのレスポンスと同じものを出力する。
    formの表示とAPIからの取得データをDBへ保存する機能
    """
    def get(self, request):
        """解析したい画像のpathを入力するフォームを表示
        Returns
        -------
        context : dict
        """
        form = ImagePathForm
        template = './app/mock.html'
        context = {
            'form': form,
        }

        return render(request, template, context)

    def post(self, request):
        """Ajaxで得たpathに関係なくランダムで生成した配列をDBへ保存する。
        Parameters
        ----------
        image_path : str

        Returns
        -------
        response : Json
        """
        form = ImagePathForm(request.POST)
        if form.is_valid():
            try:
                request_timestamp = int(datetime.datetime.today().timestamp())
                if random.getrandbits(1):
                    response = {
                        "success": True,
                        "message": "success",
                        "estimated_data": {
                            "class": 3,
                            "confidence": 0.8683
                        }
                    }
                else:
                    response = {
                        "success": False,
                        "message": "Error:E50012",
                        "estimated_data": {}
                    }
                response_timestamp = int(datetime.datetime.today().timestamp())
                result = response
                if result['success']:
                    _class = result['estimated_data']['class']
                    confidence = result['estimated_data']['confidence']
                    message = '保存が完了しました。'
                else:
                    _class = None
                    confidence = None
                    message = '解析に失敗しました。<br>' + result['message']

                AiAnalysisLog(
                    image_path=request.POST.get('image_path'),
                    success=result['success'],
                    message=result['message'],
                    _class=_class,
                    confidence=confidence,
                    request_timestamp=request_timestamp,
                    response_timestamp=response_timestamp,
                ).save()
            except Exception as error:
                message = 'Error: ' + error
        else:
            message = '入力されたパスに異常があります。'
        response = JsonResponse({
            'message': message
        })

        return response


class PostAiView(View):
    """
    http://example.com/へpostするview
    formの表示とAPIからの取得データをDBへ保存する機能
    """
    def get(self, request):
        """解析したい画像のpathを入力するフォームを表示
        Returns
        -------
        context : dict
        """
        form = ImagePathForm
        template = './app/post_api.html'
        context = {
            'form': form,
        }

        return render(request, template, context)

    def post(self, request):
        """Ajaxで得たpathを使ってAPIを叩きその結果をDBへ保存する。
        Parameters
        ----------
        image_path : str

        Returns
        -------
        response : Json
        """
        form = ImagePathForm(request.POST)
        if form.is_valid():
            try:
                url = "http://exsample.com/"
                data = {
                    'image_path': str(request.POST.get('image_path')),
                }
                request_timestamp = int(datetime.datetime.today().timestamp())
                response = requests.post(url, params=data)
                response_timestamp = int(datetime.datetime.today().timestamp())
                # apiが存在せずexample.comがhtml形式なためcontext-typeで分岐せさています。
                if 'json' in response.headers.get('content-type'):
                    result = response.json()

                    if result['success']:
                        _class = result['estimated_data']['class']
                        confidence = result['estimated_data']['confidence']
                        message = '保存が完了しました。'
                    else:
                        _class = None
                        confidence = None
                        message = '解析に失敗しました。<br>' + result['message']

                    AiAnalysisLog(
                        image_path=str(request.POST.get('image_path')),
                        success=result['success'],
                        message=result['message'],
                        _class=_class,
                        confidence=confidence,
                        request_timestamp=request_timestamp,
                        response_timestamp=response_timestamp,
                    ).save()
                else:
                    message = 'apiのcontent-typeが変更になったようです。<br>URL:' + url
            except Exception as error:
                message = 'Error: ' + error
        else:
            message = '入力されたパスに異常があります。'

        response = JsonResponse({
            'message': message
        })

        return response

class AiAnalysisLogList(ListView):
    """
    ai_analysis_logテーブルを一覧で表示
    """
    model = AiAnalysisLog
    paginate_by = 10
