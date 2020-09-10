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

box_ranges=pd.read_csv("box_ranges.csv")

max_dict=df["Max"].to_dict()

cost_dict = df["Actual_cost"].to_dict()

flags = pd.melt(df[["Key","Regular","Vegan","GlutenFree"]],  id_vars=["Key"], value_vars=["Regular","Vegan","GlutenFree"])

flags_dict = flags.set_index(['Key','variable'])['value'].to_dict()

box_ranges_dict= pd.melt(box_ranges, id_vars="box", value_vars=["max","min"]).set_index(["box","variable"])["value"].to_dict()

boxes = ["Regular","Vegan","GlutenFree"]


data={None:
      {
       "pie_idx": {None: range(len(df))}
       ,"box_idx": {None: boxes}
       ,"maxmin_idx":{None:["max","min"]}
       ,"cost":cost_dict
       ,"max":max_dict
       ,"flags":flags_dict
       , "box_range":box_ranges_dict
       }
      }

#%%


model.pie_idx = Set()

model.box_idx = Set()

model.maxmin_idx=Set()



model.cost = Param(model.pie_idx, within=NonNegativeReals)
model.max = Param(model.pie_idx, within=PositiveIntegers)
model.flags = Param(model.pie_idx, model.box_idx, within=Binary)
model.box_range = Param(model.box_idx, model.maxmin_idx, within=NonNegativeIntegers)



model.pie_box=Var(model.pie_idx, model.box_idx, within=NonNegativeIntegers)

model.box = Var(model.box_idx, within=NonNegativeIntegers)

i = model.create_instance(data)
i.pprint()


# Constraint: the total pie bought across multiple boxes is less
# than the specified max of the pie
def piemax_rule(model, i,j):
    return sum(model.pie_box[i,j] for j in model.box_idx) <= model.max[i]
model.piemax = Constraint( rule=piemax_rule )

# Constraint: number of pies to a box is less than or equal to the number of boxes or zero if the pie is not allowed for that box
def pieboxmax_rule(model, i,j):
    return model.pie_box[i,j] <= model.box_range[j,"max"]*model.flags[i,j]
model.pieboxmax = Constraint( rule=pieboxmax_rule )

def boxmax_rule(model):
    return model.box[i] <= model.box_range[i,"max"]
model.boxmax = Constraint( rule=boxmax_rule )

def boxmin_rule(model):
    return model.box[i] >= model.box_range[i,"min"]
model.boxmin = Constraint( rule=boxmin_rule )

