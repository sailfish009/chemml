import warnings
import pandas as pd
import numpy as np
import sklearn
import copy

from ..base import BASE, LIBRARY
from .syntax import Preprocessor, Regressor, Evaluator


#####################################################################DataRepresentation

class PolynomialFeatures(BASE,Preprocessor):
    def legal_IO(self):
        self.legal_inputs = {'df': None}
        self.legal_outputs = {'api':None, 'df':None}
        self.Base.requirements.append('scikit_learn', 'pandas')

    def fit(self):
        from sklearn.preprocessing import PolynomialFeatures
        # check inputs
        if self.legal_inputs['df'] == None:
            msg = '@Task #%i(%s): input data frame is required'%(self.iblock,self.SuperFunction)
            raise IOError(msg)
        try:
            model = PolynomialFeatures(**self.parameters)
        except Exception as err:
            msg = '@Task #%i(%s): '%(self.iblock+1, self.SuperFunction) + type(err).__name__ + ': '+ err.message
            raise TypeError(msg)
        order = [edge[1] for edge in self.Base.graph if edge[0]==self.iblock]
        for token in order:
            if token == 'api':
                self.legal_outputs[token] = model
            elif token == 'df':
                self.legal_outputs[token] = self.Transformer_ManipulateHeader(model, self.legal_inputs['df'])
            else:
                msg = "@Task #%i(%s): non valid output token '%s'" % (self.iblock, self.SuperFunction, token)
                raise NameError(msg)

#####################################################################Preprocessor

class Imputer(BASE,Preprocessor):
    def legal_IO(self):
        self.legal_inputs = {'df': None}
        self.legal_outputs = {'api':None, 'df':None}
        requirements = ['scikit_learn']
        self.Base.requirements += [i for i in requirements if i not in self.Base.requirements]

    def fit(self):
        from sklearn.preprocessing import Imputer
        cheml_type = "%s_%s" % (self.Base.graph_info[self.iblock][0], self.Base.graph_info[self.iblock][1])
        self.Base.cheml_type['preprocessor'].append(cheml_type)
        try:
            model = Imputer(**self.parameters)
        except Exception as err:
            msg = '@Task #%i(%s): '%(self.iblock+1, self.SuperFunction) + type(err).__name__ + ': '+ err.message
            raise TypeError(msg)
        # Send

        if not isinstance(self.legal_inputs['df'],type(None)):
            df = self.legal_inputs['df'][0]
            model, df = self.Imputer_ManipulateHeader(model, df)

        order = [edge[1] for edge in self.Base.graph if edge[0]==self.iblock]
        for token in set(order):
            if token == 'api':
                val = model
                self.Base.send[(self.iblock, token)] = [val, order.count(token)]
            elif token == 'df':
                if not isinstance(self.legal_inputs['df'], type(None)):
                    self.Base.send[(self.iblock, token)] = [df, order.count(token)]
            else:
                msg = "@Task #%i(%s): non valid output token '%s'" % (self.iblock+1, self.SuperFunction, token)
                raise NameError(msg)
        del self.legal_inputs

