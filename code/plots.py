"""
File containing code for plots used in tex project.

Usage:
    Run as main to update plots with new style.
    change style in if main statement
"""

import sys
import numpy as np
import os
sys.path.insert(0, "../../code/")

from classes import Point, PointList, LinkedList, MinkowskiSumProblem
import methods
from methods import N
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.animation as anim
from matplotlib.widgets import Button, Slider, TextBox
import random
import minimum_generator
import csv
import time
import csv
import math
from algorithm2 import algorithm2, alg2, Y_list_to_fixed_reduced
from minimum_generator import solve_MGS_instance
from copy import deepcopy



def plot_or_save(fig, fname: str):
    """ call to plot or save fig """
    if SAVE_PLOTS:
        print(f"{FIGURES_LOCATION=}")
        fig.savefig(fname = FIGURES_LOCATION + f"{fname}.pgf")
        fig.savefig(fname = FIGURES_LOCATION + f"{fname}.pdf")
    else:
        plt.title(fname)
        plt.show()

    
def example():
    N_list = range(10)

    Y1 = PointList(([(i,0) for i in N_list]))
    Y2 = PointList(([(i,i) for i in N_list]))
    Y3 = PointList(([(i,len(N_list)-1-i) for i in N_list]))

    # Y1.plot()
    # Y2.plot()
    # Y3.plot()
    Y1.plot()
    Y2.plot()
    Y3.plot()
    Y = methods.MS_sum((Y1,Y2))
    Y = PointList([y+Point((20,0)) for y in Y])
    Y.plot()
    Y = methods.MS_sum((Y1,Y2,Y3))
    Y = PointList([y+Point((50,0)) for y in Y])
    Y.plot()
    plt.show()


def example():


        

    ######################## Figure example START ########################
    fig_name = "example"
    print(f"Plotting figure: {fig_name}")
    # define new figure
    fig, ax = plt.subplots(figsize=SIZE_STANDARD_FIGURE, layout='constrained')
    
    
    Y1 = PointList([(1,10),(9,9),(10,1)])

    U = methods.induced_UB(Y1, line=True)


    y = Point((3,3))
    y.plot(l='y')

    Y1.plot(f"${_Y1}$")
    # y.plot_cone(ax=ax)

    for u in U:
        u.plot_cone(ax=ax, quadrant=1)
    
    for y in Y1:
        y.plot_cone(ax=ax, quadrant=3, color='blue')
    
    # save or plot figure
    plot_or_save(fig, fig_name)
    ######################### Figure example END #########################


def slides_MO_example():

    ######################## Figure slides_MSP_example START ########################
    fig_name = "slides_MO_example"
    print(f"Plotting figure: {fig_name}")
    # define new figure
    fig, ax = plt.subplots(figsize=(2.7,2.7), layout='constrained')
    
    Y1_list = []
    Y1_list.append(PointList(((1, 700),)))
    Y1_list.append(PointList([(1, 700),(1.5, 1000)]))
    Y1_list.append(PointList([(1, 700),(1.5, 1000), (3,500)]))
    Y1_list.append(PointList([(1, 700),(1.5, 1000), (3,500), (4,300)]))
    point_labels = ['plane1','Plane 2', 'Train','Bus']
    for i,Y1 in enumerate(Y1_list):

        Y1.plot(f"${_Y1}$", point_labels = point_labels[:i+1])
        plt.xlabel('Time (Hours)')
        plt.ylabel('Cost (DKK)')
        plt.xlim(0,5)
        plt.ylim(250,1100)
        # save or plot figure
        plot_or_save(fig, fig_name + f'_{i}')
        
        plt.cla()
        ######################### Figure slides_MSP_example END #########################

    # plot last point dominated
    Y1 = Y1_list[-1]
    i = len(Y1)
    Y1.plot(f"${_Y1}$", point_labels = point_labels)
    plt.xlabel('Time (Hours)')
    plt.ylabel('Cost (DKK)')
    plt.xlim(0,5)
    plt.ylim(250,1100)
    # save or plot figure
    Y_dom = PointList([y for y in Y1 if y not in N(Y1)])
    Y_dom.plot(marker = 'x', color = 'black')
    plot_or_save(fig, fig_name + f'_{i}')



def slides_MSP_example():

    ######################## Figure slides_MSP_example START ########################
    fig_name = "slides_MSP_example"
    print(f"Plotting figure: {fig_name}")
    # define new figure
    fig, ax = plt.subplots(figsize=(3,4), layout='constrained')
    
    plt.xlabel('Time (Hours)')
    plt.ylabel('Cost (DKK)')

    Y1 = PointList([(1, 700),(1.5, 1000),(3, 500),(4, 300)])
    Y2 = PointList([(1, 700),(1.5, 1000),(3, 500),(4, 300)])
    # Y1.plot(f"${_Y1}={_Y2}$")
    point_labels = ['plane1','Plane 2', 'Train','Bus']
    Y1.plot(f"${_Y1}={_Y2}$", point_labels = point_labels)
    # Y2.plot(f"_${_Y2}$", marker='x')
    Y = Y1 + Y2

    point_labels = False
    if point_labels:
        Y.plot(f"${_Y}$", point_labels = [f"{pl},{pl2}" for pl in point_labels for pl2 in point_labels ])
    else:
        Y.plot(f"${_Y}={_Y1}" +  "\oplus" + f"{_Y2}$", color='lightgray')

    plt.xlabel('Time (Hours)')
    plt.ylabel('Cost (DKK)')

    # save or plot figure
    plot_or_save(fig, fig_name + '_1')
    Yn = N(Y)
    # Yn.plot(f"${_Yn}$", marker='x')
    Y_dom = PointList([y for y in Y if y not in N(Y)])
    Y_dom.plot(marker = 'x', color = 'red')
    plot_or_save(fig, fig_name + '_2')
    ######################### Figure slides_MSP_example END #########################


def slides_MS_example():

    ######################## Figure MS_example START ########################
    fig_name = "/MS_example/MS_example_"
    print(f"Plotting figure: {fig_name}")
    # define new figure
    fig, ax = plt.subplots(figsize = (6,2.5), layout='constrained')
    

    Y1 = PointList([(1, 700),(1.5, 1000), (3,500), (4,300)])
    Y2 = PointList([(1, 700),(1.5, 1000), (3,500), (4,300)])
    # point_labels = ['plane1','Plane 2', 'Train','Bus']
    point_labels = True

    Yh_plot_color = 'gray'

    # plot 1 show Y1 = Y2
    plot_count = 2
    Y1.plot(f"${_Y1}={_Y2}$", point_labels = point_labels)
    plt.xlim(0,10)
    plt.ylim(0,2200)
    plot_or_save(fig, fig_name + str(plot_count))
    plt.cla()
    plot_count +=1
    
    # plot 2 show y11 + y21
    n_points1 = 1

    points_in_plot = []
    for n_points1, y1 in enumerate(Y1, start=1):
    # if True:
        # y1 = Y1[0]
        for n_points, y2 in enumerate(Y2, start=1):
            # if n_points1 >= 2:
                # n_points = len(Y2)
    #         Y1.plot(f"${_Y1}={_Y2}$", point_labels = point_labels)
            # Yh = PointList((Y1[0] + Y2[0],))
            # Yh.plot("$\{y^1\} \oplus \{y^2\}$", color=Yh_plot_color)
            # plot_or_save(fig, fig_name + str(plot_count))
            # plot_count +=1
        # plot 3 show {y11 + y21} + {y11 + y22}
            # n_points = 1

            plt.xlim(0,10)
            plt.ylim(0,2200)
            Y1h = PointList(Y1[j] for j in range(n_points1))
            print(f"{len(Y1h)=}")
            Y2h = PointList(Y2[i] for i in range(n_points))
            print(f"{len(Y2h)=}")
            Yh = Y1h + Y2h
            points_in_plot += list(Yh.points)
            # Yh = PointList((Y1[j] + Y2[i] for j in range(n_points1) for i in range(n_points)))
            Yh = PointList((y1 + Y2[i] for i in range(n_points)))
            # label = "$\{" + ",".join([f"y^{i+1}" for i in range(n_points1)]) +"\}$" + "$\oplus \{" + ",".join([f"y^{i+1}" for i in range(n_points)]) +"\}$"
            label = "$\{y^"+ str(n_points1) +"\}$" + "$\oplus \{" + ",".join([f"y^{i+1}" for i in range(n_points)]) +"\}$"
            Yh_all = PointList(set(points_in_plot))



            Y1.plot(f"${_Y1}={_Y2}$", point_labels = point_labels)
            Yh_all.plot(l = "$\hat{" + f"{_Y}" + "}\subseteq" + f"{_Y}$", color = Yh_plot_color)
            Yh.plot(l = label, color = 'black',marker='x')
            # Yh.plot(label, color=Yh_plot_color)
            y1.plot(marker='x', color='black')
            y2.plot(marker='x', color='black')
            line_color = 'lightgray'
            # for y2 in Y2h[-1]:
            if True:
                line = PointList((y2,y1+y2))
                line.plot(line=True, linestyle='dashed', color=line_color)
                line = PointList((y1,y1+y2))
                line.plot(line=True, linestyle='dashed', color=line_color)
                # line = PointList((y1,y1+y2))
                line = PointList((Point((0,0)), y1))
                line.plot(line=True, linestyle='dashed', color=line_color)
                line = PointList((Point((0,0)), y2))
                line.plot(line=True, linestyle='dashed', color=line_color)

            plot_or_save(fig, fig_name + str(plot_count))
            plt.cla()
            plot_count +=1
     

    plt.xlim(0,10)
    plt.ylim(0,2200)
    Y1.plot(f"${_Y1}={_Y2}$", point_labels = point_labels)
    Y = Y1 + Y2
    Y.plot(f"${_Y} = " +f"{_Y1}" +  "\oplus" + f"{_Y2}$", color =Yh_plot_color)
    plot_or_save(fig, fig_name + str(plot_count))
    
