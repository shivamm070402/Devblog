from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Post, Category


def post_list(request):
    """Home page — list all published posts."""
    posts      = Post.objects.filter(status='published').select_related('author', 'category')
    categories = Category.objects.all()

    featured    = posts.first()
    recent_posts = list(posts[1:4])   # 3 cards
    feed_posts  = list(posts[4:])     # rest in list feed

    sd_cat        = Category.objects.filter(slug='system-design').first()
    sd_post_count = sd_cat.posts.filter(status='published').count() if sd_cat else 0

    context = {
        'featured':        featured,
        'recent_posts':    recent_posts,
        'feed_posts':      feed_posts,
        'categories':      categories,
        'total_posts':     posts.count(),
        'total_categories': categories.count(),
        'sd_post_count':   sd_post_count,
    }
    return render(request, 'blog/post_list.html', context)


def post_detail(request, slug):
    """Full blog post view."""
    post    = get_object_or_404(Post, slug=slug, status='published')
    related = Post.objects.filter(
        category=post.category, status='published'
    ).exclude(id=post.id)[:4]

    context = {
        'post':    post,
        'related': related,
    }
    return render(request, 'blog/post_detail.html', context)


def category_posts(request, slug):
    """Posts filtered by category."""
    category = get_object_or_404(Category, slug=slug)
    posts    = Post.objects.filter(
        category=category, status='published'
    ).select_related('author')
    context = {
        'category': category,
        'posts':    posts,
    }
    return render(request, 'blog/category_posts.html', context)


def search(request):
    """Full-text search across title + body."""
    query   = request.GET.get('q', '').strip()
    results = Post.objects.none()
    if query:
        results = Post.objects.filter(
            Q(title__icontains=query) | Q(body__icontains=query),
            status='published',
        ).select_related('author', 'category')
    context = {
        'query':   query,
        'results': results,
    }
    return render(request, 'blog/search.html', context)
