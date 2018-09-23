import random
import numpy as np
import tensorflow as tf
from keras.models import load_model

class Node:
    def __init__(self, name):
        self.name = name
        self.edges = []

    def addEdge(self, node):
        self.edges.append(node)


def skill_puzzle(data):
    offensive = data["boss"]["offense"]

    attack_list = []
    offense_list = []
    points_list = []
    attack_offense_dict = {}
    attack_point_dict = {}
    nodes = []
    final_attack_list = []

    for skill in data["skills"]:
        attack_list.append(skill["name"])
        offense_list.append(skill["offense"])
        points_list.append(skill["points"])
        attack_point_dict.update({skill["name"]: skill["points"]})
        attack_offense_dict.update({skill["name"]: skill["offense"]})

        curr_node = Node(skill["name"])
        nodes.append(curr_node)

        if skill["require"] in attack_list:
            nodes[attack_list.index(skill["require"])].addEdge(curr_node)

    # print(attack_point_dict)
    # sorted_attack_point_dict = [{k: attack_point_dict[k]} for k in sorted(attack_point_dict, key=attack_point_dict.get)]
    # print(sorted_attack_point_dict)

    resolved = []
    seen = []

    def dep_resolve(node, resolved, seen):
        resolved.append(node)
        seen.append(node)
        if node not in seen:
            for edge in node.edges:
                if edge not in seen:
                    dep_resolve(edge, resolved, seen)
                else:
                    continue

    for node in nodes:
        dep_resolve(node, resolved, seen)

    # for node in resolved:
    #     print(node.name)

    current_offense = 0

    for attack in resolved:
        if current_offense < offensive:
            # print(attack.name)
            current_offense += attack_offense_dict[attack.name]
            # print("current offense: ", current_offense)
            final_attack_list.append(attack.name)
        else:
            break

    return final_attack_list


def machine_learning_q1(data):
    input = data["input"]
    output = data["output"]
    question = data["question"]

    from ortools.linear_solver import pywraplp

    # Instantiate a Glop solver, naming it LinearExample.
    solver = pywraplp.Solver('LinearExample',
                             pywraplp.Solver.GLOP_LINEAR_PROGRAMMING)

    # Create the two variables and let them take on any value.
    x = solver.NumVar(-solver.infinity(), solver.infinity(), 'x')
    y = solver.NumVar(-solver.infinity(), solver.infinity(), 'y')
    z = solver.NumVar(-solver.infinity(), solver.infinity(), 'z')

    for i in range(0, len(data["input"])):
        # Constraint : x + y + z == output.
        constraint = solver.Constraint(output[i], output[i])
        constraint.SetCoefficient(x, input[i][0])
        constraint.SetCoefficient(y, input[i][1])
        constraint.SetCoefficient(z, input[i][2])

    solver.Solve()

    print('Solution:')
    print('x = ', x.solution_value())
    print('y = ', y.solution_value())
    print('z = ', z.solution_value())

    answer = x.solution_value() * question[0] + y.solution_value() * question[1] + z.solution_value() * question[2]

    return {"answer": answer}


def train_model():
    (x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()

    # import matplotlib.pyplot as plt
    # image_index = 7777  # You may select anything up to 60,000
    # print(y_train[image_index])  # The label is 8
    # plt.imshow(x_train[image_index], cmap='Greys')
    # Reshaping the array to 4-dims so that it can work with the Keras API
    x_train = x_train.reshape(x_train.shape[0], 28, 28, 1)
    x_test = x_test.reshape(x_test.shape[0], 28, 28, 1)
    input_shape = (28, 28, 1)
    # Making sure that the values are float so that we can get decimal points after division
    x_train = x_train.astype('float32')
    x_test = x_test.astype('float32')
    # Normalizing the RGB codes by dividing it to the max RGB value.
    x_train /= 255
    x_test /= 255
    print('x_train shape:', x_train.shape)
    print('Number of images in x_train', x_train.shape[0])
    print('Number of images in x_test', x_test.shape[0])

    # Importing the required Keras modules containing model and layers
    from keras.models import Sequential
    from keras.layers import Dense, Conv2D, Dropout, Flatten, MaxPooling2D
    # Creating a Sequential Model and adding the layers
    model = Sequential()
    model.add(Conv2D(28, kernel_size=(3, 3), input_shape=input_shape))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Flatten())  # Flattening the 2D arrays for fully connected layers
    model.add(Dense(128, activation=tf.nn.relu))
    model.add(Dropout(0.2))
    model.add(Dense(10, activation=tf.nn.softmax))

    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    model.fit(x=x_train, y=y_train, epochs=10)
    model.save("image_model.h5")
    print(model.evaluate(x_test, y_test))


def predict_images(data):
    images = data["question"]
    result = []
    # load the model from the .h5 file
    model = load_model("./image_model.h5")

    for image in images:
        # get np array of image
        np_image = np.asarray(image)
        # the image is 28 x 28 pixels, so reshape the array
        pred = model.predict(np_image.reshape(1, 28, 28, 1))

        result.append(pred.argmax())

    return {"answer": result}


if __name__ == "__main__":
    # (x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()
    data = {"question":[[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,101,123,170,235,261,158,97,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,155,226,278,263,275,217,266,206,32,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,167,241,275,218,187,127,192,220,244,113,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,53,255,225,214,31,12,0,7,180,268,153,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,67,235,219,23,0,0,0,105,250,268,57,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,28,18,0,0,0,0,232,285,242,61,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,122,244,261,173,11,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,87,259,263,236,70,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,142,234,254,136,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,184,261,278,164,11,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,22,252,265,205,35,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,177,260,261,134,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,67,282,289,214,12,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,19,197,234,253,146,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,124,262,219,180,14,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,269,234,259,26,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,212,253,268,46,21,23,21,19,4,0,6,20,22,36,153,150,138,160,11,0,0,0,0,0,0,0,0,0,230,260,261,284,280,269,233,285,181,162,153,255,258,241,271,278,262,278,119,0,0,0,0,0,0,0,0,0,154,290,241,231,273,278,245,289,271,248,236,235,215,249,226,157,104,109,53,0,0,0,0,0,0,0,0,0,0,107,137,123,137,167,290,272,243,146,138,134,36,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]}
    print(predict_images(data))