class StandardScaler(BASE,LIBRARY):
    def legal_IO(self):
        self.legal_inputs = {'df': None, 'api': None}
        self.legal_outputs = {'api':None, 'df':None}
        requirements = ['scikit_learn']
        self.Base.requirements += [i for i in requirements if i not in self.Base.requirements]

    def fit(self):
        # step1: check inputs
        df, df_info = self.input_check('df', req=True, py_type=pd.DataFrame)
        model, _ = self.input_check('api', req=False)

        # step2: assign inputs to parameters if necessary (param = @token)
        self.paramFROMinput()

        # step3: check the dimension of input data frame
        # df, _ = self.data_check('df', df, ndim=2, n0=None, n1=None, format_out='df')

        # step4: import module and make APIs
        method = self.parameters.pop('method')  # method = transform or inverse
        if isinstance(self.legal_inputs['api'], type(None)):
            if method == 'fit_transform':
                try:
                    from sklearn.preprocessing import StandardScaler
                    model = StandardScaler(**self.parameters)
                except Exception as err:
                    msg = '@Task #%i(%s): '%(self.iblock+1, self.SuperFunction) + type(err).__name__ + ': '+ err.message
                    raise TypeError(msg)
            else:
                msg = "@Task #%i(%s): pass an api to transform or inverse_transform the input data, otherwise you need to fit_transform the data with proper parameters." % (self.iblock, self.SuperFunction)
                raise NameError(msg)
        else:



        # step5: process
        self.scaler(model,df,method)

        # step6: send out
        order = [edge[1] for edge in self.Base.graph if edge[0]==self.iblock]
        for token in set(order):
            if token == 'api':
                val = model
                self.Base.send[(self.iblock, token)] = [val, order.count(token),(self.iblock,token,self.Host,self.Function)]
            elif token == 'df':
                if not isinstance(self.legal_inputs['df'], type(None)):
                    self.Base.send[(self.iblock, token)] = [df, order.count(token),(self.iblock,token,self.Host,self.Function)]
                else:
                    msg = "@Task #%i(%s): received no data to send out" % (
                    self.iblock, self.SuperFunction)
                    raise NameError(msg)
            else:
                msg = "@Task #%i(%s): non valid output token '%s'" % (self.iblock, self.SuperFunction, token)
                raise NameError(msg)

        # step7: delete all inputs from memory
        del self.legal_inputs

class Normalizer(BASE,Preprocessor):
    def legal_IO(self):
        self.legal_inputs = {'df': None}
        self.legal_outputs = {'api':None, 'df':None}
        requirements = ['scikit_learn']
        self.Base.requirements += [i for i in requirements if i not in self.Base.requirements]

    def fit(self):
        from sklearn.preprocessing import Normalizer
        cheml_type = "%s_%s" % (self.Base.graph_info[self.iblock][0], self.Base.graph_info[self.iblock][1])
        self.Base.cheml_type['preprocessor'].append(cheml_type)
        try:
            model = Normalizer(**self.parameters)
        except Exception as err:
            msg = '@Task #%i(%s): '%(self.iblock+1, self.SuperFunction) + type(err).__name__ + ': '+ err.message
            raise TypeError(msg)

        if not isinstance(self.legal_inputs['df'],type(None)):
            df = self.legal_inputs['df'][0]
            model, df = self.Transformer_ManipulateHeader(model, df)

        order = [edge[1] for edge in self.Base.graph if edge[0]==self.iblock]
        for token in set(order):
            if token == 'api':
                val = model
                self.Base.send[(self.iblock, token)] = [val, order.count(token)]
            elif token == 'df':
                if not isinstance(self.legal_inputs['df'], type(None)):
                    self.Base.send[(self.iblock, token)] = [df, order.count(token)]
            else:
                msg = "@Task #%i(%s): non valid output token '%s'" % (self.iblock+1, self.SuperFunction, token)
                raise NameError(msg)
        del self.legal_inputs

class Binarizer(BASE,Preprocessor):
    def legal_IO(self):
        self.legal_inputs = {'df': None}
        self.legal_outputs = {'api':None, 'df':None}
        requirements = ['scikit_learn']
        self.Base.requirements += [i for i in requirements if i not in self.Base.requirements]

    def fit(self):
        from sklearn.preprocessing import Binarizer
        cheml_type = "%s_%s" % (self.Base.graph_info[self.iblock][0], self.Base.graph_info[self.iblock][1])
        self.Base.cheml_type['preprocessor'].append(cheml_type)
        try:
            model = Binarizer(**self.parameters)
        except Exception as err:
            msg = '@Task #%i(%s): '%(self.iblock+1, self.SuperFunction) + type(err).__name__ + ': '+ err.message
            raise TypeError(msg)

        if not isinstance(self.legal_inputs['df'],type(None)):
            df = self.legal_inputs['df'][0]
            model, df = self.Transformer_ManipulateHeader(model, df)

        order = [edge[1] for edge in self.Base.graph if edge[0]==self.iblock]
        for token in set(order):
            if token == 'api':
                val = model
                self.Base.send[(self.iblock, token)] = [val, order.count(token)]
            elif token == 'df':
                if not isinstance(self.legal_inputs['df'], type(None)):
                    self.Base.send[(self.iblock, token)] = [df, order.count(token)]
            else:
                msg = "@Task #%i(%s): non valid output token '%s'" % (self.iblock+1, self.SuperFunction, token)
                raise NameError(msg)
        del self.legal_inputs

