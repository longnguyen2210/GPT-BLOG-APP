from django.shortcuts import render, redirect
from .models import Post
from django.contrib.auth.decorators import login_required
from . import forms
from django.http import JsonResponse
from openai import OpenAI


api_key = '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'

client = OpenAI(api_key = api_key)
  

# Create your views here.
def posts_list(request):
    posts = Post.objects.all().order_by('-date')
    return render(request, 'posts/posts_list.html',{ 'posts':posts})

def post_page(request,slug):
    post = Post.objects.get(slug=slug)
    return render(request, 'posts/post_page.html',{ 'post':post})

@login_required(login_url = "/users/login")
def post_new(request):
    if request.method == "POST":
        form = forms.CreatePost(request.POST, request.FILES)
        if form.is_valid():
            newpost = form.save(commit=False)
            newpost.author = request.user
            newpost.save()
            return redirect('posts:list')
    else:
        form = forms.CreatePost()
    return render(request, 'posts/post_new.html', {'form':form})

def get_completion(prompt):
    print(prompt)

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": prompt
            }
        ]
    )



    response = completion.choices[0].message
    print(response)
    return response

def query_view(request):
    if request.method == 'POST':
        prompt = request.POST.get('prompt')
        response = get_completion(prompt)
        return JsonResponse({'response': response})
    return render(request, 'posts/post_new.html')
