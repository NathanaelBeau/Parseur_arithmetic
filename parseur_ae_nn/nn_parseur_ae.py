import torch

import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

from parseur_ae_nn.data_parseur_ae import *


class Net(nn.Module):

    def __init__(self, input_size, hidden_size, output_size):
        super(Net, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, hidden_size)
        self.fc3 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return F.log_softmax(x, dim=-1)


def train(epochs, model, X_train, X_test, y_train, y_test, PATH='./modelparameters/model.pt'):
    epoch_data = []
    optimizer = optim.Adam(model.parameters())
    loss_fn = nn.NLLLoss()
    for epoch in range(1, epochs):
        optimizer.zero_grad()  # set the grad to 0
        y_pred = model(X_train)

        loss = loss_fn(y_pred, y_train)
        loss.backward()  # compute derivative wrt parameters

        optimizer.step()  # set learning rate

        y_pred_test = model(X_test)
        loss_test = loss_fn(y_pred_test, y_test)

        _, pred = y_pred_test.data.max(1)

        accuracy = pred.eq(y_test.data).sum().item() / y_test.size()[0]
        epoch_data.append([epoch, loss.data.item(), loss_test.data.item(), accuracy])

        if epoch % 100 == 0:
            print('epoch - %d (%d%%) train loss - %.2f test loss - %.2f accuracy - %4.f' \
                  % (epoch, epoch / 150 * 10, loss.data.item(), loss_test.data.item(), accuracy))

    torch.save(model, PATH)


if __name__ == "__main__":
    dataframe = Create_Parseur_Dataframe().create_dataframe(number_example=1000, size_example=11)
    X = Create_Parseur_Dataset().create_dataset_input(dataframe)
    y = Create_Parseur_Dataset().create_dataset_output(dataframe)
    X_train, X_test, y_train, y_test = Create_Parseur_Dataset().split_train_test(X, y)
    model = Net(42, 6, 2)
    train(1000, model, X_train, X_test, y_train, y_test)
