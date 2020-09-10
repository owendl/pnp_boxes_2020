# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from pyomo.environ import *

import pandas as pd
import numpy as np



model = AbstractModel()

df=pd.read_csv("raw.csv")

max_dict=df["Max"].to_dict()

cost_dict = df["Actual_cost"].to_dict()

flags = pd.melt(df[["Key","Regular","Vegan","GlutenFree"]],  id_vars=["Key"], value_vars=["Regular","Vegan","GlutenFree"])

flags_dict = flags.set_index(['Key','variable'])['value'].to_dict()

boxes = ["Regular","Vegan","GlutenFree"]

data={None:
      {
       "pie_idx": {None: range(len(df))}
       ,"box_idx": {None: boxes}
       ,"cost":cost_dict
       ,"max":max_dict
       ,"flags":flags_dict
       }
      }

#%%


model.pie_idx = Set()

model.box_idx = Set()



model.cost = Param(model.pie_idx, within=NonNegativeReals)
model.max = Param(model.pie_idx, within=PositiveIntegers)


model.flags = Param(model.pie_idx, model.box_idx, within=Binary)
# model.reg_flag = Param(model.pie_idx, within=Binary)
# model.veg_flag = Param(model.pie_idx, within=Binary)
# model.glf_flag = Param(model.pie_idx, within=Binary)

model.pie_box=Var(model.pie_idx, model.box_idx, within=NonNegativeIntegers)

i = model.create_instance(data)


