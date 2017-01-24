# this file will take in the training set data (screenshots and the associated keypress time)


# then create a tensorflow object that will be inputted into the endless_lake_player.py file as a model input

import tensorflow as tf

class ModelerTF(object):

    def __init__(self):
        pass

    def import_data(self, fname):
        pass

    def run_tf(self):

        # placeholder that will contain input
        x = tf.placeholder(tf.float32, [None, 784])

        # model parameters
        w = tf.Variable(tf.zeros([784, 10]))
        b = tf.Variable(tf.zeros([10]))

        # create the model
        y = tf.nn.softmax(tf.matmul(x, w) + b)

        # placeholder variable that will contain correct answers
        y_ = tf.placeholder(tf.float32, [None, 10])

        # run cross entropy
        cross_entropy = tf.reduce_mean(-tf.reduce_sum(y_ * tf.log(y), reduction_indices=[1]))
        train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)

        init = tf.global_variables_initializer()

        sess = tf.Session()
        sess.run(init)

        # need data for MNIST
        for i in range(1000):
            batch_xs, batch_ys = mnist.train.next_batch(100)
            sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys})

        correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))

        accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

        print(sess.run(accuracy, feed_dict={x: mnist.test.images, y_: mnist.test.labels}))