class OneHotEncoder(BASE,Preprocessor):
    def legal_IO(self):
        self.legal_inputs = {'df': None}
        self.legal_outputs = {'api':None, 'df':None}
        requirements = ['scikit_learn']
        self.Base.requirements += [i for i in requirements if i not in self.Base.requirements]

    def fit(self):
        from sklearn.preprocessing import OneHotEncoder
        cheml_type = "%s_%s" % (self.Base.graph_info[self.iblock][0], self.Base.graph_info[self.iblock][1])
        self.Base.cheml_type['preprocessor'].append(cheml_type)
        try:
            model = OneHotEncoder(**self.parameters)
        except Exception as err:
            msg = '@Task #%i(%s): '%(self.iblock+1, self.SuperFunction) + type(err).__name__ + ': '+ err.message
            raise TypeError(msg)

        if not isinstance(self.legal_inputs['df'],type(None)):
            df = self.legal_inputs['df'][0]
            model, df = self.Transformer_ManipulateHeader(model, df)

        order = [edge[1] for edge in self.Base.graph if edge[0]==self.iblock]
        for token in set(order):
            if token == 'api':
                val = model
                self.Base.send[(self.iblock, token)] = [val, order.count(token)]
            elif token == 'df':
                if not isinstance(self.legal_inputs['df'], type(None)):
                    self.Base.send[(self.iblock, token)] = [df, order.count(token)]
            else:
                msg = "@Task #%i(%s): non valid output token '%s'" % (self.iblock+1, self.SuperFunction, token)
                raise NameError(msg)
        del self.legal_inputs

#####################################################################FeatureSelection



#####################################################################FeatureTransformation

class PCA(BASE):
    def legal_IO(self):
        self.legal_inputs = {'df': None}
        self.legal_outputs = {'api':None, 'df':None}
        requirements = ['scikit_learn']
        self.Base.requirements += [i for i in requirements if i not in self.Base.requirements]

    def fit(self):
        from sklearn.decomposition import PCA
        cheml_type = "%s_%s" % (self.Base.graph_info[self.iblock][0], self.Base.graph_info[self.iblock][1])
        self.Base.cheml_type['transformer'].append(cheml_type)
        try:
            model = PCA(**self.parameters)
        except Exception as err:
            msg = '@Task #%i(%s): '%(self.iblock+1, self.SuperFunction) + type(err).__name__ + ': '+ err.message
            raise TypeError(msg)
        order = [edge[1] for edge in self.Base.graph if edge[0]==self.iblock]
        for token in set(order):
            if token == 'api':
                val = model
                self.Base.send[(self.iblock, token)] = [val, order.count(token)]
            elif token == 'df':
                val = pd.DataFrame(model.fit_transform(self.legal_inputs['df'][0]))
                self.Base.send[(self.iblock, token)] = [val, order.count(token)]
            else:
                msg = "@Task #%i(%s): non valid output token '%s'" % (self.iblock+1, self.SuperFunction, token)
                raise NameError(msg)
        del self.legal_inputs

#####################################################################Divider

