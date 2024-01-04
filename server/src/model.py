from sklearn.datasets import load_iris
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split


class Model():

    def __init__(self) -> None:
        self.model = None

    def get_model(self):
        """
        Function responsible to create the SVC model using load_dataset method
        """

        self.load_dataset()
        X_train, _, y_train, _ = train_test_split(self.data_X, self.data_y, test_size=0.2, random_state=42)

        self.model = SVC(kernel='linear')
        self.model.fit(X_train, y_train)

    def load_dataset(self):
        """
        Function where the dataset is loaded
        """
        dataset = load_iris()
        self.target_names = list(dataset.target_names)
        self.data_X = dataset.data  # Features
        self.data_y = dataset.target  # Labels

    def get_inference(self, new_data):
        """
        Function responsible for performing an inference on the model.

        Args:
        - new_data (list[float])

        Returns:
        - predictions: str
        """
        predictions = self.model.predict(new_data)
        return predictions