def counter_example_reduction():

    ######################## Figure counter_example_reduction START ########################
    fig_name = ""
    print(f"Plotting figure: {fig_name}")
    # define new figure
    fig, ax = plt.subplots(layout='constrained')
    
    Y1 = PointList([(1,10),(9,9),(10,1)])*0.2
    Y2_list = [PointList([(3,6),(6,3)]), PointList([(3,6),(6,3),(10,-10)])]
    Y2_list = [PointList([(3,6),(6,3),(10,-10),(13,-13)]), PointList([(3,6),(6,3),(8,3-6.5),(10,-10),(13,-13)])]
    Y2_list = [
            PointList([(1,10),(2,9),(9,2),(10,1)]), 
            PointList([(1,10),(2,9),(5,4),(9,2),(10,1)]), 
               # PointList([(3,6),(6,3),(8,3-6.5),(10,-10),(13,-13)])
               ]

    for Y2 in Y2_list:
        Y = Y1 + Y2
        y1 = Y1[1]
        y2 = Y2[2]
        y1MSY2 = PointList((Y1[1],))+ Y2
        print(f"{Y.dominates(y1MSY2)=}")

        Y1.plot(f"${_Y1}$", color='red', point_labels=False)
        y1.plot(l='$y^1$', label_only=True)
        if Y2 == Y2_list[0]:
            Y2.plot(f"${_Yh2} \subseteq {_Y2}$", color = 'blue', point_labels=False)
        else:
            y2.plot(l='$y^2$', label_only=True)
            Y2.plot(f"${_Yh2} \subseteq {_Y2}$", color = 'blue', point_labels=False)
            # Y2.plot(f"${_Y2}$", color = 'blue', point_labels=False)
        Y.plot(f"${_Y}$", color = 'gray')
        if Y2 == Y2_list[-1]:
            # N(Y)[-2].plot(l='$y^{1,2} + y^{2,3}$' + "$\in$" + f"${_Yn}$", label_only=True)
            (y1+y2).plot(l='$y^{1} + y^{2}$' + "$\in$" + f"${_Yn}$", label_only=True)
        y1MSY2.plot("$\{y^1\}" + "\oplus" + f"{_Y2}$", marker='x')

        plot_or_save(fig, fig_name)
        matrix_plot(Y1,Y2, fig_name = fig_name, point_labels=True, figsize = (10,7))
        # save or plot figure
        ######################### Figure counter_example_reduction END #########################


def example_reduction_lower_bounds():
    ######################## Figure reduction_lower_bounds START ########################
    fig_name = "reduction_lower_bounds"
    print(f"Plotting figure: {fig_name}")
    # define new figure
    fig, ax = plt.subplots(figsize=SIZE_STANDARD_FIGURE, layout='constrained')
    

    
    Y1 = PointList.from_json('./instances/subproblems/sp-2-10-m_3.json')*0.5
    Y1h = PointList([y1 for i,y1 in enumerate(Y1) if i in [0,3,4,8,9]])
    Y2 = PointList.from_json('./instances/subproblems/sp-2-10-m_10.json')
    Y2h = PointList([y2 for i,y2 in enumerate(Y2) if i in [0,3,4,8,9]])
    L = methods.induced_UB(Y2,line=True, assumption='nonconsecutive')

    Y = Y1 + Y2
    Yh = N(Y1h + Y2h)

    Y1.plot(f"${_Y1}$", marker='x')
    Y1h.plot(f"${_Yh1}$", color=Y1.plot_color)
    Y2.plot(f"${_Y2}$", marker='x')
    Y2h.plot(f"${_Yh2}$", color=Y2.plot_color)

    Y.plot(f"${_Y}$", marker='x', color='lightgray')
    Yh.plot(f"${_Yh}$", color=Y.plot_color)

    L.plot(f"${_L}$", line=True)

    # fix y1 and check {y1} + LB(Y2h) is dominated by Yh
    
    y1 = Y1[3]
    
    y1.plot(l='$y^1$', label_only=True)
    y1MSLB2 = PointList((y1)) + L
    y1MSLB2.plot("$\{y^1\} \oplus" + f"{_L2}$")
    # save or plot figure
    plot_or_save(fig, fig_name)

def MSP_sol_example():

    ######################## Figure slides_MSP_example START ########################
    fig_name = "slides_MSP_example"
    print(f"Plotting figure: {fig_name}")
    # define new figure
    fig, ax = plt.subplots(figsize=(5,3), layout='constrained')
    
    Y1 = PointList.from_json("./instances/subproblems/sp-2-10-m_1.json")
    Y2 = PointList.from_json("./instances/subproblems/sp-2-10-m_2.json")
    # Y1.plot(f"${_Y1}={_Y2}$")
    # Y2.plot(f"_${_Y2}$", marker='x')
    Y = Y1 + Y2

    Y1.plot(f"${_Y1}$")
    Y2.plot(f"${_Y2}$")
    for y1 in Y1:
        
        Yhat = PointList((y1,)) + Y2
        Yhat.plot()
        # plot_or_save(fig, fig_name + '_1')

    Y.plot(f"${_Y}$")
    # Yn = N(Y)
    # Yn.plot(f"${_Yn}$")
    # save or plot figure
    plot_or_save(fig, fig_name + '_1')
    ######################### Figure slides_MSP_example END #########################



def plot_ul():

    ######################## Figure plot_ul START ########################
    fig_name = "plot_ul"
    print(f"Plotting figure: {fig_name}")
    # define new figure
    fig, ax = plt.subplots(figsize=SIZE_STANDARD_FIGURE, layout='constrained')
    
    MSP = MinkowskiSumProblem.from_json('instances/problems/prob-2-100|100-ul-2_1.json')
    Y1, Y2 = MSP.Y_list

    Y1.label = f"${_Yn1}$"
    Y2.label = f"${_Yn2}$"

    for Y in MSP.Y_list:
        Y.plot(l = Y.label)
    

    
    # save or plot figure
    plot_or_save(fig, fig_name)
    ######################### Figure plot_ul END #########################


def matrix_plot(Y1,Y2, fig_name, point_labels = False, matrix_only = False, plot_mapping= True, figsize = (7,3)):
    """ plots similar to matrix plots in Hespe et al. 2023 """


    fig = plt.figure(figsize=figsize, layout='constrained')
    ax = list()
    projection = None if Y1.dim == 2 else '3d'
    ax.append(fig.add_subplot(1, 3, 1, projection= projection ))

    plt.xlabel('Objective 1')
    plt.ylabel('Objective 2')
    plt.tick_params(left = False, right = False , labelleft = False , labelbottom = False, bottom = False) 
    plt.xlim(-1000,11000*2)
    plt.ylim(-1000,11000*2)
    ax.append(fig.add_subplot(1, 3, 2))

    # plt.xlabel('f"${_Yn1}$"')
    # plt.ylabel('f"${_Yn2}$"')

    ax.append(fig.add_subplot(1, 3, 3, projection= projection ))
    # fig, ax = plt.subplots(ncols = 3, figsize=SIZE_LARGE_FIGURE, layout='constrained')
    

    plt.xlabel('Objective 1')
    plt.ylabel('Objective 2')
    plt.tick_params(left = False, right = False , labelleft = False , labelbottom = False, bottom = False) 
    plt.xlim(-1000,11000*1.9)
    plt.ylim(-1000,11000*1.9)

    # ax[2].xlabel('Objective 1')
    # ax[2].plt.ylabel('Objective 2')
    # ax[2].tick_params(left = False, right = False , labelleft = False , labelbottom = False, bottom = False) 

    Y1 = methods.lex_sort(Y1)
    Y2 = methods.lex_sort(Y2)
    Y1_color = Y1.plot_color   
    Y2_color = Y2.plot_color   

    Y = Y1+Y2
    Yn = N(Y)
    Yn_set = set(Yn.points)

    # ######################## Figure ax1 START ########################
    # fig_name = "ax1"
    # # define new figure
    

    if not matrix_only:
        Y1.plot(ax = ax[0], l = f"${_Yn1}$", point_labels= point_labels)
        Y2.plot(ax = ax[0], l = f"${_Yn2}$", point_labels= point_labels)

    # # save or plot figure
    # plot_or_save(fig, fig_name)

    # add marking of point contributes to Pareto Sum point:

    Y1_MSP = PointList([y1 for y1 in Y1 if any((y1+y2 in Yn_set for y2 in Y2))])
    Y2_MSP = PointList([y2 for y2 in Y2 if any((y1+y2 in Yn_set for y1 in Y1))])

    if not matrix_only and plot_mapping:
        # Y1_MSP.plot(ax = ax[0], l = f"${_Yn1}\\rightarrow {_Yn}$",color = "yellow", marker='1')
        # Y2_MSP.plot(ax = ax[0], l = f"${_Yn2}\\rightarrow {_Yn}$", color = "yellow", marker='1')
        Y1_MSP.plot(ax = ax[0], l = f"_",color = "yellow", marker='1')
        Y2_MSP.plot(ax = ax[0], l = f"_", color = "yellow", marker='1')

    # ######################### Figure ax1 END #########################


    if plot_mapping:
        M = np.array([[1 if y1+y2 in Yn_set else 0 for y1 in Y1] for y2 in Y2])
    else:
        M = np.array([[0 if y1+y2 in Yn_set else 0 for y1 in Y1] for y2 in Y2])
    col_header = np.array([3 for _,y  in enumerate(Y1)])
    row_header = np.array([5] + [4 for _,y  in enumerate(Y2)])

    M = np.vstack([col_header, M])
    M = np.vstack([row_header, M.transpose()])

    ax[0].legend(loc='upper right')

    ######################## Figure matrix_plot START ########################
    
    # Define your custom colors
    colors = ['lightgray', 'yellow', 'red', Y1.plot_color, Y2.plot_color, 'white']
    if matrix_only:
        colors = ['lightgray', 'yellow', 'red', 'red', 'blue', 'white']
    # Create a colormap with discrete colors
    cmap = matplotlib.colors.ListedColormap(colors)

