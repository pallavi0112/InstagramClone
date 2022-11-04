
from django.contrib import messages
from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.decorators import login_required
from  .models import *
from django.db.models import Q

@login_required()
def Home(request):
    posts = POST.objects.filter(Q(profile__followers=request.user))
    story = Story.objects.filter(Q(profile__followers=request.user))
    profile = Profile.objects.get(user = request.user)
    profileImage = profile.profile_picture.url
    return render(request , "Instagram/home.html" , { 'posts' : posts , 'profileImage':profileImage , 'stories':story})

def SignUp(request):

    if request.method == "POST":
        username = request.POST['username']
        pswd = request.POST['password']
        profileImage = request.FILES['image']
        user = User.objects.create_user(username=username,password=pswd)
        profile = Profile.objects.create(user = user , profile_picture = profileImage)
        if profile:
            messages.success(request , 'Your Profile has been Created .. Please Login!!!!!!!')
            return redirect('login')
    return render(request , "Instagram/SignUp.html")

def Login(request):
    if request.method == "POST":
        username = request.POST['username']
        pswd = request.POST['password']
        user = authenticate(username = username , password = pswd)
        if user:
            login(request,user)
            return redirect('/')
    return render(request , "Instagram/Login.html")


def LogOut(request):
    logout(request)
    return redirect('login')


def profile(request, id=None):
    profile = Profile.objects.get(user = request.user)
    profileImage = profile.profile_picture.url
    if id is not None : 
        profile = Profile.objects.get(id=id)
        posts = POST.objects.filter(user=request.user)
        posts_num = posts.count()
    else : 
        profile = Profile.objects.get(user = request.user)
        posts = POST.objects.filter(user=request.user)
        posts_num = posts.count()
    return render(request , "Instagram/profile.html" , {'profile':profile , 'profile_of_user':True , 'posts':posts , 'posts_num':posts_num , 'profileImage':profileImage})


def Search(request):
    profile = Profile.objects.get(user = request.user)
    profileImage = profile.profile_picture.url
    search = request.GET['username']
    profiles = Profile.objects.filter(user__username__icontains = search)
    context = {
        'profiles' : profiles,
        'username' : search,
        'profileImage':profileImage

    }
    return render(request, 'Instagram/search.html' , context)

def Follow(request):
    id= request.GET.get('id')
    username= request.GET.get('username')
    profile = Profile.objects.get(id=id)
    login_profile = Profile.objects.get(user=request.user)
    if request.user in profile.followers.all():
        profile.followers.remove(request.user)
        login_profile.following.remove(profile.user)
    else : 
        profile.followers.add(request.user)
        login_profile.following.add(profile.user)

    return redirect(f'/search?username={username}')

def UploadPosts(request):
    profile = Profile.objects.get(user = request.user)
    profileImage = profile.profile_picture.url
    if request.method == "POST":
        post = request.FILES['post']
        address =request.POST.get('city')
        post_caption =request.POST.get('caption')
        profile = Profile.objects.get(user=request.user)
        posts = POST.objects.create( user=request.user , Image=post , post_address=address, caption=post_caption, profile=profile)
        if posts:
            messages.success( request , "post uploaded")
    return render(request , 'Instagram/uploadposts.html' , {'profileImage':profileImage})

def Like(request , id ):
    post = POST.objects.filter(id=id)
    is_like = False
    if request.user in post[0].likes.all():
        post[0].likes.remove(request.user)
    else:
        post[0].likes.add(request.user)
        is_like =True
    count = post[0].likes.all().count()
    return JsonResponse({'like':is_like,'count':count})

def UploadReels(request):
    profile = Profile.objects.get(user = request.user)
    profileImage = profile.profile_picture.url
    if request.method == "POST":
        reel = request.FILES['reel']
        profile = Profile.objects.get(user = request.user)
        reels = Reels.objects.create(reels=reel , profile=profile)
        if reels:
            messages.success(request , "Reels Uploaded")
    return render(request , "Instagram/uploadreels.html", {'profileImage':profileImage})

def reel(request):
    reels = Reels.objects.all()
    profile = Profile.objects.get(user = request.user)
    profileImage = profile.profile_picture.url
    return render(request , "Instagram/reels.html" , {"reels":reels , "profileImage":profileImage})

def UploadStory(request):
    profile = Profile.objects.get(user = request.user)
    profileImage = profile.profile_picture.url
    if request.method == "POST":
        story = request.FILES['story']
        profile = Profile.objects.get(user = request.user)
        uploadstory = Story.objects.create(story=story, profile=profile)
        if uploadstory:
            messages.success(request, "Story Uploaded")
    return render(request , "Instagram/UploadStory.html" , {'profileImage':profileImage})

def Delete(request):
    id = request.GET.get('id')
    profileId = request.GET.get('profileId')
    print(id)
    profile = Profile.objects.get(user=request.user)
    print(profile)
    profile2 = Profile.objects.get(id=profileId)
    print(profile2)
    post = POST.objects.filter(id=id)
    if profile.user == profile2.user:
        post.delete() 
    else :
        pass                  
    return redirect(f'/profile?id={profileId}')     
