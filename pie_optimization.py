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

priority_dict=df["Priority"].to_dict()

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
       ,"priority":priority_dict
       }
      }

#%%


model.pie_idx = Set()

model.box_idx = Set()

model.maxmin_idx=Set()

model.Pie151617_idx=Set(initialize=[15,16,17])



model.cost = Param(model.pie_idx, within=NonNegativeReals)
model.priority = Param(model.pie_idx, within=NonNegativeReals)
model.max = Param(model.pie_idx, within=PositiveIntegers)
model.flags = Param(model.pie_idx, model.box_idx, within=Binary)
model.box_range = Param(model.box_idx, model.maxmin_idx, within=NonNegativeIntegers)



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

## Baker specific maximums

# Constrain baker total max
def totalPie01_rule(model):
    return sum(model.pie_box[i,j] for i in [0,1] for j in model.box_idx)<= model.max[0]
model.totalPie01 = Constraint(rule=totalPie01_rule )

# #Constrain baker total max
def totalPie2345_rule(model):
    return sum(model.pie_box[i,j] for i in [2,3,4,5] for j in model.box_idx)<= model.max[2]
model.totalPie2345 = Constraint(rule=totalPie2345_rule )

# #Constrain baker total max
def totalPie789_rule(model):
    return sum(model.pie_box[i,j] for i in [7,8,9] for j in model.box_idx)<= model.max[7]
model.totalPie789 = Constraint(rule=totalPie789_rule )

#Constrain baker total max
def totalPie141516_rule(model):
    return sum(model.pie_box[i,j] for i in [15,16,14] for j in model.box_idx)<= model.max[15]
model.totalPie141516 = Constraint(rule=totalPie141516_rule )

# #Constrain baker total max
def totalPie1718_rule(model):
    return sum(model.pie_box[i,j] for i in [18,17] for j in model.box_idx)<= model.max[18]
model.totalPie1718 = Constraint(rule=totalPie1718_rule )

# #Constrain baker total max
def totalPie1920_rule(model):
    return sum(model.pie_box[i,j] for i in [19,20] for j in model.box_idx)<= model.max[20]
model.totalPie1920 = Constraint(rule=totalPie1920_rule )

# #Constrain baker total max
def totalPie212223_rule(model):
    return sum(model.pie_box[i,j] for i in [22,23,21] for j in model.box_idx)<= model.max[22]
model.totalPie212223 = Constraint(rule=totalPie212223_rule )

# #Constrain baker total max
def totalPie2526_rule(model):
    return sum(model.pie_box[i,j] for i in [25,26] for j in model.box_idx)<= model.max[26]
model.totalPie2526 = Constraint(rule=totalPie2526_rule )

# #Constrain baker total max
def totalPie2829_rule(model):
    return sum(model.pie_box[i,j] for i in [28,29] for j in model.box_idx)<= model.max[28]
model.totalPie2829 = Constraint(rule=totalPie2829_rule )

# #Constrain baker total max
def totalPie3031_rule(model):
    return sum(model.pie_box[i,j] for i in [30,31] for j in model.box_idx)<= model.max[30]
model.totalPie3031 = Constraint(rule=totalPie3031_rule )

# #Constrain baker total max
def totalPie3536_rule(model):
    return sum(model.pie_box[i,j] for i in [35,36] for j in model.box_idx)<= model.max[35]
model.totalPie3536 = Constraint(rule=totalPie3536_rule )

## Baker specific minimums

# #Constrain baker total min
def totalPie2345priority_rule(model):
    return sum(model.pie_box[i,j] for i in [2,3,4,5] for j in model.box_idx)>= model.priority[2]
model.totalPie2345priority = Constraint(rule=totalPie2345priority_rule )

# #Constrain baker total min
def totalPie789priority_rule(model):
    return sum(model.pie_box[i,j] for i in [7,8,9] for j in model.box_idx)>= model.priority[7]
model.totalPie789priority = Constraint(rule=totalPie789priority_rule )

# #Constrain baker total min
def totalPie111213priority_rule(model):
    return sum(model.pie_box[i,j] for i in [11,12,13] for j in model.box_idx)>= model.priority[11]
model.totalPie111213priority = Constraint(rule=totalPie111213priority_rule )

# #Constrain baker total min
def totalPie1920priority_rule(model):
    return sum(model.pie_box[i,j] for i in [19,20] for j in model.box_idx)>= model.priority[19]
model.totalPie1920priority = Constraint(rule=totalPie1920priority_rule )

# #Constrain baker total min
def totalPie24priority_rule(model):
    return sum(model.pie_box[i,j] for i in [24] for j in model.box_idx)>= model.priority[24]
model.totalPie24priority = Constraint(rule=totalPie24priority_rule )

# #Constrain baker total min
# def totalPie3435priority_rule(model):
    # return sum(model.pie_box[i,j] for i in [34,35] for j in model.box_idx)>= model.priority[34]
# model.totalPie3435priority = Constraint(rule=totalPie3435priority_rule )

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