#     ax[1].imshow(M, cmap = cmap)
    # # ax[1].imshow(M)

    if point_labels:
        for i, y in enumerate(Y1):
            ax[1].annotate(text = "$y^{" +  f"{i+1}" + "}$", xy = (i+1.5,0.51))   
        for i, y in enumerate(Y1):
            ax[1].annotate(text = "$y^{" +  f"{i+1}" + "}$", xy = (0.5,i+1.5))   

    ax[1].axis('off')


    ax[1].pcolormesh(M, cmap = cmap, edgecolors='white', linewidth=0.5)
    ax[1] = plt.gca()
    # ax[1].set_aspect('equal')
    # ax[0].set_aspect('equal')
    # ax[2].set_aspect('equal')
    
    # ax[0].set_title("Subproblem Pareto sets")
    # ax[1].set_title("Matrix")
    
    print(f"|Yn| = {len(Yn)}")
    print(f"|Y1| + |Y2| = {len(Y1) + len(Y2)}")
    print(f"|Y1||Y2| = {len(Y1)*len(Y2)}")
    print(f"")
    print(f"|Y1| = {len(Y1)}")
    print(f"|Y2| = {len(Y2)}")
    print(f"|Yn1 MSP | = {len(Y1_MSP)}")
    print(f"|Yn2 MSP | = {len(Y2_MSP)}")
    
    # save or plot figure
    # plot_or_save(fig, fig_name)
    ######################### Figure matrix_plot END #########################


    ######################## Figure pareto_sum START ########################
    # fig_name = "pareto_sum"
    print(f"Plotting figure: {fig_name}")
    # define new figure
    # fig, ax = plt.subplots(figsize=SIZE_STANDARD_FIGURE, layout='constrained')
 
    if not matrix_only:
        Y.plot(ax = ax[2], l = f"${_Yn1}"+"\\oplus" +f"{_Yn2}$", color = colors[0])
        if plot_mapping:
            Yn.plot(ax = ax[2], l = f"${_Yn}$", color = "yellow")
    
    # save or plot figure
    plot_or_save(fig, fig_name)
    ######################### Figure pareto_sum END #########################
        
def make_matrix_plot():

    plot_configs = [
            {"fig_name": 'matrix_plot', 'scaling' : 1,
             'Y1' : "instances/subproblems/sp-2-10-l_1.json",
             'Y2' : "instances/subproblems/sp-2-10-u_1.json"},
            {"fig_name": 'methods_lu', 'scaling' : 1,
             'Y1' : "instances/subproblems/sp-2-100-l_1.json",
             'Y2' : "instances/subproblems/sp-2-100-u_1.json"},
            {"fig_name": 'methods_lm', 'scaling' : 1,
             'Y1' : "instances/subproblems/sp-2-100-l_1.json",
             'Y2' : "instances/subproblems/sp-2-100-m_1.json"},
            {"fig_name": 'methods_mm', 'scaling' : 1,
             'Y1' : "instances/subproblems/sp-2-100-m_1.json",
             'Y2' : "instances/subproblems/sp-2-100-m_2.json"},
            {"fig_name": 'scaling_lu_1', 'scaling' : 1,
             'Y1' : "instances/subproblems/sp-2-100-l_1.json",
             'Y2' : "instances/subproblems/sp-2-100-u_1.json"},
            {"fig_name": 'scaling_lu_2', 'scaling' : 2,
             'Y1' : "instances/subproblems/sp-2-100-l_1.json",
             'Y2' : "instances/subproblems/sp-2-100-u_1.json"},
            {"fig_name": 'scaling_lu_0_5', 'scaling' : 0.5,
             'Y1' : "instances/subproblems/sp-2-100-l_1.json",
             'Y2' : "instances/subproblems/sp-2-100-u_1.json"},
            {"fig_name": 'scaling_lu_0_1', 'scaling' : 0.1,
             'Y1' : "instances/subproblems/sp-2-100-l_1.json",
             'Y2' : "instances/subproblems/sp-2-100-u_1.json"},
            {"fig_name": 'dim_2', 'scaling' : 1,
             'Y1' : "instances/subproblems/sp-2-100-l_1.json",
             'Y2' : "instances/subproblems/sp-2-100-u_1.json"},
            {"fig_name": 'dim_3', 'scaling' : 1,
             'Y1' : "instances/subproblems/sp-3-100-l_1.json",
             'Y2' : "instances/subproblems/sp-3-100-u_1.json"},
            {"fig_name": 'dim_4', 'scaling' : 1,
             'Y1' : "instances/subproblems/sp-4-100-l_1.json",
             'Y2' : "instances/subproblems/sp-4-100-u_1.json"},
            {"fig_name": 'dim_5', 'scaling' : 1,
             'Y1' : "instances/subproblems/sp-5-100-l_1.json",
             'Y2' : "instances/subproblems/sp-5-100-u_1.json"},
            {"fig_name": 'magnitudes1', 'scaling' : 1,
             'Y1' : "instances/subproblems/sp-2-10-u_1.json",
             'Y2' : "instances/subproblems/sp-2-10-m_10.json"},
            {"fig_name": 'magnitudes10', 'scaling' : 10,
             'Y1' : "instances/subproblems/sp-2-10-u_1.json",
             'Y2' : "instances/subproblems/sp-2-10-m_10.json"},
            {"fig_name": 'magnitudes20', 'scaling' : 20,
             'Y1' : "instances/subproblems/sp-2-10-u_1.json",
             'Y2' : "instances/subproblems/sp-2-10-m_10.json"},
            {"fig_name": 'magnitudes1_1', 'scaling' : 1,
             'Y1' : "instances/subproblems/sp-2-10-u_1.json",
             'Y2' : "instances/subproblems/sp-2-10-m_10.json"},
            {"fig_name": 'magnitudes1_2', 'scaling' : -2,
             'Y1' : "instances/subproblems/sp-2-10-u_1.json",
             'Y2' : "instances/subproblems/sp-2-10-m_10.json"},
            {"fig_name": 'magnitudes1_5', 'scaling' : -5,
             'Y1' : "instances/subproblems/sp-2-10-u_1.json",
             'Y2' : "instances/subproblems/sp-2-10-m_10.json"},
            ]
    
    for P in plot_configs:
        Y1 = PointList.from_json(P['Y1'])
        Y2 = PointList.from_json(P['Y2'])
        fig_name = P['fig_name']
        scaling = P['scaling']

        # scaling = 1
        if scaling:
            if scaling < 0:
                Y1 = PointList([y*(-scaling) for y in Y1])
            else:
                Y2 = PointList([y*scaling for y in Y2])

        point_labels = (len(Y1) <= 10 and len(Y2) <= 10)

        matrix_only = Y1.dim > 3
        
        # fig_name = "matrix_plot"
        if 'magnitudes' not in fig_name: continue

        matrix_plot(Y1,Y2, fig_name = fig_name, point_labels= point_labels, matrix_only=matrix_only)


def slides_matrix_example_MGS():
    Y1 = PointList.from_json("instances/subproblems/sp-2-10-u_1.json")
    Y1 = [y1 for y1 in Y1]
    Y1 += [y1*1.1 for y1 in PointList.from_json("instances/subproblems/sp-2-10-u_2.json")]
    Y1_remove = {i:tuple(y.val) for i,y in enumerate(N(PointList(Y1))) if i in (7, 8, 9,10, 11, 12) }
    Y1 = [y1 for i,y1 in enumerate(Y1) if tuple(y1.val) not in Y1_remove.values()]
    Y1 = PointList(Y1)

    Y2 = PointList.from_json("instances/subproblems/sp-2-10-m_10.json")
    Y2 = [y2 for y2 in Y2]
    Y2 += [y1*1.1 for y1 in PointList.from_json("instances/subproblems/sp-2-10-m_2.json")]
    Y2 = PointList(Y2)
    fig_name = "test_plot" 


    MSP = MinkowskiSumProblem([Y1,Y2])
    MGS = MinkowskiSumProblem(algorithm2(MSP))

    ######################## Figure test_plot START ########################
    fig_name = "test_plot"
    print(f"Plotting figure: {fig_name}")
    # define new figure
    fig, ax = plt.subplots(figsize=SIZE_STANDARD_FIGURE, layout='constrained')
    
    
    MSP.plot()
    MGS.plot(marker='x')
    
    
    # save or plot figure
    plot_or_save(fig, fig_name)
    ######################### Figure test_plot END #########################



