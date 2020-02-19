# TOO SHORT

## Brief description:

This is a package intended to make your life easier, and automate a lot of the common things dealt with in supervised learning. Specifically with building and testing sklearn models. Although, it also relies on some other useful tools like SMOTE for imabalanced data.

In short:

- Chooses relevant models for you based on the type of problem (classification or regression)
- Provides param grids for the chosen models
- Wraps all the preprocessing into one function so you can do somewhat customized preprocessing with a oneliner
- Wraps Oversampling and undersampling using the imbalanced learn package to simplify the process
- Feature selection based on a model input
- Automatically splitting train and test sets, as well as evaluting them seperately.
- Most importantly, provides a simple method to search and compare all the relevant models and grids with either your original data, or the transformed version set in the preprocessing, oversampling, or feature selection step.

## Class methods

The module exposes one class, too_short.

##### init

`def __init__(self, X=None, y=None, prediction_type=None):`

**init function**

**Args:**
X: pd.dataframe - Df with full X data (will be split within init) - optional (you will need to include this for most functionality)
y: list - list of targets (will be split within init) - optional (you will need to include this for most functionality)
prediction_type: string - String of either "classification" or "regression" - optional (you will need to include this for most functionality)

**Returns:**
None

##### set_attributes

`def set_attributes(self, X=None, y=None, X_test=None, y_test=None, X_train=None, y_train=None, prediction_type=None, imb_pipeline_steps=None, models=None):`

**Function for setting class attributes manually. Useful for overriding defaults if you are trying to test different settings**

**Args:**
X: Pd dataframe containing X - optional
y: target list - optional
X_test: pd dataframe - optional
y_test: pd dataframe - optional
X_train: pd dataframe - optional
y_train: pd dataframe - optional
prediction_type: string - Either "classification" or "regression" - optional
imb_pipline_steps: list - Containing imbalanced learn Pipeline steps. ex [('smote', SMOTE(random_state=random_state))]. If you want to use this within the search method
dont add a sklearn model step to the end of this, that will be done automatically in the the search function. - optional
models: list - List of models to be used in in the search function. This would be set automatically in choose_models function, but you can override here. Do not instantiate the models within the list. - optional

**Returns:**
None

##### get_param_grid

`def get_param_grid(self, model, prepend=None):`

**Function providing a hyperparam grid to be used in sklearn hyperparameter optimizatoin. This is automatically called internally in the search function, the user need not call this directly.**

**Args:**
model: sklearns model.**name** property - Required
prepend: string to be prepended to grid keys for grid search along with to underscores. this will generally be the model name as a string. ie "LogisticRegression" - optional

**Returns:**
Dictionary containing sklearn params as keys and list of param options as values

**Example:**
get_param_grid(LinearRegression)

> > {'normalize': [True, False]}

##### preproc

`def preproc(self, OHE=[], standard_scale=[], numerical_impute=[], categegorical_impute=[], label_encode={}):`

**Prerocesses data frames, including onehot encoding, scaling, and imputation, and label encoding**

**Args:**
OHE: Array of columns to be processed with sklearn OneHotEncoder, this accepts non numerical categorical rows without need for label encoding. - Default []
standard_scale: list. List of columns to be processes with standard scalar. - Defualt []
numerical_impute: list. list of column names that should be imputed using mean method. - Default []
categorical_impute: list. list of column names that should be imputed to 'missing'. - Default []
label_encode: dict. Keys in the dict should be the column names to transform, the values should be lists that
contain the various values in the column, the order of the values will determine the encoding (1st element will be 0 etc.). - Default {}

**Returns:**
List of processed pandas dataframes. Processed dfs will overwrite self.X_train and self.X_test.

##### choose_models

`def choose_models(self):`

**Function giving you suggested sklearn models based on prediction type and size of data. classification_type must be set during the class instantiation or using set_attributes.**

**Args:**
None

**Returns:**
List of sklearn model classes. Models saved to class instance under self.models, they will be automatically passed to
the search method.

##### oversample

`def oversample(self):`

**Function tranforming train data using undersampling and oversampling. Uses undersampling as well as oversampling if the ratio between classes is highly imbalanced. Otherwise only oversampling will be used**

**Args:**
None

**Returns:**
os_X_train, os_y_train. As matrices (as returned by SMOTE). os_X_train and os_y_train are saved to class and will be automatically applied during the search method, if oversample method is run first.

##### select_features

`def select_features(self, model=None):`

**Select best features from X_test and X_train**

**Keyword args:**
model: sklearn model - The model that will be used in sklearns SelectFromModel method Needs to
be instantiated - Default is LinearRegression if prediction_type is "regression", otherwise if prediction_type is "classification" defaults to LinearSVC()

**Returns:**
limited_X_train, limited_X_test - Also replaces self.X_test and self.X_train with the limited features.

##### search

`def search(self, scoring=None):`

**Function performing a grid search on a list of predefined models**

**Keyword Args:**
Scoring: string - scoring param as allowed by grid search cv - optional

**Returns:**
Dict containing each model, and within each model a sub dict containing the best grid search cv scores, best params, and test score.

## Examples

### Basic model training with some preprocessing

