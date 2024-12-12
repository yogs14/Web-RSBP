from pandas import DataFrame
from sklearn.ensemble import GradientBoostingRegressor

df:DataFrame | None = None
temp_df:DataFrame | None = None
sklearn_model: GradientBoostingRegressor | None = None
sklearn_param:dict = dict()