class Train_Test_Split(BASE, LIBRARY):
    def legal_IO(self):
        self.legal_inputs = {'dfx': None, 'dfy': None}
        self.legal_outputs = {'dfx_train': None, 'dfx_test': None, 'dfy_train': None, 'dfy_test': None}
        requirements = ['scikit_learn']
        self.Base.requirements += [i for i in requirements if i not in self.Base.requirements]

    def fit(self):
        # step1: check inputs
        dfx, dfx_info = self.input_check('dfx', req=True, py_type=pd.DataFrame)
        dfy, dfy_info = self.input_check('dfy', req=False, py_type=pd.DataFrame)

        # step2: assign inputs to parameters if necessary (param = @token)
        self.paramFROMinput()

        # step3: check the dimension of input data frame
        dfx, _ = self.data_check('dfx', dfx, ndim=2, n0=None, n1=None, format_out='df')

        # step4: import module and make APIs
        try:
            from sklearn.model_selection import train_test_split
            if dfy is None:
                tts_out = train_test_split(dfx,**self.parameters)
            else:
                dfy, _ = self.data_check('dfy', dfy, ndim=1, n0=dfx.shape[0], n1=None, format_out='df')
                tts_out = train_test_split(dfx,dfy, **self.parameters)
        except Exception as err:
            msg = '@Task #%i(%s): '%(self.iblock+1, self.SuperFunction) + type(err).__name__ + ': '+ err.message
            raise TypeError(msg)

        # step5: process
        # step6: send out
        order = [edge[1] for edge in self.Base.graph if edge[0]==self.iblock]
        for token in set(order):
            if token == 'dfx_train':
                self.Base.send[(self.iblock, token)] = [tts_out[0], order.count(token)]
            elif token == 'dfx_test':
                self.Base.send[(self.iblock, token)] = [tts_out[1], order.count(token)]
            elif token == 'dfy_train':
                self.Base.send[(self.iblock, token)] = [tts_out[2], order.count(token)]
            elif token == 'dfy_test':
                self.Base.send[(self.iblock, token)] = [tts_out[3], order.count(token)]
            else:
                msg = "@Task #%i(%s): non valid output token '%s'" % (self.iblock+1, self.SuperFunction, token)
                raise NameError(msg)

        # step7: delete all inputs from memory
        del self.legal_inputs

class KFold(BASE):
    def legal_IO(self):
        self.legal_inputs = {}
        self.legal_outputs = {'CV': None}
        requirements = ['scikit_learn']
        self.Base.requirements += [i for i in requirements if i not in self.Base.requirements]

    def fit(self):
        from sklearn.model_selection import KFold
        cheml_type = "%s_%s" % (self.Base.graph_info[self.iblock][0], self.Base.graph_info[self.iblock][1])
        self.Base.cheml_type['transformer'].append(cheml_type)
        try:
            model = KFold(**self.parameters)
        except Exception as err:
            msg = '@Task #%i(%s): ' % (self.iblock + 1, self.SuperFunction) + type(
                err).__name__ + ': ' + err.message
            raise TypeError(msg)
        order = [edge[1] for edge in self.Base.graph if edge[0] == self.iblock]
        for token in set(order):
            if token == 'CV':
                self.Base.send[(self.iblock, token)] = [model, order.count(token)]
            else:
                msg = "@Task #%i(%s): non valid output token '%s'" % (self.iblock + 1, self.SuperFunction, token)
                raise NameError(msg)
        del self.legal_inputs

#####################################################################Regression

