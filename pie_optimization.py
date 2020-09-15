# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from pyomo.environ import *

import pandas as pd
import numpy as np
from statistics import mean



model = AbstractModel()

df=pd.read_csv("raw.csv")

box_ranges=pd.read_csv("box_ranges.csv")

max_dict=df["Max"].to_dict()

cost_dict = df["Actual_cost"].to_dict()

priority_dict=df["Priority"].to_dict()

flags = pd.melt(df[["Key","Regular","Vegan","GlutenFree"]],  id_vars=["Key"], value_vars=["Regular","Vegan","GlutenFree"])

flags_dict = flags.set_index(['Key','variable'])['value'].to_dict()

swsa = pd.melt(df[["Key","Sweet", "Savory"]],  id_vars=["Key"], value_vars=["Sweet","Savory"])

swsa_dict = swsa.set_index(['Key','variable'])['value'].to_dict()

box_ranges_dict= pd.melt(box_ranges, id_vars="box", value_vars=["max","min"]).set_index(["box","variable"])["value"].to_dict()

boxes = ["Regular","Vegan","GlutenFree"]

sweet_savory = ["Sweet","Savory"]

bakers_pies=df[["Key","Bakery"]].groupby('Bakery')['Key'].apply(list).to_dict()

bakers=df["Bakery"].drop_duplicates().tolist()

bakers_mins=df[["Priority","Bakery"]].groupby("Bakery").max().to_dict()["Priority"]


baker_pie_max = df[["Bakery", "Max_pie_baker"]].drop_duplicates().groupby("Bakery").first().to_dict()["Max_pie_baker"]

data={None:
      {
       "pie_idx": {None: range(len(df))}
       ,"box_idx": {None: boxes}
      ,"swsa_idx": {None: sweet_savory}
      ,"bakers_idx":{None: bakers}
       ,"maxmin_idx":{None:["max","min"]}
       ,"cost":cost_dict
       ,"max":max_dict
       ,"flags":flags_dict
       ,"swsa":swsa_dict
       , "box_range":box_ranges_dict
       ,"priority":priority_dict
       ,"bakers_pies":bakers_pies
       ,"baker_mins": bakers_mins
       ,"baker_pie_max": baker_pie_max
       }
      }

#%%


model.pie_idx = Set()

model.box_idx = Set()

model.maxmin_idx=Set()

model.swsa_idx=Set()

model.bakers_idx=Set()




model.cost = Param(model.pie_idx, within=NonNegativeReals)
model.priority = Param(model.pie_idx, within=NonNegativeReals)
model.max = Param(model.pie_idx, within=PositiveIntegers)
model.flags = Param(model.pie_idx, model.box_idx, within=Binary)
model.swsa = Param(model.pie_idx, model.swsa_idx, within=Binary)
model.box_range = Param(model.box_idx, model.maxmin_idx, within=NonNegativeIntegers)
model.baker_mins=Param(model.bakers_idx, within=PositiveIntegers)
model.bakers_pies=Param(model.bakers_idx, within=Any)

model.baker_pie_max = Param(model.bakers_idx, within=Any)



model.pie_box=Var(model.pie_idx, model.box_idx, within=NonNegativeIntegers)

model.box = Var(model.box_idx, within=NonNegativeIntegers)



# Constraint: the total pie bought across multiple boxes is less
# than the specified max of the pie
def piemax_rule(model,i):
    return sum(model.pie_box[i,j] for j in model.box_idx) <= model.max[i]
model.piemax = Constraint(model.pie_idx,rule=piemax_rule)

# Constraint: number of pies to a box caegory is less than or equal to the number of boxes or zero if the pie is not allowed for that box
def pieboxmax_rule(model, i,j):
    return model.pie_box[i,j] <= model.box[j]*model.flags[i,j]
model.pieboxmax = Constraint(model.pie_idx,model.box_idx, rule=pieboxmax_rule )

# Constraint: specifying the range of the number of box types
def boxmax_rule(model,i):
    return model.box[i] <= model.box_range[i,"max"]
model.boxmax = Constraint(model.box_idx, rule=boxmax_rule )

def boxmin_rule(model,i):
    return model.box[i] >= model.box_range[i,"min"]
model.boxmin = Constraint(model.box_idx,rule=boxmin_rule )

# Constrain: Linking the number of pies to each box category to the number of boxes
def pieboxCoverage_rule(model, j):
    return sum(model.pie_box[i,j] for i in model.pie_idx)>=4*model.box[j]
model.pieboxCoverage = Constraint(model.box_idx, rule=pieboxCoverage_rule)

def boxsavory_rule(model,j):
    return sum(model.pie_box[i,j]*model.swsa[i, "Savory"] for i in model.pie_idx)>=model.box[j]
model.boxsavory = Constraint(model.box_idx, rule=boxsavory_rule)

## Baker specific maximums

def bakermaxs_rule(model, b):
    pies = model.bakers_pies[b]
    if model.baker_pie_max[b] == "Pie":
        return Constraint.Skip
    elif model.baker_pie_max[b]=="Baker":
        return sum(model.pie_box[p,j] for p in pies for j in model.box_idx)<= mean(model.max[p] for p in pies)
model.bakermaxs = Constraint(model.bakers_idx, rule=bakermaxs_rule)

def bakermins_rule(model,b):
    pies = model.bakers_pies[b]
    return sum(model.pie_box[i,j] for i in pies for j in model.box_idx) >= model.baker_mins[b]    
model.bakermins_rule=Constraint(model.bakers_idx, rule=bakermins_rule)


# Objective function: minimize cost of the pie * number of pies for each box
def obj_rule(model):
    return sum(model.cost[i]*model.pie_box[i,j] for i in model.pie_idx for j in model.box_idx) 
model.obj = Objective(rule=obj_rule, sense=minimize)

instance = model.create_instance(data)

# instance.pprint()

#%%

opt = SolverFactory('glpk')
opt.solve(instance, tee=True)

# instance.display()

#%%
with open('piebox.csv', 'w') as f:
    f.write('baker-pie,box,value\n')
    for (n1,n2) in instance.pie_box:
        f.write('%s,%s,%s\n' % (n1, n2, instance.pie_box[(n1,n2)].value))
        
        
results=pd.read_csv("piebox.csv")

#%%
results=results.pivot(index='baker-pie', columns='box', values='value')

#%%
raw=pd.read_csv("raw.csv")

costs=pd.concat([results.reset_index(drop=True),raw.reset_index(drop=True)], axis=1)

costs["total_pies"]=costs.iloc[:,0]+costs.iloc[:,1]+costs.iloc[:,2]

costs["total_cost"]=costs["total_pies"]*costs["Actual_cost"]

print(sum(costs["total_cost"]))
costs.to_csv("costs.csv")