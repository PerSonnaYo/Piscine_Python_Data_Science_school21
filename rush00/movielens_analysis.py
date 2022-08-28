import os
import sys
import re
from collections import Counter, defaultdict
from collections import OrderedDict
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import pytest

# print("reload success in %s" % datetime.datetime.now())

class Movies():

    def __init__(self, path_to_the_file):
        self.filename = path_to_the_file
        self.sep = ","
        self.genres = {"Action", "Adventure", "Animation", "Children", "Comedy",'Crime', 
"Documentary",
"Drama",
"Fantasy",
"Film-Noir",
"Horror",
"Musical",
"Mystery",
"Romance",
"Sci-Fi",
"Thriller",
"War",
"Western",
"(no genres listed)"}
        
    def read_csv(self):
        with open(self.filename, 'r') as csv_file:
            self.res = {}
            i = 1
            for line in csv_file:
                if i == 1:
                    self.title = line.split(self.sep)
                    i+=1
                    continue
                id = re.findall('\d+', line)[0]
                l = []
                o = 1
                for val in self.genres:
                    if val in line:
                        l.append(val)


                buf = line.split(",")
                buf = buf[1:-1]
                buf1 = ""
                for val in buf:
                    buf1 += val
                    
                lst =[]
                # year = buf[1].split(" (")
                data = buf1.split("(")
                dd = set()
                if "(" in buf1:
                    # print(buf1)
                    name = ''
                    for val in data[:-1]:
                        name += val
                    year = data[-1].split(")")[0]

                else:
                    name = ''
                    for val in data:
                        name += val
                    year = "without year"
                self.res[id] = (name, year, l)
                # print(self.res)
        return self.res

    def dist_by_release(self):
        c = Counter()
        for i in self.res:
            c[self.res[i][1]] += 1
        res = OrderedDict(c)
        release_years = OrderedDict(sorted(res.items(), key=lambda x: x[-1], reverse=True))
        return (release_years)
    
    def dist_by_genres(self):
        c = Counter()
        for i in self.res:
            for j in range(0, len(self.res[i][2])):
                c[self.res[i][2][j]] += 1
        genres = dict(sorted(c.items(), key=lambda x: x[-1], reverse=True))
        return (genres)
    
    def most_genres(self, n):
        c = Counter()
        for i in self.res:
            c[self.res[i][0]] = len(self.res[i][2])
        movies = dict(sorted(c.most_common(n), key=lambda x: x[-1], reverse=True))
        return movies

class Tags:
    """
    Analyzing data from tags.csv
    """
    def __init__(self, path_to_the_file):
       self.t = 0
       self.filename = path_to_the_file
       self.sep = ','

    def read_csv(self):
        self.lst=[]
        with open(self.filename, 'r') as csv_file:
            self.res = {}
            i = 1
            for line in csv_file:
                if i == 1:
                    self.title = line.split(self.sep)
                    i+=1
                    continue
                
                buf = line.split(",")
                self.lst.append(buf)
        # print(self.lst)

    def most_words(self, n):
        t = set()
        for val in self.lst:
            t.add(val[2])
        d = Counter()
        for i in t:
            d[i] = len(re.findall('\w+', i))
        big_tags = dict(sorted(d.most_common(n), key=lambda x: x[-1], reverse=True))
        return (big_tags)

    def longest(self, n):
        t = set()
        for val in self.lst:
            t.add(val[2])

        d = Counter()
        for i in t:
            d[i] = len(i)
        most = d.most_common(n)
        big_tags = []
        for val in most:
            big_tags.append(val[0])
        return (big_tags)
    
    def most_words_and_longest(self, n):
        m_w = set(self.most_words(n))
        long = set(self.longest(n))
        big_tags = set(m_w & long)
        # print(big_tags)
        return (list(big_tags))
    
    def most_popular(self, n):
        c = Counter()
        for i in range(0, len(self.lst)):
            c[self.lst[i][2]] +=1
        popular_tags = dict(sorted(c.most_common(n), key=lambda x: x[-1], reverse=True))
        # print(popular_tags)
        return (popular_tags)

    def tags_with(self, word):
        l = []
        for i in range(0, len(self.lst)):
            if re.search(word, self.lst[i][2]):
                l.append(self.lst[i][2])
        tags_with_word = set(l)
        tags_with_word = list(sorted(l))
        return (tags_with_word)

