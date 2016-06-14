# IMPORTS
import numpy
from sklearn import ensemble
import sklearn
from sklearn.preprocessing import Imputer
import matplotlib.pyplot as plt

# CONSTANTS
N_TREES = 5

################# FUNCTIONS I NEED ####################################################################################

def return_real_data():
	"""
	The function returns the X matrix that contains the real data
	The rows of the matrix represent events and the columns represent feature values for each event
	The function also returns a vector with the events IDs, preferebly integers
	Erez implements:
	>> return obj_ids, X
	NOTE: I created some data with 2 features so you could see with the demo how the RF performs
	"""
        data_mat = numpy.loadtxt("/Users/erezcohen/Desktop/DataMining/AnaFiles/C12_Full_ppp_events.txt", delimiter="\t")
        obj_ids = data_mat[:,0]
        X = data_mat[:,1:]
        print obj_ids
        print X
        
	return obj_ids, X

def return_synthetic_data(X):
	"""
	The function returns a matrix with the same dimensions as X but with synthetic data
	based on the marginal distributions of its featues
	"""
	features = len(X[0])
	X_syn = numpy.zeros(X.shape)

	for i in xrange(features):
		obs_vec = X[:,i]
		syn_vec = numpy.random.choice(obs_vec, len(obs_vec))
		X_syn[:,i] += syn_vec

	return X_syn

def merge_work_and_synthetic_samples(X, X_syn):
	"""
	The function merges the data into one sample, giving the label "1" to the real data and label "2" to the synthetic data
	"""
	# build the labels vector
	Y = numpy.ones(len(X))
	Y_syn = numpy.ones(len(X_syn)) * 2

	Y_total = numpy.concatenate((Y, Y_syn))
	X_total = numpy.concatenate((X, X_syn))
	return X_total, Y_total

def train_random_forest(X, Y, n_train):
	"""
	The function trains a random forest with the features X and results Y and returns the random forest
	"""
	rand_tree = sklearn.ensemble.RandomForestClassifier(n_estimators=n_train)
	rand_tree.fit(X, Y)
	return rand_tree

def build_similarity_matrix_naive(rand_tree, X):
	"""
	The function builds the similarity matrix based on the feature matrix X for the results Y
	based on the random forest we've trained
	the matrix is normalised so that the biggest similarity is 1 and the lowest is 0
	IMPORTANT: This function is not optimally implemented for speed, but rather to low memory CPUs
	also, it does not remove leaves that predict the object to be in the synthetic class, use this function only in order to understand the algorithm
	"""
	apply_mat = rand_tree.apply(X)
	obs_num = len(apply_mat)
	sim_mat = numpy.eye(obs_num) * len(apply_mat[0]) # max values that they can be similar at = N estimators

	for i in xrange(obs_num):
		for j in xrange(i, obs_num):
			vec_i = apply_mat[i]
			vec_j = apply_mat[j]
			sim_val = len(vec_i[vec_i==vec_j])
			sim_mat[i][j] = sim_val
			sim_mat[j][i] = sim_val

	return sim_mat / len(apply_mat[0])

def build_similarity_matrix(rand_tree, X):
	"""
	The function builds the similarity matrix based on the feature matrix X for the results Y
	based on the random forest we've trained
	the matrix is normalised so that the biggest similarity is 1 and the lowest is 0

	This function counts only leaves in which the object is classified as a "real" object 
	it is also implemented to optimize running time, asumming one has enough running memory
	"""
	# apply to get the leaf indices
	apply_mat = rand_tree.apply(X)
	# find the predictions of the sample
	is_good_matrix = numpy.zeros(apply_mat.shape)
	for i, est in enumerate(rand_tree.estimators_):
		d = est.predict_proba(X)[:, 0] == 1
		is_good_matrix[:, i] = d
	# mark leaves that make the wrong prediction as -1, in order to remove them from the distance measurement
	apply_mat[is_good_matrix == False] = -1 
	# now calculate the similarity matrix
	sim_mat = numpy.sum((apply_mat[:, None] == apply_mat[None, :]) & (apply_mat[:, None] != -1) & (apply_mat[None, :] != -1), axis=2) / numpy.asfarray(numpy.sum([apply_mat != -1], axis=2), dtype='float')
	return sim_mat

def convert_sim_to_dis_mat(sim_mat):
	"""
	The function converts the similarity matrix to dissimilarity matrix 
	in a way that maximises the penalty on the dissimilar objects
	"""
	dis_mat = 1 - sim_mat
	return dis_mat

################ RF EXECUTION #########################################################################################

def find_outliers(N_outliers, obj_ids=None, X=None):
	"""
	The function returns the N best outliers in the data
	"""
	# get the real data and the IDs of the events in case I didn't get them from the demo
	if obj_ids == None and X == None:
		obj_ids, X = return_real_data()
	# remove NULL values
	X_trans = Imputer(strategy="median").fit_transform(X)
	X = None 
	# construct synthetic data
	X_syn = return_synthetic_data(X_trans)
	# merge real and synthetic data
	X_total, Y_total = merge_work_and_synthetic_samples(X_trans, X_syn)
	X_syn = None
	# train random forest
	rand_tree = train_random_forest(X_total, Y_total, N_TREES)
	# build similairty matrix
	sim_mat = build_similarity_matrix(rand_tree, X_trans)
	# convert to dissimilarity matrix
	dis_mat = convert_sim_to_dis_mat(sim_mat)
	sim_mat = None
	# sum the distance matrix and obtain a "weirdness score"
	sum_vec = numpy.sum(dis_mat, axis=1)
	sum_vec /= float(len(sum_vec))
	# sort and extract the N best outliers
	sum_vec_sorted = numpy.sort(sum_vec)[::-1]
	obj_ids_sorted = obj_ids[numpy.argsort(sum_vec)][::-1]

	return sum_vec_sorted[:N_outliers], obj_ids_sorted[:N_outliers], 


############### DEMO #####################################################################################################

def demo():
	"""
	run this to see how it works on a data I've built! :)
	"""
	# build data to play with
	obj_ids, X = return_real_data()
	# find the best 10 outliers
	scores_10, obj_ids_10 = find_outliers(10, obj_ids, X)

#	# plot them!
#	plt.figure(1)
#	plt.title(r'$x_{B} \; vs. \; Q^{2}$')
#	plt.plot(X[:,0], X[:,1], "ok")
#	plt.xlabel(r'$x_{B}$')
#	plt.ylabel(r'$Q^{2} (GeV/c)^{2}$')
#        print obj_ids_10.astype(int)
#        print X[obj_ids_10.astype(int),1]

        fig = plt.figure(2)
        plt.title(r'$x_{B} \; vs. \; Q^{2}$'+" + 10 best outliers", fontsize=18)
        plt.plot(X[:,0], X[:,1], "ok")
        plt.plot(X[obj_ids_10.astype(int),0], X[obj_ids_10.astype(int),1], "or")
        plt.xlabel(r'$x_{B}$', fontsize=22)
        plt.ylabel(r'$Q^{2} (GeV/c)^{2}$', fontsize=22)


	plt.show()
        fig.savefig('/Users/erezcohen/Desktop/XbQ2_TenBestOutliers.pdf')