def slides_matrix_plot():
    Y1 = PointList.from_json("instances/subproblems/sp-2-10-u_1.json")
    Y1 = [y1 for y1 in Y1]
    Y1 += [y1*1.1 for y1 in PointList.from_json("instances/subproblems/sp-2-10-u_2.json")]
    Y1_remove = {i:tuple(y.val) for i,y in enumerate(N(PointList(Y1))) if i in (7, 8, 9,10, 11, 12) }
    Y1 = [y1 for i,y1 in enumerate(Y1) if tuple(y1.val) not in Y1_remove.values()]
    Y1 = PointList(Y1)

    Y2 = PointList.from_json("instances/subproblems/sp-2-10-m_10.json")
    Y2 = [y2 for y2 in Y2]
    Y2 += [y1*1.1 for y1 in PointList.from_json("instances/subproblems/sp-2-10-m_2.json")]
    Y2 = PointList(Y2)
    fig_name = "test_plot" 
    scaling = 1

    # scaling = 1
    if scaling:
        Y2 = PointList([y*scaling for y in Y2])

    point_labels = len(Y1) <= 20 and len(Y2) <= 20
    print(f"{point_labels=}")

    matrix_only = Y1.dim > 3
    

    ######################## Figure initial_filter START ########################
    fig_name = "initial_filter_"
    print(f"Plotting figure: {fig_name}")
    # define new figure
    fig, ax = plt.subplots(figsize=(6,3), layout='constrained')
    



    plt.xlabel('Objective 1')
    plt.ylabel('Objective 2')

    ax.tick_params(left = False, right = False , labelleft = False , labelbottom = False, bottom = False) 
    

    plt.xlim(-1000,11000)
    plt.ylim(-1000,11000)
    Y1.plot(f"${_Y1}$")
    Y2.plot(f"${_Y2}$")
    Yn1 = N(Y1)
    Yn2 = N(Y2)

    plot_or_save(fig, fig_name + str(1))


    plt.xlabel('Objective 1')
    plt.ylabel('Objective 2')

    Y1_dom = PointList([y1 for y1 in Y1 if y1 not in Yn1])
    Y2_dom = PointList((y2 for y2 in Y2 if y2 not in Yn2))
    Y1_dom.plot(marker = 'x', color = 'black')
    Y2_dom.plot(marker = 'x', color = 'black')
    
    plot_or_save(fig, fig_name + str(2))
    plt.cla()


    plt.xlabel('Objective 1')
    plt.ylabel('Objective 2')

    plt.xlim(-1000,11000)
    plt.ylim(-1000,11000)
    Yn1 = N(Y1)
    Yn2 = N(Y2)
    Yn1.plot(f"${_Yn1}$")
    Yn2.plot(f"${_Yn2}$")

    plt.xlim(-1000,11000)
    plt.ylim(-1000,11000)
    # save or plot figure
    plot_or_save(fig, fig_name + str(3))
    ######################### Figure initial_filter END #########################

    Y1, Y2 = Yn1, Yn2
    matrix_plot(Y1,Y2, fig_name = fig_name + str(4), point_labels= point_labels, matrix_only=matrix_only, plot_mapping=False)
    matrix_plot(Y1,Y2, fig_name = fig_name + str(5), point_labels= point_labels, matrix_only=matrix_only)



def minimum_not_minimal():

    ######################## Figure minimum_not_minimal START ########################
    fig_name = "minimum_not_minimal"
    print(f"Plotting figure: {fig_name}")
    # define new figure
    fig, ax = plt.subplots(ncols=3,figsize=SIZE_STANDARD_FIGURE, layout='constrained')
    print(f"{ax=}")
    


    Y1 = PointList(((1+i,13-i) for i in range(0,14,2)))
    Y2 = PointList(((0,4),(2,2),(4,0)))

    Y = Y1 + Y2

    for axis in ax:
        Y1.plot(ax = axis,l=f"${_Y1}$")
        Y2.plot(ax = axis, l=f"${_Y2}$")
        Y.plot(ax = axis, l=f"${_Y}={_Yn}$", color = 'lightgray')
        

    # plot 2
    G1 = PointList([y for i,y in enumerate(Y1) if i in (0,2,4,6)])
    G1.plot(ax=ax[1],l=f"$|{_G1}|=4$", color = 'purple')
    (G1+Y2).plot(ax=ax[1], l=f"${_G1}\oplus {_Y2}$", marker ='1', color = 'purple')
    for g in G1:
        for y2 in Y2:
            line = PointList((g,y2+g))
            line.plot(ax=ax[1],line=True, color='lightgray', linestyle='dashed')

    G1 = PointList([y for i,y in enumerate(Y1) if i in (0,3,6)])
    G1.plot(ax=ax[2],l="$|\\bar" +f"{_G1}|=3$", color='purple')
    (G1+Y2).plot(ax=ax[2], l="$\\bar" + f"{_G1}\oplus {_Y2}$", marker ='1', color = 'purple')
    for g in G1:
        for y2 in Y2:
            line = PointList((g,y2+g))
            line.plot(ax=ax[2],line=True, color='lightgray', linestyle='dashed')
   
    # save or plot figure
    plot_or_save(fig, fig_name)
    ######################### Figure minimum_not_minimal END #########################

    # matrix_plot(Y1,Y2,'minimum_not_minimal_matrix', point_labels=True)

def klamroth2023_lemma2():
    l = 6
    m = 6
    A = PointList([(-1,-1,-0)] + [(-0, -i/l, -(l-i)/l) for i in range(1,l)])
    B = PointList([(-0,-1,-1)] + [(-i/m, -(m-i)/m, -0 ) for i in range(1,m)])

    # print(f"{A=}")
    # print(f"{B=}")


    fig = plt.figure()
    fig.tight_layout(h_pad=20)
    ax= plt.axes(projection = '3d')
    

    A.plot(ax= ax, l=f"${_A}$")
    B.plot(ax= ax, l=f"${_B}$")

    # S = PointList(A.points + B.points)
    S = A + B

    S.plot(ax= ax, l = f"${_A} + {_B}$")
    Sn = N(S)
    # print(f"$A+B = \{S}$")
    # print(f"(A+B)_N = {Sn}")
    Sn.plot(ax= ax, l= f"(${_A} + {_B} )_{_mcN}$" , color="blue")

    # print(f"{len(Sn.removed_duplicates())=}")

    # print(f"|A|={len(A)}")
    # print(f"|B|={len(B)}")
    # print(f"|A+B|={len(S)}")
    # print(f"|(A+B)_N|={len(Sn)}")

    plt.show()


