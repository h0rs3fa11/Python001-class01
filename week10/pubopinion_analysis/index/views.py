from django.shortcuts import render
from django.http import HttpResponse
from .models import Goods
from .models import OriginComments
from .models import AnalysisComments


# Create your views here.
def index(request):
    # 商品id
    goods = Goods.objects.values('good_id')
    # 商品名称
    good_name = Goods.objects.values('good_name')
    # 商品总数
    goods_count = Goods.objects.all().count()
    # 评论总数
    comment_count = OriginComments.objects.all().count()
    analysis_comment = AnalysisComments.objects.all().select_related('good')

    return render(request, 'index.html', locals())
