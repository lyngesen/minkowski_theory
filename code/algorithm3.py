"""
File containing code for algorithm3 answering empirical research question 3

Usage:
    Run to add computational results
    output saved in: ./instances/results/algorithm3/result.csv
"""

from classes import Point, PointList, LinkedList, MinkowskiSumProblem, MSPInstances 
import methods
from methods import N, U_dominates_L
import time
import csv
import math
import os
from minimum_generator import solve_MGS_instance

from algorithm2 import algorithm2

import logging
import random
import numpy as np
# from numoy import linalg
from matplotlib import pyplot as plt
import collections
from scipy.spatial import ConvexHull
from functools import reduce
import itertools
from scipy.optimize import linprog
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


def get_partial(Y, level='all', seed = 0):   
    Y = N(Y)
    Y2e_points = [y for y in Y if y.cls == 'se']
    Y2other_points = [y for y in Y if y.cls != 'se']
    random.seed(seed)
    random.shuffle(Y2other_points)
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

    

def induced_UB_plot(level, Y1,Y2, prefix='', plot=True):
    print(f"{prefix}")
    # print(f"{level=}")

    Y2_partial = get_partial(Y2, level)


    ub_time = time.time()
    U = methods.find_generator_U(Y2_partial, Y1)
    ub_time = time.time() - ub_time

    Uline = methods.induced_UB(U,line=True)
   
    Y2_dominated = [y for y in Y2 if y.cls != 'se' and U.dominates_point(y)]
    dominated_relative = len(Y2_dominated)/len(Y2)
    print(f"dominated: {len(Y2_dominated)} \nrelative: {dominated_relative*100}\%")
    
    run_data = {'prefix' : prefix,
                'Y1_size' : len(Y1),
                'Y2_size' : len(Y2),
                'U' : len(U),
                'U_time' : ub_time,
                'dominated_points' : len(Y2_dominated),
                'dominated_relative_Y2' : dominated_relative,
                }

    return run_data
def multiple_induced_UB():


    set_options = ['l','m','u']
    size_options = [10, 50, 100, 150, 200, 300, 600]
    seed_options = [1,2,3,4,5]
    # UB_options = ['lexmin','extreme','0.25','0.5','0.75','all']
    UB_options = ['extreme']

    csv_file_path = './instances/results/algorithm3/result_slides_alg1_2.csv'
    # get last row
    with open(csv_file_path, 'r') as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            lastrow = row
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
#                         if start_runs == False:
                            # if prefix == lastrow[0]:
                                # start_runs = True
                                # print(f"Starting run after {prefix}")
                            # continue
                        Y1 = PointList.from_json(f"./instances/subproblems/sp-2-{s1}-{t1}_{seed}.json")
                        Y2 = PointList.from_json(f"./instances/subproblems/sp-2-{s2}-{t2}_{max(seed_options)+1-seed}.json")
                        data = induced_UB_plot(ub_level, Y1,Y2, prefix, plot=False) 
                        data.update({'t1':t1, 't2':t2, 's1':s1, 's2':s2,'seed':seed,'ub_level':ub_level})
                        print(f"ALG1 solving Yn")
                        Y = Y1+Y2
                        Yn = N(Y)
                        data.update({'Y_size':len(Y), 'Yn_size':len(Yn)})
                        print(f"Solving MSG")
                        G = solve_MGS_instance([Y1,Y2])
                        data.update({'G1_size':len(G[0]), 'G2_size':len(G[1])})
                        with open(csv_file_path, 'a') as csv_file:
                            # add header if file empty
                            writer = csv.writer(csv_file)
                            if os.path.getsize(csv_file_path) == 0:
                                writer.writerow(data.keys())
                            writer.writerow(data.values())

