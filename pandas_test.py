import pandas as pd
import os
import numpy as np
from pandas import Series, DataFrame

os.chdir('C:\\Users\\alexschindele\\Documents\\Coding')
userinfo_columns = ['user_id', 'gender', 'age', 'occupation', 'zip']
users = pd.read_table('ml-1m\\users.dat', sep='::', header=None, names=userinfo_columns, engine='python')

ratings_columns = ['user_id', 'movie_id', 'rating', 'timestamp']
ratings = pd.read_table('ml-1m\\ratings.dat', sep='::', header=None, names=ratings_columns, engine='python')

movies_columns = ['movie_id', 'title', 'genres']
movies = pd.read_table('ml-1m\\movies.dat', sep='::', header=None, names=movies_columns, engine='python')

data = pd.merge(pd.merge(ratings, users), movies)

print(data[:5])

mean_ratings = pd.pivot_table(data, index='title', values='rating', columns='gender', aggfunc='mean')
ratings_by_title = data.groupby('title').size()
active_titles = ratings_by_title.index[ratings_by_title >= 250]
mean_ratings = mean_ratings.ix[active_titles]

top_female_ratings = mean_ratings.sort_values(by='F', ascending=False)
print(top_female_ratings[:5])

mean_ratings['diff'] = mean_ratings['M'] - mean_ratings['F']
sorted_by_diff = mean_ratings.sort_index(by="diff")

rating_std_by_title = data.groupby('title')['rating'].std()
rating_std_by_title = rating_std_by_title.ix[active_titles]
sorted_rating_std = rating_std_by_title.sort_values(ascending=False)

#Next steps: figuring out genres!

# Using numpy
# ndarray

array = np.array([[6, 3, 5], [2, 4, 5]])
print(array.ndim)
print(array.shape)

zero_array = np.zeros(3)
zero_2d_array = np.zeros((3, 4))  # make sure you use a tuple as the argument
zeroed_copy_of_array = np.zeros_like(array)
one_array = np.ones(4)
empty_array = np.empty((3, 4, 3))  # can use any number of dimensions

one_to_ten = np.arange(10)



