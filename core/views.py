from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, auth
from django.contrib import admin
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Movie, MovieList, CustomMovieList
from .forms import CustomMovieListForm
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

@login_required(login_url='login')
def index(request):
    popular_movies = Movie.objects.all()
    my_list = MovieList.objects.filter(owner_user=request.user, name="My List").first()
    my_list_movies = my_list.movies.all() if my_list else []
    featured_movie = popular_movies.last() if popular_movies.exists() else None
    custom_lists = CustomMovieList.objects.filter(owner_user=request.user)

    context = {
        'popular_movies': popular_movies,
        'my_list_movies': my_list_movies,
        'featured_movie': featured_movie,
        'custom_lists': custom_lists,
        'youtube_api_key': settings.YOUTUBE_API_KEY,
    }
    return render(request, 'index.html', context)



def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('login')

    return render(request, 'login.html')


def signup(request):
    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)
                return redirect('/')
        else:
            messages.info(request, 'Password Not Matching')
            return redirect('signup')
    else:
        return render(request, 'signup.html')


@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('login')


@login_required(login_url='login')
def movie(request, pk):
    movie_uuid = pk
    movie_details = Movie.objects.get(uu_id=movie_uuid)

    context = {
        'movie_details': movie_details
    }

    return render(request, 'movie.html', context)


@login_required(login_url='login')
def genre(request, pk):
    movie_genre = pk
    movies = Movie.objects.filter(genre=movie_genre)

    context = {
        'movies': movies,
        'movie_genre': movie_genre,
    }
    return render(request, 'genre.html', context)


@login_required(login_url='login')
def search(request):
    if request.method == 'POST':
        search_term = request.POST['search_term']
        movies = Movie.objects.filter(title__icontains=search_term)

        context = {
            'movies': movies,
            'search_term': search_term,
        }
        return render(request, 'search.html', context)
    else:
        return redirect('/')

@login_required(login_url='login')
def my_list_json(request):
    movie_list = MovieList.objects.filter(owner_user=request.user).first()
    user_movie_list = movie_list.movies.all() if movie_list else []

    movies = []
    for movie in user_movie_list:
        movies.append({
            'title': movie.title,
            'description': movie.description,
            'release_date': movie.release_date,
            'genre': movie.genre,
            'length': movie.length,
            'image_card_url': movie.image_card.url,
            'image_cover_url': movie.image_cover.url,
            'youtube_video_id': movie.youtube_video_id,
            'uu_id': str(movie.uu_id),  # Ensure UUID is serialized as string
        })

    return JsonResponse({'movies': movies})

@login_required(login_url='login')
def my_list(request):
    movie_list = MovieList.objects.filter(owner_user=request.user).first()
    user_movie_list = movie_list.movies.all() if movie_list else []
    custom_lists = CustomMovieList.objects.filter(owner_user=request.user)

    context = {
        'movies': user_movie_list,
        'custom_lists': custom_lists,
    }
    return render(request, 'my_list.html', context)


@login_required(login_url='login')
@csrf_exempt
def add_to_list(request):
    if request.method == 'POST':
        movie_id = request.POST.get('movie_id')
        movie = get_object_or_404(Movie, uu_id=movie_id)

        try:
            movie_list, created = MovieList.objects.get_or_create(owner_user=request.user, name="My List")
        except MovieList.MultipleObjectsReturned:
            movie_list = MovieList.objects.filter(owner_user=request.user, name="My List").first()

        if movie in movie_list.movies.all():
            response_data = {'status': 'info', 'message': 'Movie already in list'}
        else:
            movie_list.movies.add(movie)
            response_data = {'status': 'success', 'message': 'Added ✓'}

        return JsonResponse(response_data)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

@login_required(login_url='login')
@csrf_exempt
def remove_from_list(request):
    if request.method == 'POST':
        movie_id = request.POST.get('movie_id')
        movie = get_object_or_404(Movie, uu_id=movie_id)
        movie_list = get_object_or_404(MovieList, owner_user=request.user, name="My List")

        if movie in movie_list.movies.all():
            movie_list.movies.remove(movie)
            response_data = {'status': 'success', 'message': 'Removed ✓'}
        else:
            response_data = {'status': 'info', 'message': 'Movie not in list'}

        print(response_data)  # Debug statement
        return JsonResponse(response_data)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

@login_required(login_url='login')
def custom_list_json(request, list_id):
    custom_list = get_object_or_404(CustomMovieList, id=list_id, owner_user=request.user)
    movies = custom_list.movies.all()

    movie_list = []
    for movie in movies:
        movie_list.append({
            'title': movie.title,
            'description': movie.description,
            'release_date': movie.release_date,
            'genre': movie.genre,
            'length': movie.length,
            'image_card_url': movie.image_card.url,
            'image_cover_url': movie.image_cover.url,
            'youtube_video_id': movie.youtube_video_id,
            'uu_id': str(movie.uu_id),
        })

    return JsonResponse({'movies': movie_list})


@login_required(login_url='login')
def custom_lists(request):
    custom_lists = CustomMovieList.objects.filter(owner_user=request.user)


    context = {
        'custom_lists': custom_lists
    }
    return render(request, 'custom_lists.html', context)


@login_required(login_url='login')
@csrf_exempt
def add_to_custom_list(request):
    if request.method == 'POST':
        movie_id = request.POST.get('movie_id')
        list_id = request.POST.get('list_id')
        movie = get_object_or_404(Movie, uu_id=movie_id)
        custom_list = get_object_or_404(CustomMovieList, id=list_id, owner_user=request.user)

        if movie in custom_list.movies.all():
            response_data = {'status': 'info', 'message': 'Movie already in list'}
        else:
            custom_list.movies.add(movie)
            response_data = {'status': 'success', 'message': 'Added ✓'}

        return JsonResponse(response_data)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

@login_required(login_url='login')
@csrf_exempt
def remove_from_custom_list(request):
    if request.method == 'POST':
        movie_id = request.POST.get('movie_id')
        list_id = request.POST.get('list_id')
        movie = get_object_or_404(Movie, uu_id=movie_id)
        custom_list = get_object_or_404(CustomMovieList, id=list_id, owner_user=request.user)

        if movie in custom_list.movies.all():
            custom_list.movies.remove(movie)
            response_data = {'status': 'success', 'message': 'Removed ✓'}
        else:
            response_data = {'status': 'info', 'message': 'Movie not in list'}

        return JsonResponse(response_data)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

@login_required(login_url='login')
def create_custom_list(request):
    if request.method == 'POST':
        form = CustomMovieListForm(request.POST)
        if form.is_valid():
            custom_list = form.save(commit=False)
            custom_list.owner_user = request.user
            custom_list.save()
            return redirect('my-list')
    else:
        form = CustomMovieListForm()
    return render(request, 'create_custom_list.html', {'form': form})

@login_required(login_url='login')
def update_custom_list(request, list_id):
    custom_list = get_object_or_404(CustomMovieList, id=list_id, owner_user=request.user)
    if request.method == 'POST':
        form = CustomMovieListForm(request.POST, instance=custom_list)
        if form.is_valid():
            form.save()
            return redirect('my-list')
    else:
        form = CustomMovieListForm(instance=custom_list)
    return render(request, 'update_custom_list.html', {'form': form, 'list_id': list_id})

@login_required(login_url='login')
def delete_custom_list(request, list_id):
    custom_list = get_object_or_404(CustomMovieList, id=list_id, owner_user=request.user)
    if request.method == 'POST':
        custom_list.delete()
        return redirect('my-list')
    return render(request, 'delete_custom_list.html', {'custom_list': custom_list})