def induced_LB_3d(Y : PointList, level: int, PLOT = False):

    cnames = {
    # 'aliceblue':            '#F0F8FF',
    # 'antiquewhite':         '#FAEBD7',
    'aqua':                 '#00FFFF',
    'aquamarine':           '#7FFFD4',
    # 'azure':                '#F0FFFF',
    # 'beige':                '#F5F5DC',
    # 'bisque':               '#FFE4C4',
    'black':                '#000000',
    'blue':                 '#0000FF',
    'blueviolet':           '#8A2BE2',
    'brown':                '#A52A2A',
    'burlywood':            '#DEB887',
    'cadetblue':            '#5F9EA0',
    'chocolate':            '#D2691E',
    'coral':                '#FF7F50',
    'cornflowerblue':       '#6495ED',
    'crimson':              '#DC143C',
    'cyan':                 '#00FFFF',
    'darkblue':             '#00008B',
    'darkcyan':             '#008B8B',
    'darkgoldenrod':        '#B8860B',
    'darkgray':             '#A9A9A9',
    'darkgreen':            '#006400',
    'darkkhaki':            '#BDB76B',
    }

    # for colorname, i in enumerate(cnames.keys()):
        # print(f"{colorname,i=}")



    cnames_list = list(cnames.values())
    for _ in range(10):
        cnames_list += cnames_list
    

    def in_hull(Y : PointList, y:Point):
        ''' from https://stackoverflow.com/questions/16750618/whats-an-efficient-way-to-find-if-a-point-lies-in-the-convex-hull-of-a-point-cl '''
        points = Y.as_np_array()
        x = y.val
        n_points = len(points)
        n_dim = len(x)
        c = np.zeros(n_points)
        A = np.r_[points.T,np.ones((1,n_points))]
        b = np.r_[x, np.ones(1)]
        lp = linprog(c, A_eq=A, b_eq=b)
        # print(lp.values())
        if not lp.success:
            return False
        else:
            return sum(1 for x in lp.x if x != 0)
        # return lp.success
    def strict_in_hull(Y : PointList, y:Point):

        if Y.dim ==2:
            return False 
        points = Y.as_np_array()
        epsilon = 1
        x = y.val

        centroid = np.mean(points, axis=0)
        # move all extreme points epsilon distance towards centroid
        for y in points:
            d = centroid - y
            # print(f"{d=}")
            # d = d / np.linalg.norm(d)
            y += d*epsilon

        n_points = len(points)
        n_dim = len(x)
        c = np.zeros(n_points)
        A = np.r_[points.T,np.ones((1,n_points))]
        b = np.r_[x, np.ones(1)]
        lp = linprog(c, A_eq=A, b_eq=b)
        # print(lp.values())
        if not lp.success:
            return False
        else:
            return sum(1 for x in lp.x if x != 0)
        # return lp.success





    def plot_surface(Y,ax,color = 'blue'):

        vertices = [tuple(y.val) for y in Y]
        if Y.dim == 2:
            PointList(vertices).plot(ax=ax, line=True, color=color, alpha = 0.2)
        else:
            ax.add_collection3d(Poly3DCollection([vertices], color=color, alpha = 0.2))

    def hull_sort(F: PointList):
        print(f"{len(F)=}")
        hull = ConvexHull(np.array([y.val for y in all_points]))
        FACES = tuple(PointList([y for i,y in enumerate(F) if i in sim]) for sim in hull.simplices)
        print(f"sdsad {len(FACES)=}")
        # assert len(FACES) == 1
        return FACES[0]

    def sort_polygon_vertices(Y:PointList):
        # Calculate the centroid of the polygon
        # centroid = y_bar.val

        vertices = np.array([y.val for y in Y])
        # print(f"{vertices=}")
        centroid = np.mean(vertices, axis=0)
        # centroid = reduce(Point.__add__, Y) * (1/len(Y))
        # Calculate the angles between each vertex and the centroid
        angles = np.arctan2(vertices[:, 1] - centroid[1], vertices[:, 0] - centroid[0])
        
        # Sort the vertices based on the angles
        sorted_indices = np.argsort(angles)
        sorted_vertices = vertices[sorted_indices]
        return PointList(sorted_vertices)

    def plot_dominated_cone(point):
        pass

    def split_faces(FACES) -> list[PointList]:

        F_splits = []
        for f, F in enumerate(FACES):
            y_bar = reduce(Point.__add__, F) * (1/len(F))
            for i1,y1 in enumerate(F):
                    # F_noy1 = PointList([y for y in F if y != 0])
                    F_noy1 = PointList([y for y in F ])
                    # edge_points = [ye := (y1+y2)*(1/2) for i2,y2 in enumerate(F) if (y1 != y2 and not strict_in_hull(F_noy1,ye))]
                    edge_points = [(y1+y2)*(1/2) for i2,y2 in enumerate(F) if (y1 != y2)]
                    edge_points_outer = []
                    for ye in edge_points:
                        if not strict_in_hull(F, ye):
                            edge_points_outer.append(ye)
                    edge_points = edge_points_outer

                    for ye in edge_points:
                        # print(f"{F}")
                        assert in_hull(F, ye)
                    # new_face = PointList([y1]  + [y_bar]+ [y for y in edge_points])
                    new_face = PointList([y1]  + [y_bar]+ [y for y in edge_points])
                    new_face = sort_polygon_vertices(new_face)
                    # new_face.plot(ax=ax, l='{p}')
                    # plot_surface(new_face, ax, color = cnames_list[i1])
                    if len(new_face)>Y.dim-1:
                    # if True:
                        F_splits.append(new_face)

        return F_splits

    # fig = plt.figure()
    # ax= plt.axes(projection = '3d')
    all_points = PointList(list(Y.points) + [Y.get_nadir()])
    hull = ConvexHull(np.array([y.val for y in all_points]))
    # hull = ConvexHull(all_points.as_np_array())
    # Y = [PointList([y for i,y in enumerate(Y) if i in F]) for F in hull.simplices][4]
    # plot_surface(Y,ax)

    ZERO = Point([0 for _ in range(Y.dim)])
    nadir_point = Y.get_nadir()
    # nadir_point.plot(ax=ax,l=f"$y^N$")
    # ZERO.plot(ax=ax,l=f"$0$")
    if False: # plot axis lines
        for p in range(nadir_point.dim):
            unit_point = Point([nadir_point[q] if q ==p else 0 for q in range(nadir_point.dim)])
            unit_point.plot(ax=ax,l=f"$obj^{p}$", color='black')
            PointList([ZERO, unit_point]).plot(ax=ax, line=True, color='black')


    all_points = PointList(list(Y.points) + [nadir_point])
    hull = ConvexHull(np.array([y.val for y in all_points]))
    # hull = ConvexHull(np.array([y.val for y in Y]))
    # print(f"{hull.simplices=}")



    # FACES = tuple(hull.simplices)
    FACES = [PointList([y for i,y in enumerate(Y) if i in F]) for F in hull.simplices]

    if False:
        F_splits = []
        for f, F in enumerate(FACES):
            # if len(Y) in sim: #skip faces with nadir_point
                # print(f"skipping {sim}")
                # continue
            # y_bar = Point(sum([y for y in surfacePoints])/len(surfacePoints))

            # if f == 14:
            if True:
                # plot_surface(F, ax, color = cnames_list[f])
                y_bar = reduce(Point.__add__, F) * (1/len(F))
                y_bar.plot(ax=ax, l=r"$\bar{y}^{" + str(f) + "}$", color = 'black')
                l = F.get_ideal()
                u = F.get_nadir()
                l.plot(ax=ax, color = cnames_list[f])

                # F.plot(ax=ax,point_labels=True)
                # project y_bar onto each axis
                if True:
                    for i1,y1 in enumerate(F):
                        edge_points = [(y1+y2)*(1/2) for i2,y2 in enumerate(F) if y1 != y2]
                        new_face = PointList([y1]  + [y_bar]+ [y for y in edge_points])
                        new_face = sort_polygon_vertices(new_face)
                        new_face.plot(ax=ax, l='{p}')
                        plot_surface(new_face, ax, color = cnames_list[i1])
                        F_splits.append(new_face)
                        
                if False: # plot axis lines
                    edge_points = [(y1+y2)*(1/2) for (i1,y1) in enumerate(F) for i2,y2 in enumerate(F) if i1 < i2]
                    PointList(edge_points).plot(ax=ax,l=f"e", color = 'yellow')
                    for p in range(nadir_point.dim):
                        if p != 1:
                            pass
                            # continue
                        unit_point = Point([nadir_point[q] if q ==p else 0 for q in range(nadir_point.dim)])
                        projection = Point([y_bar[q] if q ==p else l[q] for q in range(nadir_point.dim)])
                        unit_point.plot(ax=ax,l=f"$obj^{p}$", color='black')
                        # projection = l + avg_direction
                        projection.plot(ax=ax,l=f'{p}')
                        PointList([l, unit_point + l]).plot(ax=ax, line=True, color='black')
                
                        # new_face = PointList([y for y in F if l[p] != y[p]] + [y_bar])
                        new_face = PointList([y for y in F if projection < y]  + [y_bar]+ [y for y in edge_points if projection < y])
                        # new_face = methods.lex_sort(new_face)
                        new_face = sort_polygon_vertices(new_face)
                        new_face.plot(ax=ax, l='{p}')
                        print(f"{len(new_face)=}")
                        print(f"{new_face.points}")
                        plot_surface(new_face, ax, color = cnames_list[f+p])
                        F_splits.append(new_face)

    # plt.show()


    for _ in range(level):
        print(f"{len(FACES)=}")


        if True:

            if PLOT:
                fig = plt.figure()
                if Y.dim == 3:
                    ax= plt.axes(projection = '3d' if Y.dim ==3 else '2d')
                    # ax.view_init(elev=-10., azim=200)
                    # ax.dist = 5
                else:
                    ax= plt.axes()
                Y.plot(ax = ax, l=r"$\mathcal{Y}$", color='red')
                # print(f"{F_splits=}")
            for f, F in enumerate(FACES):
                l = F.get_ideal()
                assert all((l <= y for y in F))
                if PLOT and len(F)>2:
                    # F.plot(ax=ax,point_labels=False)
                    l.plot(ax=ax, color = cnames_list[f])
                    plot_surface(F, ax, color = cnames_list[f])


        FACES = split_faces(FACES)

        # if _ == 0:
            # FACES = [FACES[1]]

    if PLOT: 
        plt.show()


    # return PointList(itertools.chain.from_iterable(((f.ideal for f in F) for F in FACES)))
    L = PointList((f.get_ideal() for f in FACES))
    return L

