from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer

from .serializers import PostSerializer, PostRatingSerializer
from .models import Post, PostRating
from .permissions import IsOwnerOrReadOnly


class PostViewSet(ModelViewSet):

    queryset = Post.objects.all().order_by('-pub_date')
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]

    def list(self, request, *args, **kwargs):
        response_data = {
            'feed': self.get_queryset(),
            'serializer': PostSerializer(),
        }
        return Response(data=response_data, template_name='feed.html')

    def create(self, request, *args, **kwargs):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return redirect(to='feed:post-list')

        return JsonResponse(serializer.errors)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        post = self.get_object()
        response_data = {
            'post': post,
            'serializer': PostSerializer(post)
        }
        return Response(data=response_data,  template_name='post_detail.html')

    def update(self, request, *args, **kwargs):
        super(PostViewSet, self).update(request, *args, **kwargs)

        return HttpResponse(status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        super(PostViewSet, self).destroy(request, *args, **kwargs)

        return HttpResponse(status=status.HTTP_204_NO_CONTENT)


class PostRatingProcess(ModelViewSet):

    queryset = PostRating.objects.all()
    serializer_class = PostRatingSerializer
    permission_classes = [IsAuthenticated]


@login_required(login_url='rest_framework:login')
def rate_post(request):
    user = request.user
    pk = request.GET.get('pk')
    user_rate = request.GET.get('user_rate')
    post = get_object_or_404(Post, pk=pk)
    post_rate, _ = PostRating.objects.get_or_create(by=user, post=post)

    toggle_rate(post_rate, bool(int(user_rate)))
    post_rate.save()

    return JsonResponse({
        'likes': post.get_likes(),
        'dislikes': post.get_dislikes()
    })


def toggle_rate(post_rating: PostRating, user_rate: bool):
    if post_rating.liked is None:
        post_rating.liked = user_rate
    else:
        post_rating.liked = user_rate if post_rating.liked != user_rate else None