class regression(BASE, LIBRARY):
    def legal_IO(self):
        self.legal_inputs = {}
        self.legal_outputs = {'api': None}
        requirements = ['scikit_learn']
        self.Base.requirements += [i for i in requirements if i not in self.Base.requirements]

    def fit(self):
        # step1: check inputs
        # step2: assign inputs to parameters if necessary (param = @token)
        # step3: check the dimension of input data frame
        # step4: import module and make APIs
        try:
            if self.Function == 'OLS':
                from sklearn.linear_model import LinearRegression
                model = LinearRegression(**self.parameters)
            elif self.Function == 'Ridge':
                from sklearn.linear_model import Ridge
                model = Ridge(**self.parameters)
            elif self.Function == 'KernelRidge':
                from sklearn.kernel_ridge import KernelRidge
                model = KernelRidge(**self.parameters)
            elif self.Function == 'Lasso':
                from sklearn.linear_model import Lasso
                model = Lasso(**self.parameters)
            elif self.Function == 'MultiTaskLasso':
                from sklearn.linear_model import MultiTaskLasso
                model = MultiTaskLasso(**self.parameters)
            elif self.Function == 'ElasticNet':
                from sklearn.kernel_ridge import ElasticNet
                model = ElasticNet(**self.parameters)
            elif self.Function == 'MultiTaskElasticNet':
                from sklearn.linear_model import MultiTaskElasticNet
                model = MultiTaskElasticNet(**self.parameters)
            elif self.Function == 'Lars':
                from sklearn.linear_model import Lars
                model = Lars(**self.parameters)
            elif self.Function == 'LassoLars':
                from sklearn.kernel_ridge import LassoLars
                model = LassoLars(**self.parameters)
            elif self.Function == 'BayesianRidge':
                from sklearn.linear_model import BayesianRidge
                model = BayesianRidge(**self.parameters)
            elif self.Function == 'ARDRegression':
                from sklearn.linear_model import ARDRegression
                model = ARDRegression(**self.parameters)
            elif self.Function == 'LogisticRegression':
                from sklearn.kernel_ridge import LogisticRegression
                model = LogisticRegression(**self.parameters)
            elif self.Function == 'SGDRegressor':
                from sklearn.linear_model import SGDRegressor
                model = SGDRegressor(**self.parameters)
            elif self.Function == 'SVR':
                from sklearn.svm import SVR
                model = SVR(**self.parameters)
            elif self.Function == 'NuSVR':
                from sklearn.svm import NuSVR
                model = NuSVR(**self.parameters)
            elif self.Function == 'LinearSVR':
                from sklearn.svm import LinearSVR
                model = LinearSVR(**self.parameters)
            elif self.Function == 'MLPRegressor':
                from sklearn.neural_network import MLPRegressor
                model = MLPRegressor(**self.parameters)
            else:
                msg = "@Task #%i(%s): function name '%s' in module '%s' is not available/valid regression method" % (self.iblock, self.SuperFunction,self.Function, 'sklearn')
                raise NameError(msg)
        except Exception as err:
            msg = '@Task #%i(%s): '%(self.iblock+1, self.SuperFunction) + type(err).__name__ + ': '+ err.message
            raise TypeError(msg)

        # step5: process
        # step6: send out
        order = [edge[1] for edge in self.Base.graph if edge[0] == self.iblock]
        for token in set(order):
            if token == 'api':
                self.Base.send[(self.iblock, token)] = [model, order.count(token)]
            # elif token == 'r2_train':
            #     if not isinstance(dfx, type(None)) and not isinstance(dfy, type(None)):
            #         # step3: check the dimension of input data frame
            #         dfx, _ = self.data_check('dfx', dfx, ndim=2, n0=None, n1=None, format_out='df')
            #         dfy, _ = self.data_check('dfy', dfy, ndim=1, n0=dfx.shape[0], n1=None, format_out='df')
            #
            #         model.fit(dfx,dfy)
            #         r2score_training = model.score(dfx, dfy)
            #     else:
            #         msg = "@Task #%i(%s): training needs both dfx and dfy" % (self.iblock + 1, self.SuperFunction)
            #         raise NameError(msg)
            #     self.Base.send[(self.iblock, token)] = [r2score_training, order.count(token)]
            else:
                msg = "@Task #%i(%s): non valid output token '%s'" % (self.iblock + 1, self.SuperFunction, token)
                raise NameError(msg)
        #step7: delete all inputs from memory
        del self.legal_inputs

#####################################################################Postprocessor