def algorithm3_pair(L_Y_U: list[list[PointList]]) -> list[PointList]:
    ((L1, Y1, U1), (L2, Y2, U2)) = L_Y_U
    U = methods.N(U1 + U2)
    

    Y1_dom = set()
    for y1 in Y1:


        if U < y1 + L2:
            print(f"{y1=} is dominated")
            Y1_dom.add(y1)
    G1 = PointList((y1 for y1 in Y1 if y1 not in Y1_dom))
    # repeat
    Y2_dom = set()
    for y2 in Y2:

        if U < y2 + L1:
            print(f"{y2=} is dominated")
            Y2_dom.add(y2)
    G2 = PointList((y2 for y2 in Y2 if y2 not in Y2_dom))
 
    print(f"{len(G1),len(Y1)=}")
    print(f"{len(G2),len(Y2)=}")
    

    if True:
        fig = plt.figure()
        if Y1.dim == 3:
            ax= plt.axes(projection = '3d')
        else:
            ax= plt.axes()
        print(f"{U < y2 + L1=}")
        L1.plot(ax=ax,l=f"L^1")
        L2.plot(ax=ax,l=f"L^2")
        U1.plot(ax=ax,l=f"U^1")
        U2.plot(ax=ax,l=f"U^2")
        U.plot(ax=ax,l=f"U")
        Y1.plot(ax=ax,l=f"Y^1")
        Y2.plot(ax=ax,l=f"Y^2")
        if Y2_dom:
            PointList(Y2_dom).plot(ax=ax, marker='x', color='black')
        if Y1_dom:
            PointList(Y1_dom).plot(ax=ax, marker='x', color='black')
        y2.plot(ax=ax,l='y2', label_only=True)
        (y2 + L1).plot(ax=ax,l='y2 + L1')
        # plt.show()
        return


    return (G1,G2)