class Links:
    """
    Analyzing data from links.csv
    """
    def __init__(self, path_to_the_file):
        self.t = 0
        self.filename = path_to_the_file
        self.sep = ','

    def read_csv(self):
        self.lst=[]
        with open(self.filename, 'r') as csv_file:
            self.res = {}
            i = 1
            for line in csv_file:
                if i == 1:
                    self.title = line.split(self.sep)
                    i+=1
                    continue
                buf = line.split(",")
                self.lst.append(buf)
                self.res[buf[0]] = buf[1]
        # print(self.lst)
     
    def parse_director(self, ib, html_soup):
        director = html_soup.find('a', class_="ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link").text
        return director

    def parse_budget(self, ib, html_soup):
        budget = html_soup.find('div', attrs={"data-testid":"title-boxoffice-section"}).div.text
        budget = budget.split("(")[0].strip(" ")
        return budget

    def parse_gross(self, ib, html_soup):
        gross = html_soup.find_all('li', class_="ipc-metadata-list__item sc-3c7ce701-2 eYXppQ")
        for val in gross:
            # print (val.text)
            a = val.select_one('span.ipc-metadata-list-item__label')
            if a is not None:
                if 'Gross worldwide' in a.text:
                    gross = val.select_one('span.ipc-metadata-list-item__list-content-item').text
        return (gross)

    def parse_runtime(self, ib, html_soup):
        Runtime = html_soup.find_all('li', class_="ipc-metadata-list__item")
        for val in Runtime:
            # print (val.text)
            a = val.select_one('span.ipc-metadata-list-item__label')
            if a is not None:
                if 'Runtime' in a.text:
                    run_time = val.select_one('div.ipc-metadata-list-item__content-container').text
                    
        return (run_time)

    def get_imdb(self, list_of_movies,list_of_fields):
        d = {}
        for v in list_of_movies:
            ib = self.res[v]
            v = int(v)
            imdb_info = []
            try:
                url = f'https://www.imdb.com/title/tt{ib}/'
            except:
                raise ValueError("404")
            response = requests.get(url)
            html_soup = BeautifulSoup(response.text, 'html.parser')
            for val in list_of_fields:
                if val == 'movieId':
                    imdb_info.append(v)
                if val == 'imdbId':
                    imdb_info.append(ib)
                if val == 'Director':
                    imdb_info.append(self.parse_director(ib, html_soup))
                if val == 'Budget':
                    imdb_info.append(self.parse_budget(ib, html_soup))
                if val == 'Cumulative Worldwide Gross':
                    imdb_info.append(self.parse_gross(ib, html_soup))
                if val == 'Runtime':
                    imdb_info.append(self.parse_runtime(ib, html_soup))
            d[v] = imdb_info
        c = dict(sorted(d.items(), key=lambda x: (x[0], x[1]), reverse=True))
        print(c)
        imdb_info = []
        for i in c:
            imdb_info.append(c[i])
        
        return imdb_info

    def top_directors(self, n):
        c = Counter()
        for val in self.res:
            ib = self.res[val]
            try:
                url = f'https://www.imdb.com/title/tt{ib}/'
            except:
                raise ValueError("404")
            response = requests.get(url)
            html_soup = BeautifulSoup(response.text, 'html.parser')
            dir = self.parse_director(ib, html_soup)
            c[dir] = +1
            # print(dir)
        # print(c.most_common(n))
        directors = dict(sorted(c.most_common(n), key=lambda x: x[-1], reverse=True))
        return directors
    
    def most_expensive(self, n):
        mov = Movies("movies.csv").read_csv()
        # print(mov)
        c = Counter()
        for id in mov:
            ib = self.res[id]
            try:
                url = f'https://www.imdb.com/title/tt{ib}/'
            except:
                raise ValueError("404")
            response = requests.get(url)
            html_soup = BeautifulSoup(response.text, 'html.parser')
            dir = self.parse_budget(ib, html_soup)
            c[mov[id][0]] = dir
            # print(c)
        # print(c.most_common(n))
        budgets = dict(sorted(c.most_common(n), key=lambda x: x[-1], reverse=True))
        return budgets

    def most_profitable(self, n):
        mov = Movies("movies.csv").read_csv()
        # print(mov)
        c = Counter()
        for id in mov:
            ib = self.res[id]
            try:
                url = f'https://www.imdb.com/title/tt{ib}/'
            except:
                raise ValueError("404")
            response = requests.get(url)
            html_soup = BeautifulSoup(response.text, 'html.parser')
            dir = self.parse_budget(ib, html_soup)
            gros = self.parse_gross(ib, html_soup)
            dir = re.findall(r'\d+', dir)
            buf = ''.join(dir)
            bud = int(buf)
            gros = re.findall(r'\d+', gros)
            buf = ''.join(gros)
            gr = int(buf)
            c[mov[id][0]] = gr - bud
            # print(gr, bud)
            # print(gr - bud)
        # print(c.most_common(n))
        profits = dict(sorted(c.most_common(n), key=lambda x: x[-1], reverse=True))
        return profits

