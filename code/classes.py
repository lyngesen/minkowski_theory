from dataclasses import dataclass
import numpy as np
import matplotlib.pyplot as plt
import csv
# from itertools.collections import Counter
import collections

"""
Class
@Point

y1 = Point((4,2))
y2 = Point([3,2])

y1 < y2
>> False
t2 <= y1 
>> True


Class
@PointList 

Y1 = PointList((y1, y2))
Y2 = PointList((y2))
Y3 = PointList.from_csv(fname)

Y1 == Y2
>> False, since counter is off Y1:{y1: 1, y2: 1}, while Y2: {y2: 1}

Y3.save_csv(fname)
>> saves the list to a csv file with name fname

Y1.plot()
> plots set of points, if True plt.show() is called

Y2.dominates_point(y1)
>> True if the point y1 is dominated by the set Y2


"""

@dataclass
class Point:
    val: np.array(iter)
    dim = None
    plot_color = None

    def __post_init__(self):
        self.val = np.array(self.val)
        self.dim = len(self.val)
    def __lt__(self, other):
        if all(self.val == other.val):
            return False
        return all(self.val <= other.val)

    def __le__(self, other):
        return all(self.val <= other.val)
    
    def strictly_dominates(self, other):
        return all(self.val < other.val)

    def lex_le(self, other):
        assert len(self.val) == 2, " lex_le only implemented for p=2"
        if self.val[0] > other.val[0]:
            return False
        if self.val[0] < other.val[0]:
            return True
        if self.val[0] == other.val[0] and self.val[1] > other.val[1]:
            return False
        else:
            return True


    def __gt__(self, other):
        if all(self.val == other.val):
            return False
        return all(self.val >= other.val)
    def __iter__(self):
        return self.val.__iter__()
    def __hash__(self):
        return tuple(self.val).__hash__()
    def __eq__(self, other):
        return (self.val == other.val).all()
    def __repr__(self):
        return tuple(self.val).__repr__()
    def __getitem__(self, item):
        return self.val[item]
    def __add__(self, other):
        if isinstance(other, PointList):
            return PointList((self,)) + other

        return Point(self.val + other.val)
    def __sub__(self, other):
        return Point(self.val - other.val)
    def __mul__(self, other):
        if isinstance(other, int):
            return Point(self.val * other)
        elif isinstance(other, float):
            return Point(self.val * other)
        elif isinstance(other, Point):
            return Point(self.val * other.val)
        else:
            raise TypeError(f'__mul__ not implemented for {type(other)=}')
    

    def plot(self, SHOW = False, fname = None, ax = None, l =None,label_only = False, color = None,  **kwargs):
        assert self.dim<=3, 'Not implemented for p > 3'
        ax = ax if ax else plt
        color = color if (color is not None) else self.plot_color
        kwargs['color'] = color
        if self.dim == 3: 
            ax.scatter = ax.scatter3D

        if not label_only:
            plot = ax.scatter(*self.val, **kwargs)
            self.plot_color = plot.get_facecolor()
        if l != None:
            if self.dim == 3:
                ax.text(*self.val, l)
            else:
                ax.annotate(text=l, xy= self.val, xytext=self.val*1.02 )
                
        if l != None:
            ax.legend(loc="upper right") 
        if fname:
            ax.savefig(fname, dpi= 200)
            ax.cla()
        if SHOW:
            ax.show()
        return ax 


