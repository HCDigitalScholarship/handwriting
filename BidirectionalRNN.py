
# import TestDataGenerator class from TestData.py
from TestData import TestDataGenerator

import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Input, LSTM, Bidirectional, Reshape, Flatten
from keras import backend as K
from copy import copy



# SETTINGS
##############################################################################

SAMPLE_SIZE = 1000  # number of data points to generate if using test data
SEQ_LENGTH = 10 # for sequential test data, SAMPLE_SIZE must be divisible by SEQ_LENGTH
INPUT_DIM = 1  
OUTPUT_DIM = 1

EPOCHS = 20
BATCH_SIZE = 1

DATA = "sequential"    # "cosine" or "sequential"

##############################################################################

G = TestDataGenerator()

if (DATA == "cosine"):

  # generate SAMPLE_SIZE number of pairs (x[i], cos(x[i]))
  train_data = G.cosine(SAMPLE_SIZE)

  # restrict x to [0, 2*Pi]
  x_train = np.array([[x  % (6*np.pi)] for x, y in train_data])
  y_train = np.array([[y] for x, y in train_data])

  # grab random indices for sequences of cosine data
  seeds = np.random.permutation(range(0, SAMPLE_SIZE - (SEQ_LENGTH +1)))

  # for proof of concept, making train and validation set identical
  x_train = np.array([x_train[seed:seed + SEQ_LENGTH] for seed in seeds])
  y_train = np.array([y_train[seed + SEQ_LENGTH + 1] for seed in seeds])
  x_val = copy(x_train)
  y_val = copy(y_train)

  print("Using cosine test data.")

elif (DATA == "sequential"):

  DIRECT = "forward" # forward or reverse.

  # generate SAMPLE_SIZE number of pairs (x[i], x[i+1])
  train_data = G.sequential(SAMPLE_SIZE, direct=DIRECT)
  x_train = np.array([[x] for x, y in train_data])
  y_train = np.array([[y] for x, y in train_data])

  val_data = G.sequential(SAMPLE_SIZE // 2, direct=DIRECT)
  x_val = np.array([[x]for x, y in train_data])
  y_val = np.array([[y] for x, y in train_data])

  x_train = x_train.reshape(x_train.shape[0]//SEQ_LENGTH, SEQ_LENGTH, x_train.shape[1])
  offset = 9 if DIRECT == "forward" else 8 
  y_train = y_train[offset::SEQ_LENGTH]
  x_val = x_val.reshape(x_val.shape[0]//SEQ_LENGTH, SEQ_LENGTH, x_val.shape[1])
  y_val = y_val[offset::SEQ_LENGTH]

  print("Using sequential test data.")

else:
  print("Using user defined data.")



print("Predictors shape:", x_train.shape)
print("Labels shape:", y_train.shape)


####################################################################################
## To use data other than the test datasets:                                      ##
##    1) Change the DATA variable to anything other than "cosine" or "sequential" ##
##    2) Load your data into the variables x_train, y_train, x_val, y_val         ##
####################################################################################




####################################################################################

# here is a very basic model for example.
model = Sequential()
model.add(Bidirectional(LSTM(5), input_shape=(SEQ_LENGTH, INPUT_DIM))) # shape = (Batch size, Seq length, Input dim)
model.add(Dense(3))
model.add(Dense(OUTPUT_DIM))
model.compile(loss='mse',
              optimizer='rmsprop',
              metrics=['mae'])

model.summary()

model.fit(x_train, y_train, validation_data=(x_val, y_val),
        epochs=EPOCHS, batch_size=BATCH_SIZE)

# make predictions on x_val
y_hat = model.predict(x_val, batch_size=BATCH_SIZE)




# create list of tuples (input, output) for targets and for the model's predictions
targets = list(zip(range(len(y_val)), y_val))
pred = list(zip(range(len(y_hat)), y_hat))


# creates plots to see results. If any errors are raised here, just comment these lines out.

# Show results
G.show_data(pred)
G.show_data(targets)

# compare true vs. predicted
G.show_comparison(targets, pred)