# class Users:

class Ratings:
    """
    Analyzing data from ratings.csv
    """
    def __init__(self, path_to_the_file):
        """
        Put here any fields that you think you will need.
        """
        self.filename = path_to_the_file
        # self.sep = ','
        self.filename_movie = "movies.csv"
        self.res = {}
        self.users = {}

    def read_csv(self):
        self.lst=[]
        with open(self.filename, 'r') as csv_file:
            self.res = {}
            self.users = {}
            i = 1
            for line in csv_file:
                if i == 1:
                    self.title = line.split(",")
                    i+=1
                    continue
                buf = line.split(",")
                self.lst.append(buf)
                if buf[1] not in self.res:
                    self.res[buf[1]] = []
                self.res[buf[1]].append(float(buf[2]))
                if buf[0] not in self.users:
                    self.users[buf[0]] = []
                self.users[buf[0]].append(float(buf[2]))
        # print(self.lst)
        return self.lst
        # print(self.lst)
    
    def get_movies(self):
        rating = Ratings.Movies(self, self.filename_movie)
        return rating
        # print(rating.dist_by_year())
    
    def get_users(self):
        rating = Ratings.Users(self, self.filename_movie)
        return rating
        # print(rating.dist_by_year())

    class Movies(Movies):
        def __init__(self, rating, path_to_the_file):
            # super().__init__(path_to_the_file)
            self.rating = rating
            self.filename = path_to_the_file
            self.sep = ','
            self.genres = {"Action", "Adventure", "Animation", "Children", "Comedy",'Crime', 
                "Documentary",
                "Drama",
                "Fantasy",
                "Film-Noir",
                "Horror",
                "Musical",
                "Mystery",
                "Romance",
                "Sci-Fi",
                "Thriller",
                "War",
                "Western",
                "(no genres listed)"}
            
        def dist_by_year(self):
            ratings_by_year = Counter()
            for film_info in self.rating.lst:
                ratings_by_year[datetime.fromtimestamp(int(film_info[3])).year] += 1
            ratings_by_year = dict(sorted(ratings_by_year.items(), key=lambda x: (x[0], x[1]), reverse=False))
            return ratings_by_year
        
        def dist_by_rating(self):
            ratings_distribution = Counter()
            for film_info in self.rating.lst:
                ratings_distribution[film_info[2]] += 1
            ratings_distribution = dict(sorted(ratings_distribution.items(), key=lambda x: (x[0], x[1]), reverse=False))
            return ratings_distribution

        def top_by_num_of_ratings(self, n):
            top_movies = Counter()
            id_name = {}
            c = self.read_csv()
            for film_info in c:
                id_name[film_info] = c[film_info][0]
            # print(id_name)
            for film_info in self.rating.lst:
                # print(film_info)/
                top_movies[id_name[film_info[1]]] += 1
            top_movies = dict(sorted(top_movies.most_common(n), key=lambda x: x[-1], reverse=True))
            return top_movies
        
        def variance(self, data): 
            n = len(data) 
            # Mean of the data 
            mean = sum(data) / n 
            # Square deviations 
            deviations = [(x - mean) ** 2 for x in data] 
            # Variance 
            variance = sum(deviations) / n 
            return variance 

        def my_median(self, sample):
            n = len(sample)
            index = n // 2
           # Sample with an odd number of observations
            if n % 2:
                return sorted(sample)[index]
        # Sample with an even number of observations
            return (sum(sorted(sample)[index - 1:index + 1]) / 2)

        def my_mean(self,sample):
            return sum(sample) / len(sample)

        def top_by_ratings(self, n, metric):
            id_name = {}
            c = self.read_csv()
            for film_info in c:
                id_name[film_info] = c[film_info][0]
            id_rat = {}
            r = self.rating.read_csv()
            for i in r:
                id_rat[i[1]] = i[2]
            # print(self.dist_by_rating)

            # print(id_rat, id_name)
            new = Counter()
            # print(id_name)
            if (metric == 'mediana'):
                for val in id_name:
                    if val in self.rating.res:
                        med = round(self.my_median(self.rating.res[val]),2)
                        new[id_name[val]] = med
                        # print(round(med,2))
            elif (metric == 'average'):
                for val in id_name:
                    if val in self.rating.res:
                        med = round(self.my_mean(self.rating.res[val]),2)
                        new[id_name[val]] = med
                        # print(round(med,2))

            top_movies = dict(sorted(new.most_common(n), key=lambda x: x[-1], reverse=True))
            return top_movies

        def top_controversial(self, n):
            id_name = {}
            c = self.read_csv()
            for film_info in c:
                id_name[film_info] = c[film_info][0]
            id_rat = {}
            r = self.rating.read_csv()
            for i in r:
                id_rat[i[1]] = i[2]
            # print(self.dist_by_rating)

            # print(id_rat, id_name)
            new = Counter()
            # print(id_name)
        
            for val in id_name:
                if val in self.rating.res:
                    med = round(self.variance(self.rating.res[val]),2)
                    new[id_name[val]] = med
                    # print(round(med,2))

            top_movies = dict(sorted(new.most_common(n), key=lambda x: x[-1], reverse=True))
            return top_movies
        
    class Users(Movies):
        def __init__(self, rating, path_to_the_file):
            # super().__init__(path_to_the_file)
            self.rating = rating
            self.filename = path_to_the_file
            self.sep = ','
            self.genres = {"Action", "Adventure", "Animation", "Children", "Comedy",'Crime', 
"Documentary",
"Drama",
"Fantasy",
"Film-Noir",
"Horror",
"Musical",
"Mystery",
"Romance",
"Sci-Fi",
"Thriller",
"War",
"Western",
"(no genres listed)"}

        def first_method(self):
            d = Counter()
            for val in self.rating.users:
                d[val] = len(self.rating.users[val])
            return d
        
        def second_method(self, metric):
            id_name = {}
            c = self.read_csv()
            for film_info in c:
                id_name[film_info] = c[film_info][0]
            id_rat = {}
            r = self.rating.read_csv()
            for i in r:
                id_rat[i[1]] = i[2]
            # print(self.dist_by_rating)

            # print(id_rat, id_name)
            new = Counter()
            # print(id_name)
            if (metric == 'mediana'):
                for val in self.rating.users:
                    med = round(self.my_median(self.rating.users[val]),2)
                    new[val] = med
                        # print(round(med,2))
            elif (metric == 'average'):
                for val in self.rating.users:
                    med = round(self.my_mean(self.rating.users[val]),2)
                    new[val] = med
                        # print(round(med,2))
            c = dict(sorted(new.items(), key=lambda x: (x[1], x[0]), reverse=True))
            return c
        
        def third_method(self, n):
            new = Counter()
            # print(id_name)
        
            for val in self.rating.users:
                med = round(self.variance(self.rating.users[val]),2)
                new[val] = med
                    # print(round(med,2))

            top_movies = dict(sorted(new.most_common(n), key=lambda x: x[-1], reverse=True))
            return top_movies