def induced_UB_plot(level, Y1,Y2, prefix='', plot=True):
    print(f"{prefix}")
    # print(f"{level=}")
    def get_partial(Y, level='all'):   
        Y = N(Y)
        Y2e_points = [y for y in Y if y.cls == 'se']
        Y2other_points = [y for y in Y if y.cls != 'se']
        # random.shuffle(Y2other_points)
        match level:
            case 'all':
                return Y
            case 'lexmin': 
                return PointList((Y[0], Y[-1]))
            case 'extreme':
                return PointList(Y2e_points)
            # case float():
            case _:
                to_index = math.floor(float(level)*len(Y2other_points))
                return PointList(Y2e_points + Y2other_points[:to_index])
                # print(f"case not implemented {level}")
    ######################## Figure Induced_UB START ########################
    # fig_name = f"Induced_UB_{level}".replace('lexmin','0.00lexmin')
 
    def reset_graph():
        plt.xlabel('Objective 1')
        plt.ylabel('Objective 2')
        plt.tick_params(left = False, right = False , labelleft = False , labelbottom = False, bottom = False)

    fig_name = f"/RGS_example/RGS_sup"


    only_supported = True 

    LB_assumption = 'consecutive'
    if only_supported:
        LB_assumption = 'supported'


    # print(f"Plotting figure: {fig_name}")
    # define new figure
    if plot:
        fig, ax = plt.subplots(figsize=(7,3.5), layout='constrained')

        reset_graph()

        plot_count = 1
    

    Y2_partial = get_partial(Y2, level)
    Y = Y1 + Y2
    Y2.plot_color= 'lightcoral'
    # Y1_supported = N(PointList([y1_s for y1_s in Y1 if y1_s.cls =='s']))
    Y1_supported = Y1
    if only_supported:
        # Y1_supported = N(PointList([y1_s for y1_s in Y1 if y1_s.cls =='s']))
        Y1_supported = N(PointList([y1_s for y_id, y1_s in enumerate(N(Y1)) if y_id in {0,1,2,6,9}]))
    # Y1_supported = Y1
    # L1_line = methods.induced_UB(N(Y1), line=True, assumption=LB_assumption)
    L1_line = methods.induced_UB(Y1_supported, line=True, assumption=LB_assumption)
    L1 = N(methods.induced_UB(Y1_supported,line=True, assumption=LB_assumption))

    label_hatY2 = "$\hat{"+f"{_Y1}" + "} \subseteq " + f"{_Y1}" + "$"

    for y2 in [y2_choice for y2_choice_id, y2_choice in enumerate(Y2) if y2_choice_id in {2,3,4}]:
        print(f"{y2=}")
        # y2 = Y2[2]
        if plot:
            Y_partial = Y2_partial + Y1
            Y2.plot(f"${_Y1}$")
            Y2_partial.plot(label_hatY2, marker='o', color='red')

            Y1.plot(f"${_Y2}$", color ='blue')
            # L1_line.plot(f"${_L2}$", line=True, color=Y1.plot_color)
            Y.plot(f"${_Y}= {_Y1}"  + "\oplus" + f"{_Y2}$", color='lightgray')
            # Y_partial.plot("$\hat{"f"{_Y}" + "}=" + "\hat{"f"{_Y1}" + "}" + "\oplus" + f"{_Y2}$", marker='1')
            Y_partial.plot("$\hat{"+f"{_Y}" + "}=" + "\hat{"f"{_Y1}" + "}" + "\oplus" + f"{_Y2}$", marker='1', color = 'gray')
            plot_or_save(fig, fig_name + str(plot_count))
            plot_count +=1
            plt.cla()
            ax = reset_graph()

            # Y_partial = Y2_partial + Y1
            Y2.plot(f"${_Y1}$")
            Y2_partial.plot(label_hatY2, marker='o', color='red')
            Y1.plot(f"${_Y2}$")
            # L1_line.plot(f"${_L2}$", line=True, color=Y1.plot_color)
            Y.plot(f"${_Y}= {_Y1}"  + "\oplus" + f"{_Y2}$", color='lightgray')
            Y_partial.plot("$\hat{"+f"{_Y}" + "}=" + "\hat{"f"{_Y1}" + "}" + "\oplus" + f"{_Y2}$", marker='1', color = 'gray')

            U_partial = methods.induced_UB(Y_partial, line=True)
            U_partial.plot(line=True, color='lightgray')
            plot_or_save(fig, fig_name + str(plot_count))
            plot_count +=1


            plt.cla()
            reset_graph()
            # Y_partial = Y2_partial + Y1
            Y2.plot(f"${_Y1}$")
            Y2_partial.plot(label_hatY2, marker='o', color='red')
            Y1.plot(f"${_Y2}$")
            # L1_line.plot(f"${_L2}$", line=True, color=Y1.plot_color)


            Y.plot(f"${_Y}= {_Y1}"  + "\oplus" + f"{_Y2}$", color='lightgray')
            Y_partial.plot("$\hat{"+f"{_Y}" + "}=" + "\hat{"f"{_Y1}" + "}" + "\oplus" + f"{_Y2}$", marker='1')
            y2.plot(l='$y^1$',marker='x', label_only=True)
            y2MSY1 = Y1_supported + PointList((y2,))
            L1MSY1 = L1 + PointList((y2,))
        
            y2MSY1.plot("$\{y^1\}"  + "\oplus" + f"{_Y2}$", color='black')

            # nonconsecutive
            # L1_line.plot(f"${_L2}$", line=True, color=Y1.plot_color)
            # L1.plot(f"${_L2}$", color = Y1.plot_color, marker='x')
            # L1MSY1.plot("$\{y^1\}"  + "\oplus" + f"{_L2}$", color='blue', marker='x')

            # supported
            # L1_line = methods.induced_UB(Y1, line=True, assumption=LB_assumption)
            # L1_line.plot(f"${_L2}$", line=True, color=Y1.plot_color)
            # U_partial = methods.induced_UB(Y_partial, line=True)
            U_partial.plot(line=True, color='lightgray')
            

            plot_or_save(fig, fig_name + str(plot_count))
            plot_count +=1
            plt.cla()
            reset_graph()






        ub_time = time.time()
        U = methods.find_generator_U(Y2_partial, Y1)
        ub_time = time.time() - ub_time

        Uline = methods.induced_UB(U,line=True, assumption=LB_assumption)
        Uline.plot_color = Y2.plot_color
        
        Y2_dominated = [y for y in Y2 if y.cls != 'se' and U.dominates_point(y)]
        # if Y2_dominated and plot:
            # PointList(Y2_dominated).plot("dominated", marker='x')
        print(f"{len(Y2_dominated)=}")
        dominated_relative = len(Y2_dominated)/len(Y2)
        print(f"dominated: {len(Y2_dominated)} \nrelative: {dominated_relative*100}\%")
        if plot:


            Y2.plot(f"${_Y1}$")
            Y2_partial.plot(label_hatY2, marker='o', color='red')
            Y1.plot(f"${_Y2}$")
            L1_line.plot(f"${_L2}$", line=True, color=Y1.plot_color)
            Y.plot(f"${_Y}= {_Y1}"  + "\oplus" + f"{_Y2}$", color='lightgray')
            Y_partial.plot("$\hat{" + f"{_Y}" + "}=" + "\hat{"f"{_Y1}" + "}" + "\oplus" + f"{_Y2}$", marker='1')
            y2.plot(l='$y^1$',marker='x', label_only=True)
            y2MSY1.plot("$\{y^1\}"  + "\oplus" + f"{_L2}$")
            y2L = methods.induced_UB(y2MSY1, line=True, assumption=LB_assumption)
            y2L.plot(line=True, color='black')
            U_partial.plot(line=True, color='lightgray')
            # L1_line.plot(f"${_L2}$", line=True, color=Y1.plot_color)
            plot_or_save(fig, fig_name + str(plot_count))
            plot_count +=1


            plt.cla()
            reset_graph()

            # new plot
            Y2.plot(f"${_Y1}$")
            Y2_partial.plot(label_hatY2, marker='o', color='red')
            Y1.plot(f"${_Y2}$")
            Y.plot(f"${_Y}= {_Y1}"  + "\oplus" + f"{_Y2}$", color='lightgray')
            Y_partial.plot("$\hat{"f"{_Y}" + "}=" + "\hat{"f"{_Y1}" + "}" + "\oplus" + f"{_Y2}$", marker='1')
            y2.plot(l='$y^1$',marker='x', label_only=False, color ="black")
            # Uline.plot(f"${_U}$", line=True)
            # y2 = Y2[4]
            # y2.plot(l='$y^1$',marker='x', label_only=True)
            # y2MSY1 = Y1 + PointList((y2,))
            # y2MSY1.plot("$\{y^1\}"  + "\oplus" + f"{_Y2}$")
            # plot_or_save(fig, "slides_" + fig_name + '_1' )
            # plt.cla()
            # Uline.plot(f"${_U}$", line=True)
            # Y2.plot(f"${_Y1}$")
            # Y1.plot(f"${_Y2}$")
            # Y2_partial.plot("$\hat{"f"{_Y1}" + "}$", marker='1')



        # if plot: plt.text(0.1,0.1,f"dominated: {len(Y2_dominated)} \n relative: {dominated_relative*100}\%")
        
        # save or plot figure
        if plot:
            plot_or_save(fig, fig_name + str(plot_count))
            plot_count +=1
        ######################### Figure Induced_UB END #########################

        run_data = {'prefix' : prefix,
                    'Y1_size' : len(Y1),
                    'Y2_size' : len(Y2),
                    'U' : len(U),
                    'U_time' : ub_time,
                    'dominated_points' : len(Y2_dominated),
                    'dominated_relative_Y2' : dominated_relative,
                    }

        # return run_data
def multiple_induced_UB():


    set_options = ['l','m','u']
    size_options = [10, 50, 100, 150, 200, 300, 600]
    seed_options = [1,2,3,4,5]
    UB_options = ['lexmin','extreme','0.25','0.5','0.75','all']

    csv_file_path = './instances/results/algorithm3/result.csv'
    # get last row
    with open(csv_file_path, 'r') as csv_file:
        reader = csv.reader(csv_file)
        rows = [row for row in reader]

    lastrow = rows[-1]
    del rows

    start_runs = False
    for s1 in size_options:
        s2 = s1
        for ub_level in UB_options:
        # s1 = 100 
        # s2 = 100
            # for s2 in size_options:
            for t1 in set_options:
                for t2 in set_options:
                    for seed in seed_options:
                        
                        prefix = f'{t1}-{t2}_{s1}_{s2}_{ub_level}_{seed}_'
                        
                        if start_runs == False:
                            if prefix == lastrow[0]:
                                start_runs = True
                                print(f"Starting run after {prefix}")

                            continue

                        Y1 = PointList.from_json(f"./instances/subproblems/sp-2-{s1}-{t1}_{seed}.json")
                        Y2 = PointList.from_json(f"./instances/subproblems/sp-2-{s2}-{t2}_{max(seed_options)+1-seed}.json")
                        data = induced_UB_plot(ub_level, Y1,Y2, prefix, plot=False) 
                        data.update({'t1':t1, 't2':t2, 's1':s1, 's2':s2,'seed':seed,'ub_level':ub_level})
                        with open(csv_file_path, 'a') as csv_file:
                            # add header if file empty
                            writer = csv.writer(csv_file)
                            if os.path.getsize(csv_file_path) == 0:
                                writer.writerow(data.keys())
                            writer.writerow(data.values())


def empirical_matrix():



    size_options = [10, 50, 100, 150, 200, 300, 600]
    seed_options = [1,2,3,4,5]

    size = size_options[1]
    s1, s2 = size, size
    seed = seed_options[0]
    set_options = ['l','m','u']


    t1, t2 = set_options[0], set_options[1]
    for t1, t2 in ((t1, t2) for t1 in set_options for t2 in set_options):

        Y1 = PointList.from_json(f"./instances/subproblems/sp-2-{s1}-{t1}_{seed}.json")*1.5
        Y2 = PointList.from_json(f"./instances/subproblems/sp-2-{s2}-{t2}_{max(seed_options)+1-seed}.json")
        Y = Y1 + Y2

        Yn = N(Y)

        ######################## Figure simple_plot START ########################
        prefix = f'{t1}-{t2}_{s1}_{s2}_{seed}_'
        fig_name = prefix

        print(f"Plotting figure: {fig_name}")
        # define new figure
        fig, ax = plt.subplots(figsize=SIZE_SMALL_SQUARE, layout='constrained')
     
        # ax.axis('off')
        ax.tick_params(left = False, right = False , labelleft = False , 
                    labelbottom = False, bottom = False) 
        Y1.plot(f"${_Y1}$")
        Y2.plot(f"${_Y2}$")
        Y.plot(f"${_Y}$")
        Yn.plot(f"${_Yn}$")


        text_label1 = f"$$|{_Y}| = {len(Y)}$$"
        text_label2 = f"$$|{_Yn}|= {len(Yn)}$$"
        text_label3 = f"$$|{_Yn}| / |{_Y}|= {100 * len(Yn) / len(Y) :0.0f}\%$$"
        # ax.legend(title=text_label1 + '\n' + text_label2 + '\n' + text_label3)
        plt.plot([], [], ' ', label=text_label1)
        plt.plot([], [], ' ', label=text_label2)

        # save or plot figure
        plot_or_save(fig, f"{t1}-{t2}" ) 
        ######################### Figure simple_plot END #########################
    


def RGS_slides():

    Y1 = PointList.from_json('./instances/subproblems/sp-2-10-m_1.json')*2
    Y2 = PointList.from_json('./instances/subproblems/sp-2-10-u_4.json')
    # Y1.points = [y2 for y2 in list(Y1)[::2]]
    point_labels = ['plane1','Plane 2', 'Train','Bus']

    induced_UB_plot('extreme', Y1, Y2, plot= True)

