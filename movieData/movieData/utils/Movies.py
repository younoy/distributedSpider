import os
import io

class Movies():
    def movieNames(self):
        file_name = (os.path.expanduser('~') +
                     '/.surprise_data/ml-100k/ml-100k/u.item')
        rid_to_name = {}
        name_to_rid = {}
        rid_to_movie = {}
        movies = []
        with io.open(file_name, 'r', encoding='ISO-8859-1') as f:
            for line in f:
                line = line.split('|')
                rid_to_movie[line[0]] = line[1]
                line[1] = line[1].split('(')[0]
                rid_to_name[line[0]] = line[1]
                name_to_rid[line[1]] = line[0]
                movies.append(line[1])

        return movies, rid_to_name, name_to_rid, rid_to_movie


    def read_item_genre(self):
        genre_name = (os.path.expanduser('~') + '/.surprise_data/ml-100k/ml-100k/u.genre')
        item_name = (os.path.expanduser('~') + '/.surprise_data/ml-100k/ml-100k/u.item')
        name_to_genre = {}

        genres = []

        with io.open(genre_name, 'r', encoding='ISO-8859-1') as f:
            for line in f:
                if line != '\n':
                    line = line.split('|')
                    genres.append(line[0])

        with io.open(item_name, 'r', encoding='ISO-8859-1') as f:
            for line in f:
                movieName = line.split('|')[1]
                genresNum = line.split('|')[5:]
                count = 0
                genreName = []
                for i in genresNum:
                    if i == '1' or i == '1\n':
                        genreName.append(genres[count])
                    count = count + 1
                name_to_genre[movieName] = genreName

        return name_to_genre