from django.shortcuts import render, redirect
from .forms import NewUserForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from .models import Post, Comment, Like
from .api.serializers import PostSerializer, CommentSerializer, CommentPostSerializer, TaggedPostSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import filters
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes

# Create your views here.
def index(request):
    return render (request=request, template_name="blog/index.html")


def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("blog:index")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render (request=request, template_name="blog/register.html", context={"register_form":form})


def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("blog:index")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="blog/login.html", context={"login_form":form})


def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("blog:index")


class PostsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['author', 'safe']
    search_fields = ['title', 'body', 'author__username']
    
    def get_queryset(self):
        queryset = Post.objects.all().order_by('author')
        user_id = self.request.query_params.get('user')
        is_safe = self.request.query_params.get('safe')
        if user_id is not None:
            queryset = queryset.filter(author=user_id)
        if is_safe is not None:
            queryset = queryset.filter(safe=is_safe)
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
	
    @action(detail=False, methods=['get'], url_path=r'my-tags')
    def my_tags(self, request):
        user = request.user
        tagged_posts = Post.objects.filter(tagged_users=user)
        serializer = TaggedPostSerializer(tagged_posts, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'], url_path=r'like')
    def like(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        like, created = post.likes.get_or_create(user=request.user)
        if not created:
            return Response({'status': 'already liked'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'status': 'liked'})

    @action(detail=True, methods=['get'], url_path=r'unlike')
    def unlike(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        try:
            like = post.likes.get(user=request.user)
        except Like.DoesNotExist:
            return Response({'status': 'not liked'}, status=status.HTTP_400_BAD_REQUEST)
        like.delete()
        return Response({'status': 'unliked'})


class CommentsViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    def get_serializer_class(self):
        if self.action in ['retrieve', 'partial_update', 'list']:
            return CommentSerializer
        return CommentPostSerializer
    def perform_create(self, serializer):
        serializer.save()
    
    @action(detail=True, methods=['get'], url_path=r'like')
    def like(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        like, created = comment.likes.get_or_create(user=request.user)
        if not created:
            return Response({'status': 'already liked'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'status': 'liked'})

    @action(detail=True, methods=['get'], url_path=r'unlike')
    def unlike(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        try:
            like = comment.likes.get(user=request.user)
        except Like.DoesNotExist:
            return Response({'status': 'not liked'}, status=status.HTTP_400_BAD_REQUEST)
        like.delete()
        return Response({'status': 'unliked'})