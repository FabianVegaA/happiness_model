from utils import Utils
from models import Models


if __name__ == '__main__':
    utils = Utils()
    models = Models()

    data = utils.load_from_csv()

    X, y = utils.features_target(data, ['score'], ['score'])

    print(X, y)

    models.grid_training(X, y)