def test_alg_3():



    files = [
            './instances/subproblems/sp-2-100-m_1.json',
             './instances/subproblems/sp-2-100-u_1.json'
             ]

    for level in [0,1,2]:
        L_Y_U = list()
        for i, file in enumerate(files):
            Y = methods.lex_sort(PointList.from_json(file))
            # assert Y == methods.N(Y)
            Yse = PointList([y for y in Y if y.cls =='se'])


            L = methods.N(induced_LB_3d(Yse, level, PLOT=False))
            U = Yse
            L_Y_U.append((L,Y,U))

            # Y.plot(ax=ax, l=f"$Y^{i}$")
            # L.plot(ax=ax, color=Y.plot_color, marker=1)
            # U.plot(ax=ax, color=Y.plot_color, marker=2)
        # plt.show()
        # U.plot(SHOW=True)
        algorithm3_pair(L_Y_U)
    plt.show()





def setup_instances():

    L_Y_U_list = list()

    Y = PointList.from_json('instances/subproblems/sp-2-100-u_1.json')
    Yse = PointList([l for l in Y if l.cls =='se'])
    L_Y_U_list.append((L,Y,U))


    Y = PointList.from_json('instances/subproblems/sp-2-10-l_1.json')
    Yse = PointList([l for l in Y if l.cls =='se'])
    L_Y_U_list.append((L,Y,U))


    Y = PointList.from_json('instances/subproblems/sp-2-10-m_1.json')
    Yse = PointList([l for l in Y if l.cls =='se'])
    L_Y_U_list.append((L,Y,U))

    return L_Y_U_list



