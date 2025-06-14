from django.shortcuts import render, get_object_or_404
from .forms import CommentForm
from django.core.mail import mail_admins
from django.contrib import messages
from .models import Post, Comment, Video, VaultLink
from django.db import connection
print(connection.introspection.table_names())


def videos_view(request):
    videos = {
        'tech': Video.objects.filter(category='tech', is_active=True).order_by('-created_at').first(),
        'conspiracy': Video.objects.filter(category='conspiracy', is_active=True).order_by('-created_at').first(),
        'personal': Video.objects.filter(category='personal', is_active=True).order_by('-created_at').first(),
    }
    return render(request, 'blog/videos.html', {'videos': videos})
def about(request):
    return render(request, 'blog/about.html')

def videos(request):
    videos = {
        'tech': Video.objects.filter(category='tech', is_active=True).first(),
        'conspiracy': Video.objects.filter(category='conspiracy', is_active=True).first(),
        'personal': Video.objects.filter(category='personal', is_active=True).first(),
    }
    return render(request, 'blog/videos.html', {'videos': videos})

def conspiracy(request):
    links = VaultLink.objects.filter(is_active=True).order_by('-created_at')

    grouped_links = []
    for key, label in VaultLink.CATEGORY_CHOICES:
        cat_links = links.filter(category=key)
        grouped_links.append({
            'category': key,
            'label': label,
            'links': cat_links
        })

    return render(request, 'blog/conspiracy.html', {
        'grouped_links': grouped_links
    })

def tech(request):
    return render(request, 'blog/tech.html')

def portfolio(request):
    return render(request, 'blog/portfolio.html')

def contact(request):
    return render(request, 'blog/contact.html')

def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    # Only show approved comments
    comments = post.comments.filter(approved=True).order_by('-created_at')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post

            parent_id = request.POST.get('parent_id')
            if parent_id:
                try:
                    comment.parent = Comment.objects.get(id=parent_id)
                except Comment.DoesNotExist:
                    comment.parent = None

            comment.save()

            # Email + flash message
            mail_admins(
                subject='New Comment Submitted',
                message=f'New comment on "{post.title}" by {comment.name}:\n\n{comment.body}'
            )
            messages.info(request, "Your comment was submitted and is awaiting approval.")
            form = CommentForm()



    else:
        form = CommentForm()

    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form,

    })


