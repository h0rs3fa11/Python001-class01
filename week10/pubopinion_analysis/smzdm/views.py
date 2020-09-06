from django.shortcuts import render
from .models import Goods
from .models import OriginComments
from .models import AnalysisComments
from django.db.models import Avg
from datetime import datetime
from django.http import HttpResponse


# Create your views here.
def index(request):
    # 商品id
    goods = Goods.objects.all()
    # 商品名称
    good_name = Goods.objects.values('good_name')
    # 商品总数
    goods_count = Goods.objects.all().count()
    # 评论总数
    comment_count = OriginComments.objects.all().count()
    return render(request, 'index.html', locals())


def good_info(request, id):
    queryset = AnalysisComments.objects.values('content')
    conditions = {'good_id__exact': id}
    comments_count = queryset.filter(**conditions).count()

    good_name = Goods.objects.values('good_name').filter(**conditions)[0]['good_name']

    queryset = AnalysisComments.objects.values('sentiments')
    sent_avg = f"{queryset.filter(**conditions).aggregate(Avg('sentiments'))['sentiments__avg']:0.2}"

    queryset = AnalysisComments.objects.values('sentiments')
    sent_cond = {'sentiments__lt': 0.5}
    minus = queryset.filter(**conditions).filter(**sent_cond).count()

    sent_cond = {'sentiments__gte': 0.5}
    plus = queryset.filter(**conditions).filter(**sent_cond).count()

    queryset = AnalysisComments.objects.all()
    analysis_comment = queryset.filter(**conditions)

    return render(request, 'good_info.html', locals())


def search(request):
    query = request.GET.get('q')
    try:
        search_date = datetime.strptime(query, "%Y-%m-%d")
        query_date = search_date.strftime("%Y-%m-%d")
        goods_result = None
        comment_result = OriginComments.objects.filter(time__gte=query_date)
    except ValueError:
        goods_result = Goods.objects.filter(good_name__icontains=query)
        comment_result = OriginComments.objects.filter(content__icontains=query)
    return render(request, 'comment_search_result.html',
                  {'error_msg': 0, 'result': {"goods": goods_result, "comments": comment_result}})