# if __name__ == "__main__":
#     # mov = Movies("movies.csv")
#     # mov.read_csv()
#     # mov.dist_by_release()
#     # mov.dist_by_genres()
#     # mov.most_genres(5)
#     # tag = Tags("tags.csv")
#     # tag.read_csv()
#     # tag.most_popular(5)
#     # tag.tags_with("Netflix")
#     # tag.most_words_and_longest(5)
#     # tag.most_words(100)
#     # tag.longest(6)
#     # l = Links("links.csv")
#     # l.read_csv()
#     # l.get_imdb(['52', '20', '45', '122'], ['movieId', 'Director', 'Budget', 'Cumulative Worldwide Gross', 'Runtime'])
#     # l.top_directors(10)
#     # l.most_expensive(5)
#     # l.most_profitable(5)
    # rat = Ratings("ratings.csv")
    # rat.read_csv()
#     # rat.get_movies().dist_by_year()
#     # rat.get_movies().dist_by_rating()
    # print(rat.get_movies().top_by_num_of_ratings(10))
#     # print(rat.get_movies().top_controversial(2000))
#     print(rat.get_users().second_method('mediana'))
#     print(rat.get_users().third_method(20))




class Tests:

    def test_movie(self): 
        self.movies = Movies('movies.csv')
        self.movies.read_csv()
        if not isinstance(self.movies.dist_by_release(), dict) or not isinstance(self.movies.dist_by_release(), OrderedDict):
            raise ValueError("Error type")
        if not isinstance(self.movies.dist_by_genres(), dict):
            raise ValueError("Error type")
        if not isinstance(self.movies.most_genres(10), dict):
            raise ValueError("Error type")

    def test_movie1(self): 
        self.movies = Movies('movies.csv')
        self.movies.read_csv()
        assert self.movies.dist_by_release() == OrderedDict(sorted(self.movies.dist_by_release().items(),key=lambda x: x[-1], reverse=True))
        assert self.movies.dist_by_genres() == dict(sorted(self.movies.dist_by_genres().items(), key=lambda x: x[-1], reverse=True))
        assert self.movies.most_genres(5) == dict(sorted(self.movies.most_genres(5).items(), key=lambda x: x[-1], reverse=True))
    
    def test_links(self):
        self.links = Links('links.csv')
        self.links.read_csv()
        if not isinstance(self.links.get_imdb(['52', '20', '45', '122'], ['movieId', 'Director', 'Budget', 'Cumulative Worldwide Gross', 'Runtime']), list):
            raise ValueError("Error type")
    #     if not isinstance(self.links.top_directors(5), dict):
    #         raise ValueError("Error type")
    #     if not isinstance(self.links.most_expensive(5), dict):
    #         raise ValueError("Error type")
    #     if not isinstance(self.links.most_profitable(5), dict):
    #         raise ValueError("Error type")
    #     if not isinstance(self.links.longest(5), dict):
    #         raise ValueError("Error type")
    #     if not isinstance(self.links.top_cost_per_minute(5), dict):
    #         raise ValueError("Error type")

    def test_links1(self):
        self.links = Links('links.csv')
        self.links.read_csv()
        cd = self.links.get_imdb(['52', '20', '45', '122'], ['movieId', 'Director', 'Budget', 'Cumulative Worldwide Gross', 'Runtime'])
        for t in cd:
            if not isinstance(t, list):
                raise ValueError("Error type")
    
    def test_links2(self):
        self.links = Links('links.csv')
        self.links.read_csv()
        cd = self.links.get_imdb(['52', '20', '45', '122'], ['movieId', 'Director', 'Budget', 'Cumulative Worldwide Gross', 'Runtime'])
        # print(sorted(cd))
        assert cd == sorted(cd, reverse=True)

    def test_ratings(self):
        self.rat = Ratings('ratings.csv')
        self.rat.read_csv()
        if not isinstance(self.rat.get_movies().dist_by_year(), dict):
            raise ValueError("Error type")
        if not isinstance(self.rat.get_movies().dist_by_rating(), dict):
            raise ValueError("Error type")
        if not isinstance(self.rat.get_movies().top_by_num_of_ratings(10), dict):
            raise ValueError("Error type")
        if not isinstance(self.rat.get_movies().top_by_ratings(10, 'mediana'), dict):
            raise ValueError("Error type")
        if not isinstance(self.rat.get_movies().top_controversial(2000), dict):
            raise ValueError("Error type")
    
    def test_ratings1(self):
        self.rat = Ratings('ratings.csv')
        self.rat.read_csv()
        assert self.rat.get_movies().dist_by_year() == dict(sorted(self.rat.get_movies().dist_by_year().items(), key=lambda x: x[-1], reverse=True))
        assert self.rat.get_movies().dist_by_rating() == dict(sorted(self.rat.get_movies().dist_by_rating().items(), key=lambda x: x[-1], reverse=True))
        assert self.rat.get_movies().top_by_num_of_ratings(10) == dict(sorted(self.rat.get_movies().top_by_num_of_ratings(10).items(), key=lambda x: x[-1], reverse=True))
        assert self.rat.get_movies().top_by_ratings(10, 'mediana') == dict(sorted(self.rat.get_movies().top_by_ratings(10, 'mediana').items(), key=lambda x: x[-1], reverse=True))
        assert self.rat.get_movies().top_controversial(200) == dict(sorted(self.rat.get_movies().top_controversial(200).items(), key=lambda x: x[-1], reverse=True))

    def test_tags(self):
        self.rat = Tags('tags.csv')
        self.rat.read_csv()
        if not isinstance(self.rat.most_words(100), dict):
            raise ValueError("Error type")
        if not isinstance(self.rat.longest(6), list):
            raise ValueError("Error type")
        if not isinstance(self.rat.most_words_and_longest(5), list):
            raise ValueError("Error type")
        if not isinstance(self.rat.most_popular(5), dict):
            raise ValueError("Error type")
        if not isinstance(self.rat.tags_with("Netflix"), list):
            raise ValueError("Error type")

    def test_tags1(self):
        self.rat = Tags('tags.csv')
        self.rat.read_csv()
        gg = self.rat.most_words(10)
        for kk in gg:
            if not isinstance(gg[kk], int):
                raise ValueError("Error type")
        gg = self.rat.most_popular(5)
        for kk in gg:
            if not isinstance(gg[kk], int):
                raise ValueError("Error type")

    def test_tags2(self):
        self.rat = Tags('tags.csv')
        self.rat.read_csv()
        assert self.rat.most_words(100) == dict(sorted(self.rat.most_words(100).items(), key=lambda x: x[-1], reverse=True))
        assert self.rat.tags_with("Netflix") == sorted(self.rat.tags_with("Netflix"), reverse=False)

    def test_tags2(self):
        self.rat = Ratings('ratings.csv')
        self.rat.read_csv()
        gg = self.rat.get_movies().dist_by_year()
        for kk in gg:
            if not isinstance(gg[kk], int):
                raise ValueError("Error type")
        gg = self.rat.get_movies().dist_by_rating()
        for kk in gg:
            if not isinstance(gg[kk], int):
                raise ValueError("Error type")
        gg = self.rat.get_movies().top_by_num_of_ratings(10)
        for kk in gg:
            if not isinstance(gg[kk], int):
                raise ValueError("Error type")
        gg = self.rat.get_movies().top_by_ratings(10, 'mediana')
        for kk in gg:
            if not isinstance(gg[kk], float):
                raise ValueError("Error type")
        gg = self.rat.get_movies().top_controversial(10)
        for kk in gg:
            if not isinstance(gg[kk], float):
                raise ValueError("Error type")

    def test_movie2(self): 
        self.movies = Movies('movies.csv')
        self.movies.read_csv()
        gg = self.movies.dist_by_release()
        for kk in gg:
            if not isinstance(gg[kk], int):
                raise ValueError("Error type")
        gg = self.movies.dist_by_genres()
        for kk in gg:
            if not isinstance(gg[kk], int):
                raise ValueError("Error type")
        gg = self.movies.most_genres(10)
        for kk in gg:
            if not isinstance(gg[kk], int):
                raise ValueError("Error type")