from movie.models import Movie

f = open("get_movie_info.log")

begin_index = len('cannot retrieve data of movie  ')
for line in f.readlines():
    title = line[begin_index:].replace('\n', '')
    movies = Movie.objects.filter(name=title)
    for q in movies:
        if q.rating == None:
            q.delete()

f.close()