def phase_1_slides():
    

    ######################## Figure phase1_slides START ########################
    fig_name = "phase1_slides"
    print(f"Plotting figure: {fig_name}")
    # define new figure
    fig, ax = plt.subplots(figsize=(6,2), layout='constrained')
    

    plt.xlabel('Objective 1')
    plt.ylabel('Objective 2')
    ax.tick_params(left = False, right = False , labelleft = False , labelbottom = False, bottom = False) 
    plt.xlim(0,5)
    plt.ylim(-100,1100)

    Y = PointList([(1,900),(1, 700),(1.5, 1000),(2.5,660),(3, 500),(3.5, 366 + 2/3),(4, 300)])
    Y[0].cls = 'd'
    Y[1].cls = 'se'
    Y[2].cls = 'd'
    Y[3].cls = 'us'
    Y[4].cls = 'us'
    Y[5].cls = 's'
    Y[6].cls = 'se'
    Ys = PointList([y for y in Y if y.cls =='s'])
    Yse = PointList([y for y in Y if y.cls =='se'])
    Yd = PointList([y for y in Y if y.cls =='d'])
    Yus = PointList([y for y in Y if y.cls =='us'])

    Y.plot_color = 'lightgray'
    line_color = 'black'
    line_width = 0.5
    line = PointList((Point((0,10000)), Y[1], Y[1] - Point((-1,10000))))
    line3 = PointList((Y[1], Y[-1]))
    line2 = PointList((Point((10,0)), Y[-1], Y[-1] + Point((-4,4*300/6))))

    Ys.plot()
    Yse.plot()
    Yus.plot()
    plt.cla()
 

    def draw_triangle(y1,y2,y3):
        X = np.array([y1.val, y2.val, y3.val])
        Y = ['red', 'red', 'red']

        # plt.figure()
        # plt.scatter(X[:, 0], X[:, 1], s=170, color=Y[:])

        # Create the triangle based on the points
        # triangle = plt.Polygon(X, color=Y[0])
        # triangle = plt.Polygon(X, color='lightgray', fill=True, linestyle='--', edgecolor='gray')
        triangle = plt.Polygon(X, color='lightgray', hatch='//', edgecolor='gray')

        plt.gca().add_patch(triangle)


    # draw_triangle(Y[1],Y[2],Y[3])

    plt.xlim(0,5)
    plt.ylim(-100,1100)
    Y.plot(f"${_Y}$")
    plot_count = 1
    plot_or_save(fig, fig_name + str(plot_count))
    plt.cla()
    plt.xlim(0,5)
    plt.ylim(-100,1100)
    plot_count += 1



    Y.plot(f"${_Y}$")
    line.plot(line=True,color = line_color, linestyle='dashed',linewidth=0.5)
    plot_or_save(fig, fig_name + str(plot_count))
    plt.cla()
    plt.xlim(0,5)
    plt.ylim(-100,1100)
    plot_count += 1

    Y.plot(f"${_Y}$")
    line2.plot(line=True,color = line_color, linestyle='dashed',linewidth=line_width)
    line.plot(line=True,color = line_color, linestyle='dashed',linewidth=line_width)
    plot_or_save(fig, fig_name + str(plot_count))
    plt.cla()
    plt.xlim(0,5)
    plt.ylim(-100,1100)
    plot_count += 1

    Y.plot(f"${_Y}$")
    Yse.plot(f"${_Y}_" + '{se}$')
    line3.plot(line=True,color = line_color, linestyle='dashed',linewidth=line_width)
    line2.plot(line=True,color = line_color, linestyle='dashed',linewidth=line_width)
    line.plot(line=True,color = line_color, linestyle='dashed',linewidth=line_width)
    plot_or_save(fig, fig_name + str(plot_count))
    plt.cla()
    plt.xlim(0,5)
    plt.ylim(-100,1100)
    plot_count += 1




    line3.plot(line=True,color = line_color, linestyle='dashed',linewidth=line_width)
    line2.plot(line=True,color = line_color, linestyle='dashed',linewidth=line_width)
    line.plot(line=True,color = line_color, linestyle='dashed',linewidth=line_width)
    Y.plot(f"${_Y}$")
    Yse.plot(f"${_Y}_" + '{se}$')
    Ys.plot(f"${_Y}_" + '{sne}$')
    # Yus.plot(f"${_Y}_" + '{u}$')

    plot_or_save(fig, fig_name + str(plot_count))
    plot_count += 1
    plt.cla()
    plt.xlim(0,5)
    plt.ylim(-100,1100)

    Y.plot(f"${_Y}$")
    Yse.plot(f"${_Y}_" + '{se}$')
    Ys.plot(f"${_Y}_" + '{sne}$')
    Yus.plot(f"${_Y}_" + '{u}$')
    plot_or_save(fig, fig_name + str(plot_count))
    plot_count += 1
    plt.cla()
    
    draw_triangle(Yse[0], Point((3.5,700)),Ys[0] )
    draw_triangle(Yse[-1], Point((4,366+2/3)),Ys[0] )
    plt.xlim(0,5)
    plt.ylim(-100,1100)
    Y.plot(f"${_Y}$")
    Yse.plot(f"${_Y}_" + '{se}$')
    Ys.plot(f"${_Y}_" + '{sne}$')
    Yus.plot(f"${_Y}_" + '{u}$')
    # save or plot figure
    plot_or_save(fig, fig_name + str(plot_count))
    ######################### Figure phase1_slides END #########################


def all_slides():
    ''' Figures for PhD Seminar April 2024 '''
    global FIGURES_LOCATION
    FIGURES_LOCATION = "../../../phd/projects/papers/slidesCORAL/figures/"
    FIGURES_LOCATION = "../../../phd/projects/papers/slidesEURO24/figures/"
#     phase_1_slides()
    # slides_MO_example()
    # # # slides_MS_example()
    # slides_MSP_example()
    slides_matrix_plot()
    RGS_slides()




def MSP_plot():


    file = "prob-2-100|100|100-uuu-3_2.json"
    # file = "prob-5-50|50-uu-2_1.json"
    # file = "prob-2-100|100-mm-2_1.json"

    file = "prob-2-100|100-mm-2_1.json"
    file = "prob-2-100|100-ul-2_2.json"
    file = "prob-2-200|200|200-uuu-3_1.json"
    file = "prob-2-50|50|50-uuu-3_3.json"

    MSP = MinkowskiSumProblem.from_json('./instances/problems/' + file)


    ######################## Figure validate_algorithm2 START ########################
    fig_name = "validate_algorithm2"
    print(f"Plotting figure: {fig_name}")
    # define new figure
    fig, ax = plt.subplots(figsize=SIZE_STANDARD_FIGURE, layout='constrained')
    
    print(f"{len(set(MSP.Y_list[0].points).intersection(set(MSP.Y_list[1].points)))=}")
    
    # matrix_plot(*MSP.Y_list,fig_name = fig, matrix_only=False)
    # matrix_plot(MSP.Y_list[0],MSP.Y_list[0]*3, fig_name = fig, matrix_only=False)
    


    # save or plot figure
    # plot_or_save(fig, fig_name)
    ######################### Figure validate_algorithm2 END #########################

    # return

    # MGS_check = solve_MGS_instance(MSP.Y_list,plot=True)



    MGS, Yn = algorithm2(MSP)
    MSP_reversed = deepcopy(MSP)
    MSP_reversed.Y_list = MSP_reversed.Y_list[::-1]
    MGS_reversed, Yn_reversed = algorithm2(MSP_reversed)

    MGS_size = sum(len(Y) for Y in MGS.Y_list)
    MGS_reversed_size = sum(len(Y) for Y in MGS_reversed.Y_list)
    print(f"{MGS_size=}")
    print(f"{MGS_reversed_size=}")
    assert MGS_size == MGS_reversed_size
    

    print(f"{[(len(Y), len(G)) for G,Y in zip(MSP.Y_list,MGS.Y_list)]=}")
    print(f"{[(len(Y), len(G)) for G,Y in zip(MSP_reversed.Y_list,MGS_reversed.Y_list)]=}")



    for y in MGS.Y_list[0]:
        Y2 = PointList([ymgs for ymgs in MGS.Y_list[0] if ymgs != y])
        print(f"{len(Y2),y=}")
        Y_list_reduced = [MGS.Y_list[1]] + [Y2] + [MGS.Y_list[2]]
        print(f"{[(len(Y), len(G)) for G,Y in zip(MSP.Y_list,Y_list_reduced)]=}")
        assert methods.MS_sequential_filter(Y_list_reduced) == methods.MS_sequential_filter(MSP.Y_list) 
    # print(f"{MGS=}")

    print(f"{Y_list_reduced=}")
    MGS.plot()

    plt.show()


def animate_scalling():

    file = "prob-2-50|50|50-uuu-3_3.json"
    MSP = MinkowskiSumProblem.from_json('./instances/problems/' + file)
    alpha = 3

    ######################## Figure validate_algorithm2 START ########################
    fig_name = "validate_algorithm2"
    print(f"Plotting figure: {fig_name}")
    # define new figure
    fig, ax = plt.subplots(figsize=SIZE_STANDARD_FIGURE, layout='constrained')
    
 
    def update(alpha):
        plt.cla()
        Y1 = MSP.Y_list[0]
        Y2 = MSP.Y_list[1]*alpha
        Y1.plot(f"${_Y1}$")
        Y2.plot(f"${_Y2}$")
        Yn = N(Y1+Y2)
        Yn.plot(f"${_Yn}$")

    # create a slider for alpha which creates a new plot using the new alpha values:

    plt.show()



# def plot_eks():


    # ######################## Figure plot_til_forklaring START ########################
    # fig_name = "plot_til_forklaring"
    # print(f"Plotting figure: {fig_name}")
    # # define new figure
    # fig, ax = plt.subplots(figsize=SIZE_STANDARD_FIGURE, layout='constrained')
   
    # MSP = MinkowskiSumProblem.from_subsets([
        # 'sp-2-50-l_1.json',
         # 'sp-2-50-u_2.json',
    
    
    
    # # save or plot figure
    # plot_or_save(fig, fig_name)
    # ######################### Figure plot_til_forklaring END #########################