def pairwise_alg3(L1, Y1, U1, L2, Y2, U2):
    """Implementation of the pairwise algorithm3
    Returns: Subset Y_hat of Y1
    """

    U = N(U1 + U2)
    G1_not = []
    for y1 in methods.lex_sort(Y1):
        L = L2 + PointList(y1)
        L.is_complete = L2.is_complete

        if U_dominates_L(U,L):
            G1_not.append(y1)

    # G1 = PointList([y1 for y1 in Y1 if y1 not in G1_not])
    G2_not = []
    for y2 in methods.lex_sort(Y2):
        L = L1 + PointList(y2)
        L.is_complete = L1.is_complete

        if U_dominates_L(U,L):
            G2_not.append(y2)

    # G2 = PointList([y2 for y2 in Y2 if y2 not in G2_not])
    
    if True: # validate resutlts
        for y1 in G1_not:
            assert y1 in Y1, f"{y1,Y1=}"

        for y2 in G2_not:
            assert y2 in Y2

    return (G1_not,G2_not)




def all_pairs_alg3():
    
    Y1 = methods.lex_sort(PointList.from_json('instances/subproblems/sp-2-10-m_1.json'))
    Y1se = PointList([l for l in Y1 if l.cls =='se'])
    Y2 = methods.lex_sort(PointList.from_json('instances/subproblems/sp-2-50-l_1.json'))
    Y2se = PointList([l for l in Y2 if l.cls =='se'])


    if False:

        # '/sp-2-50-l_1.json',
        # '/sp-2-50-u_1.json'
        Y1 = methods.lex_sort(PointList.from_json('instances/subproblems/sp-2-50-l_1.json'))
        Y1se = PointList([l for l in Y1 if l.cls =='se'])
        Y2 = methods.lex_sort(PointList.from_json('instances/subproblems/sp-2-50-u_1.json'))
        Y2se = PointList([l for l in Y2 if l.cls =='se'])

    U1_line = methods.induced_UB(Y1se, line = True)
    U2_line = methods.induced_UB(Y2se, line = True)

    # U1 = methods.induced_UB(Y1se, line = False)
    # U2 = methods.induced_UB(Y2se, line = False)
    U1 = Y1se
    U2 = Y2se

    G1_not, G2_not = pairwise_alg3(Y1se, Y1, Y1se, Y2se, Y2, Y2se)
    

    def plot_sets():
        Y1.plot('Y1')
        Y2.plot('Y2')
        Y1se.plot('Y1se', line=True, linestyle = 'dashed', color = Y1.plot_color)
        Y2se.plot('Y2se', line =True, linestyle = 'dashed', color = Y2.plot_color)
        U1_line.plot('U1', line =True, linestyle = 'dashed', color = Y1.plot_color)
        U2_line.plot('U1', line =True, linestyle = 'dashed', color = Y2.plot_color)

        PointList(G1_not).plot(marker='x', color = 'black')
        PointList(G2_not).plot(marker='x', color = 'black')
    

    print(f"{len(G1_not),len(Y1)=}")
    print(f"{len(G2_not),len(Y2)=}")


    if True: # validate
        for y1 in Y1[::math.floor(len(Y1)/5)]:
            plot_sets()
            U = N(U1 + U2)
            L = PointList(y1) + Y2se
            U.plot('U')
            U_line = methods.induced_UB(U, line = True)
            U_line.plot(line=True)
            L.plot(line=True)
            L.plot('L')
            PointList(y1).plot('y1', marker = 'x')
            y1.plot('y1', label_only=True)
            print(f"{U_dominates_L(U, L)=}")
            plt.show()
            # return
            if y1 in G1_not:
                assert U_dominates_L(U, L)


