from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Embedding, LSTM, Conv1D, MaxPooling1D, Dropout
import data_helpers
from datetime import datetime
startTime = datetime.now()
print (startTime)

train_X, val_X, train_y, val_y = data_helpers.load_data_and_labels()
tokenizer, max_length, vocab_size, encoded_train_X, padded_train_X, padded_val_X = data_helpers.give_labels_and_pad_predictors(train_X, val_X, train_y, val_y)
embeddings_index = data_helpers.load_GloVe()
# embedding_matrix = matrix of predefined weights
embedding_matrix = data_helpers.creating_embedding_matrix(tokenizer, vocab_size, embeddings_index, encoded_train_X)

e = Embedding(vocab_size, 50, input_length=max_length, weights=[embedding_matrix], trainable=False)

model = Sequential()
model.add(e)
model.add(Dropout(0.2))
model.add(Conv1D(64, 5, activation='relu'))
model.add(MaxPooling1D(pool_size=4))
model.add(LSTM(50))
model.add(Dense(1, activation ='sigmoid'))

# compile the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['acc'])
print(model.summary())
model.fit(padded_train_X, train_y, epochs=50, batch_size=40,verbose=0)
#model.fit(padded_train_X, train_y, epochs=75, batch_size=60, verbose=0)
scores = model.evaluate(padded_val_X, val_y, verbose=0)
print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))
print(datetime.now()- startTime)
