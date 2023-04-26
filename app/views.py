#from django.shortcuts import render
#from django.views.generic import View
#from .models import Profile, Work, Experience, Education, Software, Technical

from django.shortcuts import render, redirect
from django.views.generic import View
from .forms import ContactForm
from .models import Profile, Work, Experience, Education, Software, Technical
from django.conf import settings
from django.core.mail import BadHeaderError, EmailMessage
from django.http import HttpResponse
import textwrap

# Create your views here.

class IndexView(View):
    """トップページのビュー

    トップページのビューを記載。
    Attribute:
    """

    def get(self, request, *args, **kwargs):
        """get関数

        すべてのプロフィールデータを取得。
        """

        profile_data = Profile.objects.all()
        if profile_data.exists():
            #idを降順に並び替え、最新のプロフィールデータを取得
            profile_data = profile_data.order_by('-id')[0]
        work_data = Work.objects.order_by('-id')
        #プロフィールデータをindex.htmlに渡す
        return render(request, 'app/index.html', {
            'profile_data':profile_data,
            'work_data':work_data
        })


class DetailView(View):
    """作品詳細ページのビュー

    作品詳細ページのビューを記載。
    Attributes:
    """
    def get(self, request, *args, **kwargs):
        """get関数

        作品データをを取得。
        """
        work_data = Work.objects.get(id=self.kwargs['pk'])
        return render(request, 'app/detail.html', {
            'work_data': work_data
        })

class AboutView(View):
    """プロフィールページのビュー

    プロフィールページのビューを記載。
    Attributes:
    """
    def get(self, request, *args, **kwargs):
        """get関数

        プロフィールデータを取得
        """
        profile_data = Profile.objects.all()
        if profile_data.exists():
            profile_data = profile_data.order_by('-id')[0]
            experience_data = Experience.objects.order_by('-id')
            education_data = Education.objects.order_by('-id')
            software_data = Software.objects.order_by('-id')
            technical_data = Technical.objects.order_by('-id')
            return render(request, 'app/about.html', {
                'profile_data': profile_data,
                'experience_data': experience_data,
                'education_data' :education_data,
                'software_data': software_data,
                'technical_data': technical_data,
            })


class ContactView(View):
    """お問い合わせページのビュー

    お問い合わせページのビューを記載。
    Attributes:
    """
    def get(self, request, *args, **kwargs):
        """get関数

        お問い合わせデータを取得
        ページ表示にコールされる
        """
        form = ContactForm(request.POST or None)
        return render(request, 'app/contact.html', {
            'form': form
        })


    def post(self, request, *args, **kwargs):
        """post関数

        お問い合わせデータをサーバに送信
        """
        form = ConatctForm(request.POST or None)

        #フォーム内容が正しいかを判断
        if forms.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            subject = 'お問い合わせありがとうございます。'
            contact = textwrap.dedent('''
                ※このメールはシステムからの自動返信です。

                {name} 様

                お問い合わせありがとうございます。
                以下の内容でお問い合わせを受付いたしました。
                内容を確認させていただき、ご返信させていただきますので、少々お待ちください。

                ---------------
                ◆お名前
                {name}

                ◆メールアドレス
                {email}

                ◆メッセージ
                {message}
                ---------------

                ※This email is an automatic reply from the system.

                Dear {name}

                Thank you for your inquiry.
                We have received inquiries with the above contents.
                We will check the contents and reply to you, so please be patient.
                ''').format(
                    name=name,
                    email=email,
                    message=message
                )
            to_list = [email]
            #自分のメールアドレスをBccに追加
            bcc_list = [settings.EMAIL_HOST_USER]

            try:
                message = EmailMessage(subject=subject, body=contact, to=to_list, bcc=bcc_list)
                #メールを送信
                message.send()
            except BadHeaderError:
                return HttpResponse('無効なヘッダが検出されました。')

            return redirect('index')

        return render(request, 'app/contact.html', {
            #フォーム画面に不備があった場合、空のフォーム画面を表示
            'form': form
    })