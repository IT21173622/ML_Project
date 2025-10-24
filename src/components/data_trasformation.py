from data_ingestion import DataIngestion
import pandas as pd
import os
from sklearn.preprocessing import OneHotEncoder ,StandardScaler
from sklearn.compose import ColumnTransformer
import sys
from dataclasses import dataclass
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder,StandardScaler

from src.logger import logging
from src.exception import CustomException
import numpy as np

@dataclass

class DataTransformationConfig:
    preprocessor_obj_file_path: str = os.path.join('artifacts', 'preprocessor.pkl')

class DataTransformation:
    def __init__(self):
        self.DataTransformationConfig = DataTransformationConfig()

    def get_data_transformer_object(self):

        """
        this function is responsible for data transformation

        """

        try :
            logging.info("Data Transformation initiated")
            numerical_columns = ['writing score', 'reading score']
            categorical_columns = [
                "gender",
                "race_ethnicity",
                "parental_level_of_education",
                "lunch",
                "test_preparation_course",
            ]

            numerical_pipeline = Pipeline(
                steps = [
                    ('imputer',SimpleImputer(strategy='median')),
                    ('scaler',StandardScaler())

                ]
            )

            categorical_columns = Pipeline(
                steps=[
                    ('imputer',SimpleImputer(strategy='most_frequent')),
                    ('one_hot_encoder',OneHotEncoder()),
                    ('scaler',StandardScaler(with_mean=False))
                ]
            )

            logging.info(f"Categorical columns: {categorical_columns}")
            logging.info(f"Numerical columns: {numerical_columns}")

            preprocessor = ColumnTransformer(
                [
                    ('num_pipeline',numerical_pipeline,numerical_columns),
                    ('cat_pipelines',categorical_columns,categorical_columns)
                ]

            )

            return preprocessor
        
        

        except Exception as e:
            raise CustomException(e,sys)
    

    def initiate_data_transformation(self,train_path,test_path):

        try:
            train_data = pd.read_csv(train_path)

            test_data = pd.read_csv(test_path)

            logging.info("Read train and test data completed")
            logging.info("Obtaining preprocessing object")

            preprocessing_obj = self.get_data_transformer_object()

            target_column_name = "math score"
            numerical_columns = ['writing score', 'reading score']

            input_feature_train_df = train_data.drop(columns=[target_column_name],axis=1)
            target_feature_train_df = train_data[target_column_name]

            input_feature_test_df = test_data.drop(columns=[target_column_name],axis=1)
            target_feature_test_df = test_data[target_column_name]

            logging.info("Applying preprocessing object on training and testing dataframes")

            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)

            train_arry =np.c_[
                input_feature_train_arr , np.array(target_feature_train_df)
                
            ]

            test_arry = np.c_[
                input_feature_test_arr , np.array(target_feature_test_df)
            ]

            save_object(
                file_path = self.DataTransformationConfig.preprocessor_obj_file_path,
                obj = preprocessing_obj
            )

            return(
                train_arry,
                test_arry,
                self.DataTransformationConfig.preprocessor_obj_file_path
            )
            

        except Exception as e:
            raise CustomException(e,sys)    






     


       
        # Add more data transformation steps as needed

