import omdb
from movie.models import Movie
from threading import Thread
def get_movie_info (start_id, end_id):
    sub_query = Movie.objects.filter(movie_id__gte=start_id).filter(movie_id__lt=end_id)
    for q in sub_query:
        title = q.name
        api_result = omdb.title(title)
        if api_result:
            q.plot = api_result['plot']
            q.duration = api_result['runtime']
            q.release_date = api_result['released']
            q.rating = api_result['imdb_rating']
            q.poster = api_result['poster']
            q.cast_crew = api_result['actors']
            q.genre = api_result['genre']
            q.save()
        else:
            print ('cannot retrieve data of movie  ' + title)


total_count = Movie.objects.all().count()
# total_count = 20
thread_work = total_count / 5
start_id = 1
threads = []
for i in range(5):

    if i == 4:
        t = Thread(target=get_movie_info, args=(start_id, total_count + 1))
        threads.append(t)
    else:
        t = Thread(target=get_movie_info, args=(start_id, start_id + thread_work))
        start_id += thread_work
        threads.append(t)

for t in threads:
    t.start()

for t in threads:
    t.join()