def algorithm3_run(MSP,levels = None, logger = None):
    """ The actual function used for results """
    if levels is None:
        levels = [0 for s in range(MSP.S)]
    

    time_start = time.time()

    print(f"{MSP.S=}")
    Y_list = [methods.lex_sort(Y) for Y in MSP.Y_list]
    # Yse_list = [PointList([y for y in Y if y.cls == 'se']) for Y in MSP.Y_list]

    print(f"{MSP.filename=}")

    L_list = []
    U_list = []

    for s in range(MSP.S):
        if levels[s] == 1 or levels[s] == 'all':
            Ls = MSP.Y_list[s]
            if levels[s] == 'all':
                Ls.is_complete = True
        else:
            Ls = get_partial(MSP.Y_list[s], 0) # only se points
            Ls.is_complete = False # convex hull of Ls points
        L_list.append(Ls)

    
        if levels[s] == 'all':
            U_list.append(get_partial(MSP.Y_list[s], 1))
        else:
            U_list.append(get_partial(MSP.Y_list[s], levels[s]/100, seed = MSP.filename))

            
    print(f"{[len(Y) for Y in MSP.Y_list]=}")
    print(f"{[len(U) for U in U_list]=}")

    G_not_list = [set() for _ in range(MSP.S)]

    for s1, Y1 in enumerate(MSP.Y_list):
        
        for s2, Y2 in enumerate(MSP.Y_list):
            if s1 >= s2: continue 

            # Y1se = Yse_list[s1]
            # Y2se = Yse_list[s2]
            # G1_not, G2_not = pairwise_alg3(Y1se, Y1, Y1se, Y2se, Y2, Y2se)
            G1_not, G2_not = pairwise_alg3(L_list[s1], Y1, U_list[s1], L_list[s2], Y2, U_list[s2])

            print(f"{len(set(G1_not))=}")
            print(f"{len(set(G2_not))=}")
            print(f"{G1_not=}")
            print(f"{G2_not=}")
            for y1 in G1_not:
                G_not_list[s1].add(y1)
            
            for y2 in G2_not:
                G_not_list[s2].add(y2)
            print(f"{len(G_not_list[s1])=}")
            print(f"{len(G_not_list[s2])=}")

    print(f"{G_not_list=}")

    for s in range(MSP.S):
        print(f"")
        print(f"|Y{s}| = {len(Y_list[s])}")
        print(f"|G_not{s}| = {len(G_not_list[s])}")
        print(f"")


    if False: # plot
        for s, Y in enumerate(MSP.Y_list):
            Y.plot(f'Y{s}')
        for s, Y in enumerate(MSP.Y_list):
            PointList(G_not_list[s]).plot(f'not {s}',marker='x')


        plt.show()

    RGS = MinkowskiSumProblem([PointList(G_not) for G_not in G_not_list])

    MGS, Yn = algorithm2(MSP, logger)

    statistics = {
            '|G_sizes|': [len(G_not) for G_not in RGS.Y_list],
            'removed': [len(G_not) for G_not in RGS.Y_list],
            'removed_unknown': [len([g for g in G_not if g not in Us]) for G_not, Us in zip(RGS.Y_list, U_list)],
            'RGS_size': [len(Ys)- len(G_not) for G_not,Ys in zip(RGS.Y_list, MSP.Y_list)],
            '|Ys|-|Gs|_sizes': [len(Ys) - len(Gs) for (Ys,Gs) in zip(MSP.Y_list, MGS.Y_list)],
            '|G_not_sizes_total|': sum([len(G_not) for G_not in RGS.Y_list]),
            'running_time_RGS': time.time() - time_start,
            'known': [len(Us) for Us in U_list],
            'known_relative': [len(Us)/len(Ys) for Us, Ys in zip(U_list, MSP.Y_list)],
            'q_stats': [len(G_not_list[s])/(len(MSP.Y_list[s]) - len(MGS.Y_list[s])) if (len(MSP.Y_list[s]) - len(MGS.Y_list[s])) != 0 else None  for s in range(MSP.S) ],
            'q_stats_unknown': [len(G_not_list[s].difference(U_list[s]))/(len(MSP.Y_list[s]) - len(MGS.Y_list[s])) if (len(MSP.Y_list[s]) - len(MGS.Y_list[s])) != 0 else None  for s in range(MSP.S) ],
            'L_is_U': [Ls.is_complete for Ls in L_list],
            'any_L_is_U': any([Ls.is_complete for Ls in L_list])
            }

    print(f"{statistics=}")

    # add statistics from MGS
    statistics.update(MGS.statistics)
    
    RGS.statistics = statistics

    print(f"{RGS.statistics=}")

    

    return RGS

    pass




