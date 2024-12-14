from pandas import DataFrame
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.neural_network import MLPRegressor

df:DataFrame | None = None
temp_df:DataFrame | None = None
sklearn_model: GradientBoostingRegressor | None = None
sklearn_param:dict = dict()

mlp_model: MLPRegressor | None = None
mlp_param:dict = dict()