class GridSearchCV(BASE, LIBRARY):
    def legal_IO(self):
        self.legal_inputs = {'dfx': None, 'dfy': None, 'estimator': None}
        self.legal_outputs = {'cv_results_': None, 'api': None, 'best_estimator_': None}
        requirements = ['scikit_learn']
        self.Base.requirements += [i for i in requirements if i not in self.Base.requirements]

    def fit(self):
        # step1: check inputs
        _, _ = self.input_check('estimator', req = True)
        dfx, dfx_info = self.input_check('dfx', req = True, py_type = pd.DataFrame)
        dfy, dfy_info = self.input_check('dfy', req = True, py_type = pd.DataFrame)

        # step2: assign inputs to parameters if necessary (param = @token)
        self.paramFROMinput()

        # step3: check the dimension of input data frame
        dfx, _ = self.data_check('dfx', dfx, ndim=2, n0=None, n1=None, format_out='df')
        dfy, _ = self.data_check('dfy', dfy, ndim=1, n0=dfx.shape[0], n1=None, format_out='df')

        # step4: import module and make APIs
        try:
            from sklearn.model_selection import GridSearchCV
            api = GridSearchCV(**self.parameters)
        except Exception as err:
            msg = '@Task #%i(%s): '%(self.iblock+1, self.SuperFunction) + type(err).__name__ + ': '+ err.message
            raise TypeError(msg)

        # step5: process
        api.fit(dfx, dfy)

        # step6: send out
        order = [edge[1] for edge in self.Base.graph if edge[0]==self.iblock]
        for token in set(order):
            if token == 'best_estimator_':
                if self.parameters['refit']==True:
                    best_estimator_ = copy.deepcopy(api.best_estimator_)
                else:
                    best_estimator_ = copy.deepcopy(self.parameters['estimator'])
                    best_estimator_.set_params(**api.best_params_)
                    # best_estimator_.fit(dfx,dfy)
                self.Base.send[(self.iblock, token)] = [best_estimator_, order.count(token)]
            elif token == 'cv_results_':
                self.Base.send[(self.iblock, token)] = [pd.DataFrame(api.cv_results_), order.count(token)]
            elif token == 'api':
                self.Base.send[(self.iblock, token)] = [api, order.count(token)]
            else:
                msg = "@Task #%i(%s): non valid output token '%s'" % (self.iblock+1, self.SuperFunction, token)
                raise NameError(msg)

        #step7: delete all inputs from memory
        del self.legal_inputs