@dataclass
class PointList:
    points: tuple[Point] = ()
    dim = None
    plot_color = None
    def __post_init__(self):
        # Check if SINGLETON: allows for PointList((y)) where y is of class Point 
        if isinstance(self.points, Point):
            self.points = (self.points,)
        else: #unpack list
            self.points = tuple([y if isinstance(y, Point) else Point(y) for y in self.points])
        self.dim = self.points[0].dim

    def __iter__(self):
        return tuple(self.points).__iter__()
    def __len__(self):
        return tuple(self.points).__len__()
    
    def plot(self,  l =None,SHOW = False, fname = None, ax= None, line=False, color = None, point_labels = False, **kwargs):
        ax = ax if ax else plt
        assert self.dim<=3, 'Not implemented for p > 3'
        # color = self.plot_color if (color is not None) else color
        color = color if (color is not None) else self.plot_color
        kwargs['color'] = color
        
        if self.dim == 3: 
            ax.scatter = ax.scatter3D
            ax.plot = ax.plot3D

        if line:
            plot = ax.plot(*zip(*self.points), label =l, **kwargs)
            self.plot_color = plot[-1].get_color()
        else:
            plot = ax.scatter(*zip(*self.points), label =l, **kwargs)
            # self.plot_color = plot.to_rgba(-1) # save used color to object
            self.plot_color = plot.get_facecolors()
        if l:
            ax.legend(loc="upper right") 
        if fname:
            plt.savefig(fname, dpi= 200)
            plt.cla()
        if point_labels:
            # add labels to points
            for i,y in enumerate(self, start = 1):
                y.plot(ax = ax, l=f"$y^{i}$", label_only=True)
           

                
        if SHOW:
            ax.show()

        return ax

    def dominates_point(self, point:Point):
        for y in self.points:
            if y < point:
                return True
        return False


    def __add__(self,other):
        """
        input: list of two PointList
        output: Minkowski sum of sets
        """
        return PointList([y1 + y2 for y1 in self for y2 in other])

    def __sub__(self,other):
        """
        input: list of two PointList
        output: Minkowski subtration of sets
        """
        return PointList([y1 - y2 for y1 in self for y2 in other])






    def dominates(self, other, power="default"):
        match power:
            case "default":
                if self == other:
                    return False
                for y in other.points:
                    if any((l <= y for l in self.points)):
                        continue
                    else:
                        return False
                return True

            case "strict":
                for y in other.points:
                    if any((l < y for l in self.points)):
                        continue
                    else:
                        return False
                return True


    def save_csv(self, filename="testsets/disk.csv"):
        with open(f"{filename}", "w") as out:
            csv_out=csv.writer(out)
            for y in self.__iter__():
                csv_out.writerow(y)   

    def from_csv(filename = "disk.csv"):
        with open(f"{filename}", "r") as csvfile:
            points = []
            for y in csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC):
                #points.append(Point(tuple(map(float,y))))
                points.append(Point(y))
            # self.points = points
            return PointList(points)

    def print_data(self):
        N_POINTS = len(self.points)
        print(f"{N_POINTS=}")

    def __eq__(self, other):
        return collections.Counter(self.points) == collections.Counter(other.points)
    
    def __getitem__(self, item):
        return self.points[item]

    def removed_duplicates(self):
        return PointList(set(self.points))


class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None

    def __repr__(self):
        return f"{str(self.data)}"

class LinkedList:
    def __init__(self):
        self.head = None

    def __repr__(self):
        node = self.head
        nodes = []
        while node is not None:
            nodes.append(str(node.data))
            node = node.next
        nodes.append("None")
        return " -> ".join(nodes)

    def __iter__(self):
        node = self.head
        # while node is not None:
        while node is not None:
            yield node
            node = node.next

    def add_first(self, node):
        node.next = self.head
        self.head = node
        self.prev = None

    def add_after(self, target_node_data, new_node):
        if self.head is None:
            raise Exception("List is empty")

        for node in self:
            if node.data == target_node_data:
                new_node.next = node.next
                node.next = new_node
                return

        raise Exception("Node with data '%s' not found" % target_node_data)


    def add_before(self, target_node_data, new_node):
        if self.head is None:
            raise Exception("List is empty")

        if self.head.data == target_node_data:
            return self.add_first(new_node)

        prev_node = self.head
        for node in self:
            if node.data == target_node_data:
                prev_node.next = new_node
                new_node.next = node
                return
            prev_node = node

        raise Exception("Node with data '%s' not found" % target_node_data)


    def remove_node(self, target_node_data):
        if self.head is None:
            raise Exception("List is empty")

        if self.head.data == target_node_data:
            self.head = self.head.next
            return

        previous_node = self.head
        for node in self:
            if node.data == target_node_data:
                previous_node.next = node.next
                return
            previous_node = node

        raise Exception("Node with data '%s' not found" % target_node_data)


