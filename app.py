import gc
import flask
import numpy as np
import pandas as pd
import difflib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


app = flask.Flask(__name__, template_folder='templates')

movies_data = pd.read_csv('movies.csv')

collected = gc.collect()

selected_features = ['genres','keywords','tagline','cast','director','vote_average','popularity']
collected = gc.collect()

for feature in selected_features:
  movies_data[feature] = movies_data[feature].fillna('')
  
collected = gc.collect()

combined_features = movies_data['genres']+' '+movies_data['keywords']+' '+movies_data['tagline']+' '+movies_data['cast']+' '+movies_data['director']+' '+str(movies_data['vote_average'])+' '+ str(movies_data['popularity'])
vectorizer = TfidfVectorizer()
collected = gc.collect()
feature_vectors = vectorizer.fit_transform(combined_features)
similarity = cosine_similarity(feature_vectors)
collected = gc.collect()
list_of_all_titles = movies_data['title'].tolist()

collected = gc.collect()

# Set up the main route
@app.route('/', methods=['GET', 'POST'])

def main():
    if flask.request.method == 'GET':
        return(flask.render_template('index.html'))

    if flask.request.method == 'POST':
        m_name = flask.request.form['movie_name']
        find_close_match = difflib.get_close_matches(m_name, list_of_all_titles)
        collected = gc.collect()

        if find_close_match==[]:
            return flask.render_template('positive.html',movie_names=["Empty_List"],movie_date=["Empty_List"],movie_dir=["Empty_List"], search_name="Not in dataset")
        close_match = find_close_match[0]
        collected = gc.collect()

        index_of_the_movie = movies_data[movies_data.title == close_match]['index'].values[0]
        collected = gc.collect()

        similarity_score = list(enumerate(similarity[index_of_the_movie]))
        collected = gc.collect()

        sorted_similar_movies = sorted(similarity_score, key = lambda x:x[1], reverse = True)
        collected = gc.collect()

        i = 1
        names = []
        genre = []
        dir=[]
        for movie in sorted_similar_movies:

            index = movie[0]
            title_from_index = movies_data[movies_data.index==index]['title'].values[0]
            genre_from_index = movies_data[movies_data.index==index]['genres'].values[0]
            dir_from_index = movies_data[movies_data.index==index]['homepage'].values[0]
            collected = gc.collect()

            if (i<16):
                names.append(title_from_index)
                genre.append(genre_from_index)
                dir.append(dir_from_index)
                collected = gc.collect()

                #print(i, '.',title_from_index,'->', genre_from_index,'by',director_from_index)
            i+=1
        return flask.render_template('positive.html',movie_names=names,movie_date=genre,movie_dir=dir, search_name=m_name)
        collected = gc.collect()

if __name__ == '__main__':
    app.run()