```

X, y = get_iris()
too_short = TooShort(X, y, prediction_type="classification")
result = too_short.preproc(
standard_scale=['alcohol', 'malic_acid', 'ash', 'alcalinity_of_ash', 'magnesium',
'total_phenols', 'flavanoids', 'nonflavanoid_phenols',
'proanthocyanins', 'color_intensity', 'hue',
'od280/od315_of_diluted_wines', 'proline'])

models = too_short.choose_models()
result = too_short.search()
model_keys = result.keys()
print(result)

```

#### output

```

{'SVC': {'best_score': 0.9833333333333332, 'best_params': {'C': 1, 'gamma': 0.01, 'kernel': 'rbf'}, 'test_score': 1.0}, 'RandomForestClassifier': {'best_score': 0.9833333333333332, 'best_params': {'RandomForestClassifier**bootstrap': False, 'n_estimators': 400, 'min_samples_split': 5, 'min_samples_leaf': 4, 'max_features': 'auto', 'max_depth': 32}, 'test_score': 1.0}, 'KNeighborsClassifier': {'best_score': 1.0, 'best_params': {'p': 1, 'n_neighbors': 17, 'leaf_size': 21}, 'test_score': 0.9830508474576272}, 'LinearSVC': {'best_score': 0.9833333333333332, 'best_params': {'C': 0.0001, 'dual': True}, 'test_score': 1.0}, 'LogisticRegression': {'best_score': 0.9833333333333332, 'best_params': {'LogisticRegression**class_weight': {1: 0.5, 0: 0.5}, 'LogisticRegression\_\_C': 100, 'solver': 'liblinear', 'penalty': 'l2'}, 'test_score': 1.0}}

```

---

### Choosing your own models

```

X, y = get_iris()
too_short = TooShort(X, y)
result = too_short.preproc(
standard_scale=too_short.X_train.columns)
too_short.set_attributes(models=[KNeighborsClassifier])
result = too_short.search()
print(result)

```

#### output

```

{'KNeighborsClassifier': {'best_score': 0.9833333333333332, 'best_params': {'p': 1, 'n_neighbors': 20, 'leaf_size': 14}, 'test_score': 1.0}}

```

---

### More involved preprocessing

```

X, y = get_wine()
X['A_FAKE_CAT'] = np.random.randint(4, size=len(y))
X['B_FAKE_CAT'] = np.random.randint(4, size=len(y))
X['C_FAKE_CAT'] = np.random.choice(['SWEET', 'SOUR', 'TART'], len(y))
X['D_FAKE_LABEL_CAT'] = np.random.choice(
['BAD', 'OK', 'GOOD', 'GREAT'], len(y))
X_copy = X.copy()
too_short = TooShort(X, y)
too_short.preproc(OHE=np.array(
['A_FAKE_CAT', 'B_FAKE_CAT', 'C_FAKE_CAT']),
label_encode={
'D_FAKE_LABEL_CAT': ['BAD', 'OK', 'GOOD', 'GREAT']
},
standard_scale=['alcohol', 'malic_acid', 'ash', 'alcalinity_of_ash', 'magnesium',
'total_phenols', 'flavanoids', 'nonflavanoid_phenols',
'proanthocyanins', 'color_intensity', 'hue',
'od280/od315_of_diluted_wines', 'proline'])
print(too_short.X_train.columns)

```

#### output

You new column names A_FAKE_CAT_0 etc have been one hot encoded and renamed. The final column has been label encoded (dont apply this for OHE as a first step). The other columns have been applied with the standard scalar.

```

A_FAKE_CAT_0 A_FAKE_CAT_1 A_FAKE_CAT_2 A_FAKE_CAT_3 B_FAKE_CAT_0 B_FAKE_CAT_1 ... proanthocyanins color_intensity hueod280/od315_of_diluted_wines proline D_FAKE_LABEL_CAT

```

---

### Oversampling, feature selection and customer scoring (recall)

```

df = pd.read_excel(
"https://archive.ics.uci.edu/ml/machine-learning-databases/00350/default%20of%20credit%20card%20clients.xls", encoding="utf-8", skiprows=1)
df = df.rename(
columns={'default payment next month': 'DEFAULT_PAYMENT_NEXT_MONTH', 'PAY_0': 'PAY_1'})
y = df['DEFAULT_PAYMENT_NEXT_MONTH'].ravel()
X = df.drop(['DEFAULT_PAYMENT_NEXT_MONTH'], axis=1)
too_short = TooShort(X, y, prediction_type="classification")
too_short.oversample()
too_short.preproc(standard_scale=['LIMIT_BAL', 'SEX', 'EDUCATION', 'MARRIAGE', 'AGE', 'PAY_1', 'PAY_2',
'PAY_3', 'PAY_4', 'PAY_5', 'PAY_6', 'BILL_AMT1', 'BILL_AMT2',
'BILL_AMT3', 'BILL_AMT4', 'BILL_AMT5', 'BILL_AMT6', 'PAY_AMT1',
'PAY_AMT2', 'PAY_AMT3', 'PAY_AMT4', 'PAY_AMT5', 'PAY_AMT6'])
too_short.select_features()
too_short.choose_models()
result = too_short.search(scoring="recall")

```

```

```