def interactive_scaling():

    file = "prob-2-50|50-ul-2_3.json"
    MSP = MinkowskiSumProblem.from_json('./instances/problems/' + file)

    if True:
        MSP = MinkowskiSumProblem.from_subsets([
            # '/sp-2-100-u_1.json',
            # '/sp-2-100-u_2.json',
            # '/sp-2-100-u_3.json',
            'sp-2-50-l_1.json',
             'sp-2-50-u_2.json',
            ])


    alpha = 3

    ######################## Figure validate_algorithm2 START ########################
    # Define the figure and axis
    fig, ax = plt.subplots(figsize=(8, 6))
    plt.subplots_adjust(bottom=0.15)  # Adjust the bottom to make space for the slider
    # Initial plot data
    Y1 = MSP.Y_list[0]
    Y2 = methods.lex_sort(MSP.Y_list[1])[:10]
    alpha_1 = 1
    alpha_2 = 4
    y01, y02 = 0, 0

    y0 = Point((y01, y02))
    alpha = Point((alpha_1, alpha_2))

    # Plot initial data
    Y1 = MSP.Y_list[0] * 4
    Y2 = MSP.Y_list[1]*alpha + PointList((y0,))
    # Y3 = MSP.Y_list[2]
    # Y2 = methods.lex_sort(Y2)[:10]
    Y1.plot(f"${_Y1}$")
    Y2.plot(f"${_Y2}$")
    # Y3.plot(f"${Y3}$")
    Y2_color = Y2.plot_color
    Y = Y1 + Y2
    Y.plot(f"${_Y}$", ax= ax, color = 'gray')
    # Yn = N(Y1+Y2)
    # G,Yn = algorithm2(MSP)

    Yn = N(Y)
    G,Yn = algorithm2(MinkowskiSumProblem([Y1,Y2]))
    for s, g in enumerate(G.Y_list):
        g.plot(f"${_G}^{s}$", color='yellow', marker = 'x')
    Yn.plot(f"${_Yn}$", color = 'yellow')

    # Add legend
    ax.legend()

    # Define the update function
    def update(val):
        ax.clear()  # Clear the current axes
        alpha_1 = slider_3.val
        alpha_2 = slider_4.val
        alpha = Point((alpha_1, alpha_2))
        # also update y0
        y01 = float(textbox_1.text)
        y02 = float(textbox_2.text)
        # y02 = slider_2.val
        y0 = Point((y01, y02))
        Y2 = MSP.Y_list[1] * alpha + PointList((y0,))
        # Y2 = methods.lex_sort(Y2)[:10]
        Y1.plot(f"${_Y1}$", ax=ax, color = Y1.plot_color)
        Y2.plot(f"${_Y2}\cdot \\alpha  + y^0$", ax= ax, color = Y2_color)
        # Y3.plot(f"${_Y1}$", ax=ax, color = Y3.plot_color)
        # Y = Y1 + Y2 + Y3
        Y = Y1 + Y2
        # G,Yn = algorithm2(MinkowskiSumProblem([Y1,Y2]))
        Y.plot(f"${_Y}$", ax= ax, color = 'gray')
        # Yn = N(Y1 + Y2 + Y3)
        Yn = N(Y1 + Y2)

        # G = alg2(MinkowskiSumProblem([Y1,Y2]))
        # print(f"{Y_fixed=}")
        # Yn_with_duplicates, C_dict = SimpleFilter(MSP.Y_list)
        # for s, g in enumerate(Y_fixed):
            # g.plot(f"${_G}^{s}$", color='yellow', marker = 'x', ax=ax)



        Yn.plot(f"${_Yn}$", ax=ax, color= 'yellow')
        y0.plot(ax=ax, label = '$y0$', color = 'black', marker = 'x')

        ax.legend()
        fig.canvas.draw_idle()

    # Define the position of each slider
    ax_slider3 = plt.axes([0.25, 0.05, 0.65, 0.03], facecolor='lightgoldenrodyellow')
    ax_slider4 = plt.axes([0.25, 0.01, 0.65, 0.03], facecolor='lightgoldenrodyellow')

    # Create the sliders
    slider_3 = Slider(ax_slider3, 'Alpha_1', 0.1, 50.0, valinit=alpha_1)
    slider_4 = Slider(ax_slider4, 'Alpha_2', 0.1, 50.0, valinit=alpha_2)

    # update(1)
    slider_3.on_changed(update)
    slider_4.on_changed(update)
        
    # Define the position of each textbox
    ax_textbox1 = plt.axes([0.25, 0.1, 0.25, 0.03], facecolor='lightgoldenrodyellow')
    ax_textbox2 = plt.axes([0.55, 0.1, 0.25, 0.03], facecolor='lightgoldenrodyellow')

    # Create the textboxes
    textbox_1 = TextBox(ax_textbox1, 'y01', initial=str(y01))
    textbox_2 = TextBox(ax_textbox2, 'y02', initial=str(y02))

    textbox_1.on_submit(update)
    textbox_2.on_submit(update)

    # Show the plot
    plt.show()

def interactive_scaling_3d():

    file = "prob-2-50|50-ul-2_3.json"
    MSP = MinkowskiSumProblem.from_json('./instances/problems/' + file)

    if True:
        MSP = MinkowskiSumProblem.from_subsets([
            '/sp-3-10-m_1.json',
            '/sp-3-50-l_1.json',
            ])



    # Create the figure first
    fig = plt.figure(figsize = (30,10))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_axis_off()
    # fig.subplots_adjust(top=1.1, bottom=-.1)
    plt.subplots_adjust(bottom=0.25)  # Adjust the bottom to make space for the slider
    ax.set_aspect('auto')

    # Initial plot data
    Y1 = MSP.Y_list[0]
    Y2 = methods.lex_sort(MSP.Y_list[1])[:10]
    alpha_1 = 2
    alpha_2 = 3
    alpha_3 = 1
    y01, y02, y03 = 0, 0, 0

    y0 = Point((y01, y02, y03))
    alpha = Point((alpha_1, alpha_2, alpha_3))

    # Plot initial data
    Y1.plot(f"${_Y1}$", ax=ax)
    Y2 = MSP.Y_list[1] * alpha + PointList((y0,))
    Y2.plot(f"${_Y2}$", ax=ax)
    Y2_color = Y2.plot_color
    Y = Y1 + Y2
    Y.plot(f"${_Y}$", ax=ax, color='gray')
    Yn = N(Y)
    Yn.plot(f"${_Yn}$", color='yellow', ax=ax)

    # Add legend
    ax.legend()


    # Calculate the new axis limits
    x_max, y_max, z_max = [max([y[p] for y in Y]) for p in range(3)]
    ax.set_xlim([0, 2 * x_max])
    ax.set_ylim([0, 2 * y_max])
    ax.set_zlim([0, 2 * z_max])

    # Plot the vectors
    ax.quiver(0, 0, 0, 2 * x_max, 0, 0, color='black', arrow_length_ratio=0.1)
    ax.quiver(0, 0, 0, 0, 2 * y_max, 0, color='black', arrow_length_ratio=0.1)
    ax.quiver(0, 0, 0, 0, 0, 2 * z_max, color='black', arrow_length_ratio=0.1)



    # Define the update function
    def update(val):
        ax.clear()  # Clear the current axes

        ax.set_xlim([0, 2 * x_max])
        ax.set_ylim([0, 2 * y_max])
        ax.set_zlim([0, 2 * z_max])
        ax.set_axis_off()

        ax.quiver(0, 0, 0, 2 * x_max, 0, 0, color='black', arrow_length_ratio=0.1)
        ax.quiver(0, 0, 0, 0, 2 * y_max, 0, color='black', arrow_length_ratio=0.1)
        ax.quiver(0, 0, 0, 0, 0, 2 * z_max, color='black', arrow_length_ratio=0.1)

        alpha_1 = slider_3.val
        alpha_2 = slider_4.val
        alpha_3 = slider_5.val
        alpha = Point((alpha_1, alpha_2, alpha_3))
        y01 = float(textbox_1.text)
        y02 = float(textbox_2.text)
        y03 = float(textbox_3.text)
        y0 = Point((y01, y02, y03))
        Y2 = MSP.Y_list[1] * alpha + PointList((y0,))
        Y1.plot(f"${_Y1}$", ax=ax, color=Y1.plot_color)
        Y2.plot(f"${_Y2}\cdot \\alpha  + y^0$", ax=ax, color=Y2_color)
        Y = Y1 + Y2
        Y.plot(f"${_Y}$", ax=ax, color='gray')
        Yn = N(Y1 + Y2)
        Yn.plot(f"${_Yn}$", ax=ax, color='yellow')
        y0.plot(ax=ax, label='$y0$', color='black', marker='x')
        ax.legend()
        fig.canvas.draw_idle()

    # Define the position of each slider
    ax_slider3 = fig.add_axes([0.25, 0.05, 0.65, 0.03], facecolor='lightgoldenrodyellow')
    ax_slider4 = fig.add_axes([0.25, 0.10, 0.65, 0.03], facecolor='lightgoldenrodyellow')
    ax_slider5 = fig.add_axes([0.25, 0.15, 0.65, 0.03], facecolor='lightgoldenrodyellow')

    # Create the sliders
    slider_3 = Slider(ax_slider3, 'Alpha_1', 0.1, 50.0, valinit=alpha_1)
    slider_4 = Slider(ax_slider4, 'Alpha_2', 0.1, 50.0, valinit=alpha_2)
    slider_5 = Slider(ax_slider5, 'Alpha_3', 0.1, 50.0, valinit=alpha_3)

    # Connect sliders to the update function
    slider_3.on_changed(update)
    slider_4.on_changed(update)
    slider_5.on_changed(update)

    # Define the position of each textbox
    ax_textbox1 = fig.add_axes([0.2, 0.2, 0.2, 0.03], facecolor='lightgoldenrodyellow')
    ax_textbox2 = fig.add_axes([0.45, 0.2, 0.2, 0.03], facecolor='lightgoldenrodyellow')
    ax_textbox3 = fig.add_axes([0.65, 0.2, 0.2, 0.03], facecolor='lightgoldenrodyellow')

    # Create the textboxes
    textbox_1 = TextBox(ax_textbox1, 'y01', initial=str(y01))
    textbox_2 = TextBox(ax_textbox2, 'y02', initial=str(y02))
    textbox_3 = TextBox(ax_textbox3, 'y03', initial=str(y03))

    # Connect textboxes to the update function
    textbox_1.on_submit(update)
    textbox_2.on_submit(update)
    textbox_3.on_submit(update)

    # Show the plot
    plt.show()



