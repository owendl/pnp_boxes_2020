# Porches and Pies Box Optimization

Due to the City of Atlanta regulations in response to covid-19, my neighborhood association's Events Committee decided to convert our neighborhood pie bake-off and festival into a box of hand pies and other goodies. This would allow us to drive some business to local businesses and doing something for our neighborhood (donating some boxes to local senior residents). This event also acts as the sole revenue generator for our association, that allows us to do more events in our community.

We reached out to local bakers and generated of available pies, quantity and costs. Which led to the natural question of what pies to purchase given our budget constraints and the goal to make each box of pies as economical as possible. This sounds like a natural optimization problem. 

## Framing the problem: Math
### Objective
The goal of the problem is to create a three kinds of boxes (gluten free, vegan, no conditions which we called regular) that contain 4 hand pies from our vendors for the minimum cost possible (<img src="https://render.githubusercontent.com/render/math?math=c_i">, the cost for us to purchase the pie $i$). We have labeled each pie from each baker as falling into one or more of those categories. Thus, a particular pie could be used in multiple types of boxes. To account for this for each pie, I created a variable <img src="https://render.githubusercontent.com/render/math?math=Q_{i,j}">, where i is a particular pie from a particular baker and j is the box category, denoting the number of the pies needed for the j type box. This makes the objective function:<img src="https://render.githubusercontent.com/render/math?math=min\sum_{j \in J}\sum_{i \in I}c_iQ_{i,j}"> 

### Baker and pie capacity
Put simply, we can't ask for more pies from a baker than they can supply. However, some bakers gave us their maximum capacity on a per pie basis (i) and some gave us total maximum capacity across all their pies (ii). Thus there are two different versions of this constraint. The first (i)
<img src="https://render.githubusercontent.com/render/math?math=\sum_{j \in J}Q_{i,j}<=max_i">
where <img src="https://render.githubusercontent.com/render/math?math=max_i"> is the maximum capacity for that pie.
<img src="https://render.githubusercontent.com/render/math?math=\sum_{i \in baker}\sum_{j \in J}Q_{i,j}<=max_{baker}">
where <img src="https://render.githubusercontent.com/render/math?math=i \in baker"> is the set of all pies for a particular baker.

### Box type constraint and no repeated pies
To provide variety for each box, we wanted no box to have more than one pie. This led to a contraint
<img src="https://render.githubusercontent.com/render/math?math=Q_{i,j}<=Q_jF_{i,j}">
where <img src="https://render.githubusercontent.com/render/math?math=Q_j"> is the total number of boxes of type j and <img src="https://render.githubusercontent.com/render/math?math=F_{i,j}"> is 1 if pie i is eligible for box j and 0 if it is not. This constraint also controls that pies are not placed in boxes that they are not eligible for.

### Box ranges
Even though we are seeking to minimize cost, which is correlated with the number of pies ordered, I set box range quantities for each type of box to provide more flexibility for the solver.
<img src="https://render.githubusercontent.com/render/math?math=min_j<=Q_j<=max_j">

### Box coverage
Each box must contain at least 4 pies of the appropriate type of pies. 
<img src="https://render.githubusercontent.com/render/math?math=\sum_{i \in I}Q_{i,j}>=4Q_j">

## Implementing the Solution: Coding

I took this opportunity to teach myself [pyomo](http://www.pyomo.org), an open-source optimization package/framework. I had previous experience with [cvxpy](https://www.cvxpy.org) but it is limited to convex optimization problems. Speaking to some optimization experts, pyomo seems to be a good skill to develop. See the accompanying [python file](pie_optimization.py) for the full model.
