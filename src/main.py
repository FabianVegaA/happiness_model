from utils import Utils
from models import Models


if __name__ == '__main__':
    utils = Utils()
    models = Models()

    data = utils.load_from_csv('./in/2015.csv')
    print(data)

    X, y = utils.features_target(data, ['Country', 'Region', 'Happiness Rank', 'Happiness Score', 'Standard Error'], ['Happiness Score'])

    models.grid_training(X, y)