def article_plots_csv():
    ''' ad-hoc script for creating csv-files for plots '''

    # % For each plot I need a csv with columns:
    # %  p1, p2: coordinates 
    # %  subprob: either "1", "2" or "m" (master problem)
    # %  ndom: 1 (if nondom), 0 (otherwise)  (that is for the subprob all equal 1)
    # %  gen: 1 (if generator), 0 (otherwise)    (that is for the master all equal 0)



    # % First subplot: (no scaling)
    # % 'sp-2-50-u_1.json',
    # % 'sp-2-50-u_2.json',
    
    MSP_name_list = []

    

    MSP = MinkowskiSumProblem.from_subsets([
        '/sp-2-50-u_1.json',
        '/sp-2-50-m_2.json',
        ])

    plot_name = "first"
    MSP_name_list.append((MSP, plot_name))

    # % Second subplot: (no scaling)
    # % 'sp-2-50-l_1.json',
    # % 'sp-2-50-u_2.json',

    MSP = MinkowskiSumProblem.from_subsets([
        'sp-2-50-l_1.json',
        'sp-2-50-u_2.json',
        ])

    plot_name = "second"

    MSP_name_list.append((MSP, plot_name))
    # % Third subplot: (no scaling)
    # % 'sp-2-50-m_1.json',
    # % 'sp-2-50-m_2.json',
    # %

    MSP = MinkowskiSumProblem.from_subsets([
        'sp-2-50-m_1.json',
        'sp-2-50-m_2.json',
        ])
    plot_name = "third"
    MSP_name_list.append((MSP, plot_name))

        

    # % Fourth subplot: (2. plot where the u subset have be scalled on lie in [0, 2500]^2)
    # %

    MSP = MinkowskiSumProblem.from_subsets([
        'sp-2-50-l_1.json',
        'sp-2-50-u_2.json',
        ])
    plot_name = "fourth"
    # scale problems

    MSP.Y_list = [MSP.Y_list[0], MSP.Y_list[1]*(1/4)  ]
    MSP_name_list.append((MSP, plot_name))


    for MSP, plot_name in MSP_name_list:

        Y = methods.MS_sum(MSP.Y_list)
        G,Yn = algorithm2(MinkowskiSumProblem(MSP.Y_list))


        with open(f'./temp/plot_{plot_name}.csv', 'w') as out_file:

            csv_writer = csv.writer(out_file)


            for j, y in enumerate(Y):
                y_dir = {
                        'p1' : y[0],
                        'p2' : y[1],
                        'subprob' : 'm',
                        'ndom' : int(y in Yn), 
                        'gen' : 0,
                         }
                
                if j == 0: # write header
                    csv_writer.writerow(y_dir.keys())
                csv_writer.writerow(y_dir.values())

                print(f"{y_dir=}")



            
            for s, Ys in enumerate(MSP.Y_list):
                for ys in Ys:
                    y_dir = {
                            'p1' : ys[0],
                            'p2' : ys[1],
                            'subprob' : s+1,
                            'ndom' : 1,
                            'gen' : int(ys in G.Y_list[s]),
                             }

                    print(f"{y_dir=}")
            
                    csv_writer.writerow(y_dir.values())


            ######################## Figure csv_plot_view START ########################

            # define new figure
            fig, ax = plt.subplots(figsize=(10,7), layout='constrained')
            
            if True:
                MSP.plot()
                G.plot(set_label = 'G', marker= 'x')
                Y.plot(color= 'gray')
                Yn.plot()
                # plt.show()
                fig.savefig(fname = f"temp/{plot_name}.png")
                # plt.cla()
            
            ######################### Figure csv_plot_view END #########################

           



    


def main():

    
    # animate_scalling()


    article_plots_csv()    

    # interactive_scaling()
    # interactive_scaling_3d()

    # MSP_plot()

    # slides_matrix_example_MGS()
    # slides_matrix_plot()

    # RGS_slides()
    # phase_1_slides()
    # all_slides()

    # Week 22, 2024
    # counter_example_reduction()
    # minimum_not_minimal()
    # example_reduction_lower_bounds()


    # all_slides()

    # example()

    # empirical_matrix()
    # plot_ul()
    # klamroth2023_lemma2()
    # example()

    # with plt.style.context('bmh'):

    # with plt.rcParams({"lines.linewidth": 2, "lines.color": "r"}):
    # with matplotlib.rc_context['xtick.bottom']:

    # test_matrix_plot()
    # make_matrix_plot()

    # multiple_induced_UB()



    # induced_UB_plot(0.25)
    # induced_UB_plot(0.50)
    # induced_UB_plot(0.75)
    # induced_UB_plot(1.0)

if __name__ == '__main__':


    SAVE_PLOTS = False 
    if 'save' in sys.argv:
        SAVE_PLOTS = True 
    if 'show' in sys.argv or 'plot' in sys.argv:
        SAVE_PLOTS = False 
    FIGURES_LOCATION = "../../papers/paper1/figures/UB_instances/"
    FIGURES_LOCATION = "../../../phd/projects/papers/paper1/figures/UB_instances/multiple/"
    FIGURES_LOCATION = "../../../phd/projects/papers/paper1/figures/empirical_example/"

    NO_AXIS = False 

    # used figure sizes
    SIZE_STANDARD_FIGURE = (5,2)
    SIZE_SMALL_FIGURE = (2.5,2)
    SIZE_LARGE_FIGURE = (5,3)
    SIZE_SMALL_SQUARE = (3,3)
    SIZE_LARGE_SQUARE = (5,5)
    SIZE_VERY_LARGE_FIGURE = (7,3)

    # Style options for plots
    all_styles = ['Solarize_Light2', '_mpl-gallery', '_mpl-gallery-nogrid', 'bmh', 'classic', 'dark_background', 'fast', 'fivethirtyeight', 'ggplot', 'grayscale',  'tableau-colorblind10']
    # STYLE = "ggplot" 
    STYLE = all_styles[6] # 1 6 8 9 10
    plt.style.use(STYLE)


    if NO_AXIS:
        plt.rcParams['xtick.bottom'] = False
        plt.rcParams['xtick.labelbottom'] = False
        plt.rcParams['ytick.left'] = False
        plt.rcParams['ytick.labelleft'] = False

    # if SAVE_PLOTS:
        # matplotlib.rcParams.update({"pgf.texsystem": "pdflatex",})

    matplotlib.rcParams.update({
            'font.family': 'serif',
            'text.usetex': True,
            'font.size' : 11,
            'pgf.rcfonts': True,
            # 'grid.alpha': 0.0,
            # 'figure.figsize': (8.77, 4.2),
        })

    # latex commands
    _Y = "\mathcal{Y}" # % objective space
    _G = "\mathcal{G}" # % generator set
    _A = "\mathcal{A}" # % a set
    _B = "\mathcal{B}" # % a set
    _U = "\mathcal{U}" # % upper bound set _Yn = "\mathcal{Y}_\mathcal{N}" # % non-dominated objective space
    _L = "\mathcal{L}" # % lower bound set
    _Y1 = "\mathcal{Y}^1" # % objective space 1
    _Y2 = "\mathcal{Y}^2" # % objective space 1
    _L1 = "\mathcal{L}^1" # % lower bound set 1
    _L2 = "\mathcal{L}^2" # % lower bound set 2
    _Yn = "\mathcal{Y}_\mathcal{N}" # % non-dominated objective space
    _Yn1 = "\mathcal{Y}_\mathcal{N}^1" # % non-dominated objective space
    _G1 = "\mathcal{G}^1" # % generator set 1
    _G2 = "\mathcal{G}^2" # % generator set 2
    _Yn2 = "\mathcal{Y}_\mathcal{N}^2" # % non-dominated objective space
    _mcN = "\mathcal{N}" # % Non-dominated set
    _YsS = "\mathcal{Y}^{s|S}" # % Conditioned non-dominated set
    _Gc = "\mathcal{G}^{1|2}" # % set of generators
    _Yc = "\\bar{\mathcal{Y}}^{1}" # % a minimal generator
    _hYc = "\hat{\mathcal{Y}}^{1}" # % (another) minimal generator
    _Yh = "\hat{"+ f"{_Y}" + "}"
    _Yh1 = "\hat{"+ f"{_Y}" + "}^1"
    _Yh2 = "\hat{"+ f"{_Y}" + "}^2"
    _hYn = "\hat{\mathcal{Y}}_\mathcal{N}" # % subset of _Yn
    _Uc = "\\bar{\mathcal{U}}^{1}" # % a conditional upper bound set
    _bY = "\\bar{\mathcal{Y}}" # % bar over objective space
    _bYn = "\\bar{\mathcal{Y}}_\mathcal{N}" # % bar over non-dominated points

    main()