class Evaluation(BASE, Regressor, Evaluator):
    def legal_IO(self):
        self.legal_inputs = {'dfx': None, 'dfy': None, 'CV': None, 'X_scaler': None, 'Y_scaler': None, 'model': None}
        self.legal_outputs = {'results': None}
        requirements = ['scikit_learn']
        self.Base.requirements += [i for i in requirements if i not in self.Base.requirements]

    def scenario1(self, dfx_test, dfy_test):
        # 0 CV
        if self.X_scaler is not None:
            dfx_test = self.X_scaler.transform(dfx_test)
        if len(dfy_test.columns)==1:
            col = dfy_test.columns[0]
            dfy_test = np.array(dfy_test[col])
        self.dfy_pred = self.predict(self.legal_inputs['model'], dfx_test)
        if self.Y_scaler is not None:
            self.dfy_pred = self.Y_scaler.inverse_transform(self.dfy_pred)
        self.evaluate(dfy_test, self.dfy_pred)

    def scenario2(self, dfx, dfy):
        # 1 CV
        self.model_info = {'r2_training':[], 'models':[], 'X_scaler':[], 'Y_scaler':[]}
        for train, test in self.CV.split(dfx):
            dfx_train = dfx.iloc[train]
            dfy_train = dfy.iloc[train]
            if dfy_train.shape[1]==1:
                flag = True
            else:
                flag = False
            dfx_test = dfx.iloc[test]
            dfy_test = dfy.iloc[test]
            if not isinstance(self.X_scaler, type(None)):
                dfx_train = self.X_scaler.fit_transform(dfx_train)
                dfx_test = self.X_scaler.transform(dfx_test)
                self.model_info['X_scaler'].append(self.X_scaler)
            if not isinstance(self.Y_scaler, type(None)):
                dfy_train = self.Y_scaler.fit_transform(dfy_train)
                self.model_info['Y_scaler'].append(self.Y_scaler)
                print dfy_train.shape
            if flag:
                dfy_train = np.ravel(dfy_train)
            model, r2 = self.train(self.legal_inputs['model'], dfx_train, dfy_train)
            self.model_info['models'].append(model)
            self.model_info['r2_training'].append(r2)
            dfy_pred = self.predict(self.legal_inputs['model'], dfx_test)
            if not isinstance(self.Y_scaler, type(None)):
                dfy_pred = self.Y_scaler.inverse_transform(dfy_pred)
            self.evaluate(dfy_test, dfy_pred)

    def fit(self):
        #Todo: add a function to read the model from file
        dfx = self.type_check('dfx', cheml_type='df', req=True, py_type=pd.DataFrame)
        dfy = self.type_check('dfy', cheml_type='df', req=True, py_type=pd.DataFrame)
        model = self.type_check('model', cheml_type='model', req=True)
        self.X_scaler = self.type_check('X_scaler', cheml_type='preprocessor', req=False)
        self.Y_scaler = self.type_check('Y_scaler', cheml_type='preprocessor', req=False)
        self.CV = self.type_check('CV', cheml_type='cv', req=False)

        self._evaluation_params()
        # Todo: check if we can have one sent variable for two inputs
        if self.CV is None:
            self.scenario1(dfx, dfy)
        else:
            self.scenario2(dfx, dfy)
        del dfx
        del dfy

        order = [edge[1] for edge in self.Base.graph if edge[0]==self.iblock]
        for token in set(order):
            if token == 'results':
                self.Base.send[(self.iblock, token)] = [pd.DataFrame(self.results), order.count(token)]
            else:
                msg = "@Task #%i(%s): non valid output token '%s'" % (self.iblock+1, self.SuperFunction, token)
                raise NameError(msg)
        del self.legal_inputs

class Evaluate_static(BASE,LIBRARY,Evaluator):
    def legal_IO(self):
        self.legal_inputs = {'dfy': None, 'dfy_pred': None}
        self.legal_outputs = {'evaluation_results_': None}
        requirements = ['scikit_learn']
        self.Base.requirements += [i for i in requirements if i not in self.Base.requirements]

    def fit(self):
        # step1: check inputs
        dfy, dfy_info = self.input_check('dfy', req = True, py_type = pd.DataFrame)
        dfy_pred, dfy_pred_info = self.input_check('dfy_pred', req = True, py_type = pd.DataFrame)

        # step2: assign inputs to parameters if necessary (param = @token)
        self.paramFROMinput()

        # step3: check the dimension of input data frame
        dfy, _ = self.data_check('dfy', dfy, ndim=2, n0=None, n1=None, format_out='df')
        dfy_pred, _ = self.data_check('dfy_pred', dfy_pred, ndim=2, n0=dfy.shape[0], n1=None, format_out='df')

        # step4: import module and make APIs
        try:
            self._evaluation_params()
            self.evaluate(dfy,dfy_pred)
        except Exception as err:
            msg = '@Task #%i(%s): '%(self.iblock+1, self.SuperFunction) + type(err).__name__ + ': '+ err.message
            raise TypeError(msg)

        # step5: process
        # step6: send out
        order = [edge[1] for edge in self.Base.graph if edge[0]==self.iblock]
        for token in set(order):
            if token == 'evaluation_results_':
                evaluation_results_ = self.results
                self.Base.send[(self.iblock, token)] = [pd.DataFrame(evaluation_results_), order.count(token)]
            else:
                msg = "@Task #%i(%s): non valid output token '%s'" % (self.iblock+1, self.SuperFunction, token)
                raise NameError(msg)

        #step7: delete all inputs from memory
        del self.legal_inputs