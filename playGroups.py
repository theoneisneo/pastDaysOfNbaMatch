import sys
import time
import matplotlib.pyplot as plt
import networkx as nx


class UnionFind():
    def __init__(self):
        # the group below is a "set".
        self.leader = {}  # dict, key: group member, value: group's leader
        self.group = {}  # dict, key: group's leader , value: group
        
    def makeSet(self, member):
        if member not in self.leader:
            self.leader[member] = member
            self.group[member] = set([member])
    
    def link(self, member1, member2):
        leader1 = self.leader.get(member1)  # if a is not in self.leader, would get None.
        leader2 = self.leader.get(member2)

        if leader1 is not None:
            if leader2 is not None:
                if leader1 == leader2:  # a and b are in the same group already.
                    return None
                
                group1 = self.group[leader1]
                group2 = self.group[leader2]
                
                if len(group1) < len(group2):
                    leader1, leader2 = leader2, leader1
                    group1, group2 = group2, group1
                group1 |= group2  # union group1 and group2, and assign value to variable group1
                del self.group[leader2]  # no need it anymore
                for k in group2:
                    self.leader[k] = leader1  # update leader
            else:
                # member2 has no leader, just add to group of leader1 and update leader value
                self.group[leader1].add(member2)
                self.leader[member2] = leader1
        else:
            if leader2 is not None:
                # member1 has no leader, just add to group of leader2 and update leader value
                self.group[leader2].add(member1)
                self.leader[member1] = leader2
            else:
                self.leader[member1] = member1
                self.leader[member2] = member1
                self.group[member1] = set([member1, member2])


past_days = int(sys.argv[1])
uf = UnionFind()
g = nx.Graph()
file = 'played.txt'
fp = open(file, 'r')
for line in fp:
    x = line[:-1].split(' ')
    if int(x[0][-2:]) >= 12 - past_days:
        uf.makeSet(x[-1])
        uf.makeSet(x[-3])
        uf.link(x[-1], x[-3])
        g.add_edge(x[-1], x[-3])
fp.close()

print(f"teams have played: {len(uf.leader)}")
print(f"group(s): {len(uf.group)}")
pos = nx.spring_layout(g)
nx.draw(g, pos, with_labels=True, font_size=9, node_size=400, font_color='b', node_color='r')
plt.plot()
plt.savefig(f"past_{past_days}_days_{time.time()}.png")
# plt.show()
