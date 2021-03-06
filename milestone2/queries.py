from requests import *
import json

SELECT_URL = 'http://localhost:8983/solr/movies/select'

# get Drama movies before 2000 Tobey Maguire took part in (sorted by vote desc)
params = {
    'q': '{!parent which="-_nest_path_:* *:*"}name:"Tobey Maguire"',
    'indent': 'true',
    'fl': '*, [child]',
    'q.op': 'OR',
    'fq': ['year:[* TO 1999]',
           'genre:drama'],
    'sort': 'weighted_average_vote desc',
    'wt': 'json',
}

movies = get(SELECT_URL, params=params)
movies_json = json.loads(movies.text)["response"]["docs"]

print('Drama movies before 2000 Tobey Maguire took part in (sorted by vote desc):')
for doc in movies_json:
    print("> %s - %s - %s" % (doc['imdb_title_id'], doc["original_title"], doc["year"]))

print()
# get comedy movies from the 20's with at least 8.0 as mean vote, sorted by year asc and mean vote desc
params = {
    'q': 'title:* AND genre:comedy AND year:[1920 TO 1930] AND mean_vote:[8.0 TO *]',
    'sort': 'year asc, mean_vote desc',
    'fl': '*,[child]',
    'rows': 1000
}

movies = get(SELECT_URL, params=params)
movies_json = json.loads(movies.text)["response"]["docs"]

# ---

print('Comedy movies from the 20\'s:')
for doc in movies_json:
    print("> %s - %s - %d - %.02f" % (doc['imdb_title_id'], doc['original_title'], doc['year'], doc['mean_vote'][0]))

# worst 10 rated horror movies since 2000
params = {
    'q': 'genre:horror year:[2000 TO *]',
    'q.op': 'and',
    'sort': 'weighted_average_vote asc',
    'fl': 'imdb_title_id, original_title, mean_vote',
    'rows': 10
}

movies = get(SELECT_URL, params=params)
movies_json = json.loads(movies.text)["response"]["docs"]

print()
print('Worst 10 rated horror movies since 2000')
for i in range(len(movies_json)):
    doc = movies_json[i]
    print("#%d %s - %s - %.02f" % (i + 1, doc['imdb_title_id'], doc['original_title'], doc['mean_vote'][0]))

# ---

# top 10 rated Drama movies with at least 100000 votes
params = {
    'q': 'mean_vote:* AND genre:Drama AND total_votes:[100000 TO 999999999]',
    'sort': 'mean_vote desc',
    'fl': 'imdb_title_id, original_title, mean_vote, total_votes',
    'rows': 10
}

movies = get(SELECT_URL, params=params)
movies_json = json.loads(movies.text)["response"]["docs"]

print()
print('Top 10 rated movies\'s')
for i in range(len(movies_json)):
    doc = movies_json[i]
    print("#%d %s - %s - %.02f - %d" % (
        i + 1, doc['imdb_title_id'], doc['original_title'], doc['mean_vote'][0], doc['total_votes'][0]))

# ---

# Use uf to get movies with word Crime in the title ignoring genre
params = {
    'q': 'title:Crime AND genre:Crime',
    'uf': 'title',
    'sort': 'mean_vote desc',
    'fl': 'imdb_title_id, original_title, mean_vote, total_votes',
    'rows': 10
}

movies = get(SELECT_URL, params=params)
movies_json = json.loads(movies.text)["response"]["docs"]

print()
print('Movie\'s with the word Crime in title')
for i in range(len(movies_json)):
    doc = movies_json[i]
    print("#%d %s - %s - %.02f - %d" % (
        i + 1, doc['imdb_title_id'], doc['original_title'], doc['mean_vote'][0], doc['total_votes'][0]))

# ---

# Action movies from the 20\'s 1hour or shorter where at least one actor has New York mentioned on their
# biography, sorted by weighted average vote descending:

params = {
    'q': '{!parent which="-_nest_path_:* *:*"}bio:"new york" role:actor',
    'indent': 'true',
    'fl': '*, [child]',
    'q.op': 'AND',
    'fq': ['year:[1920 TO 1929]',
           'genre:action',
           'duration:[* TO 60]'],
    'sort': 'weighted_average_vote desc',
    'wt': 'json'
}

movies = get(SELECT_URL, params=params)
movies_json = json.loads(movies.text)["response"]["docs"]

print()
print('Action movies from the 20\'s 1hour or shorter where at least one actor has New York mentioned on their '
      'biography, sorted by weighted average vote descending: ')
for i in range(len(movies_json)):
    doc = movies_json[i]
    print("#%d %s - %s - %.02f" % (
        i + 1, doc['imdb_title_id'], doc['original_title'], doc['mean_vote'][0]))

# ---

# best movie by genre with at least 10000 votes
params = {
    'q': 'mean_vote:* AND total_votes:[10000 TO *]',
    'sort': 'mean_vote desc',
    'fl': 'imdb_title_id, original_title, mean_vote, total_votes',
    'rows': 1000,
    'group': 'true',
    'group.field': 'genre'
}

movies = get(SELECT_URL, params=params)
groups = json.loads(movies.text)['grouped']['genre']['groups']

print()
print('Best movie\'s by genre with at least 10000 votes')
for group in groups:
    group_values = group['doclist']['docs'][0]
    print("> %s" % (group['groupValue']))
    print("\t>ID: %s" % group_values['imdb_title_id'])
    print("\t>Title: %s" % group_values['original_title'])
    print("\t>Total votes: %s" % group_values['total_votes'][0])
    print("\t>Mean vote: %s" % group_values['mean_vote'][0])