def test_algorithm3_run():



    # for logging
    logname = 'algorithm3.log'
    logging.basicConfig(level=logging.DEBUG, 
                        filename=logname,
                        format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
                        )

    logger = logging.getLogger(logname)





    MSP = MinkowskiSumProblem.from_subsets([
        '/sp-2-10-m_1.json',
        '/sp-2-50-l_1.json',
        '/sp-2-50-u_1.json'
        ])

    # TI = MSPInstances(preset = 'algorithm1', p_options = (2,), m_options = (2,3,4), size_options = (100,200,), seed_options = (1,) ,ignore_ifonly_l=True)
    TI = MSPInstances(p_options = (2,), m_options = (2,3,4), size_options = (50, 100, 200, 300), seed_options = (1,2,3,4,5) ,ignore_ifonly_l=True)
    # TI = MSPInstances(p_options = (2,), m_options = (2,3), size_options = (50, 100,200, 300), seed_options = (1,) ,ignore_ifonly_l=True)

    save_solution_dir = './instances/results/algorithm3_partial_levels/'
    save_prefix = 'alg3-'
    TI.filter_out_solved(save_prefix, save_solution_dir)

    print(f"{TI=}")


    # return
    # MSP = MinkowskiSumProblem.from_json('./instances/problems/prob-2-100|100|100|100-uull-4_2.json')
    # MSP = MinkowskiSumProblem.from_json('./instances/problems/prob-2-300|300-ul-2_3.json')


    all_partial_levels = [0,25,50,75,100, 'all']

    
    solved_instances = set(os.listdir(save_solution_dir))

    for MSP in TI:
    # for MSP in [MinkowskiSumProblem.from_json('./instances/problems/prob-2-50|50|50-ull-3_1.json')]:
    # if True:

        # MSP = MinkowskiSumProblem.from_json('./instances/problems/prob-2-50|50-ul-2_1.json')
        

        for levels in itertools.product(*[all_partial_levels for s in range(MSP.S)]):
        # for levels in [(75,74, 73)]:

            RGS_filename = save_prefix + MSP.filename.split('/')[-1].replace('.json', '-' + '|'.join((str(l) for l in levels)) + '.json' )

            
            # or tuple([(l if not isinstance(l, str) else 101) for l in levels]) != tuple(sorted([(l if not isinstance(l, str) else 101) for l in levels])):
            # only two kinds of levels, selv and other same lambda value
            level_count_dict = collections.Counter(levels)
            if len([v for v in level_count_dict.values() if v > 0]) > 2 or  len([v for v in level_count_dict.values() if v > 1]) > 1: 
                logger.debug(f"Skipping, not valid combination {levels=}")
                continue
            
            

            # if "all" in levels and MSP.S != 2:
                # logger.debug(f"Skipping, only all for p=2 {levels=}")
                # continue

            if RGS_filename in solved_instances:
                logger.debug(f"Skipping, already solved {RGS_filename=}")
                continue

            # print(f"{MSP=}")
            # print(f"{levels=}")

            logger.info("SOLVING " + RGS_filename )
            RGS = algorithm3_run(MSP, levels=levels, logger=logger)

            # print(f"{RGS_filename=}")
            logger.info("SOLVED " + RGS_filename )
            print(f"{RGS.statistics=}")
            RGS.save_json(save_solution_dir + RGS_filename)
            logger.info("SAVED " + RGS_filename )



def result_validation():


    # check that no points of G_not_s is in G_s

    pass

def main():
    
    if False:
        Y = PointList.from_json('./instances/subproblems/sp-2-10-l_1.json')
        Y = PointList([y for y in Y if y.cls =='se'][1:3])
    else:
        Y = PointList.from_json('./instances/subproblems/sp-3-10-l_1.json')
        Y = PointList([y for y in Y if y.cls =='se'][2:5])
    L = induced_LB_3d(Y, 3, PLOT=True)

    # L.plot(SHOW=True)

    # multiple_induced_UB()

if __name__ == '__main__':
    # test_alg_3() 
    # pairwise_alg3()
    # main()


    test_algorithm3_run()
    # all_pairs_alg3()
