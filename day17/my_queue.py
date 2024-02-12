import math


class MinHeapQueue(object):
    def __init__(self):
        self.p_to_els = {}
        self.el_to_p = {}
        self.min_ps = [math.inf]
        self.len = 0

    def __len__(self):
        return self.len

    def push(self, el, prio):
        if prio not in self.p_to_els:
            self.p_to_els[prio] = []
        self.p_to_els[prio].append(el)
        self.el_to_p[el] = prio
        # if prio < self.min_p:
        #     self.min_p = prio
        self.add_prio(prio)
        # if prio == 0:
        #     print("Prout", self.min_ps)
        self.len += 1

    def pop(self):
        # print("pop", self.min_ps)
        el = self.p_to_els[self.min_ps[0]].pop()
        del self.el_to_p[el]
        if len(self.p_to_els[self.min_ps[0]]) == 0:
            del self.p_to_els[self.min_ps[0]]
            # self.min_p = min(self.p_to_els)
            # print("ok", self.min_ps[0])
            self.pop_prio()
        self.len -= 1
        return el

    def reprio(self, el, new_prio):
        old_prio = self.el_to_p[el]
        self.el_to_p[el] = new_prio
        self.p_to_els[old_prio].remove(el)
        if len(self.p_to_els[old_prio]) == 0:
            del self.p_to_els[old_prio]
            # if old_prio == self.min_p:
            #     self.min_p = min(self.p_to_els)
            self.remove_prio(old_prio)
        self.add_prio(new_prio)
        if new_prio not in self.p_to_els:
            self.p_to_els[new_prio] = []
        self.p_to_els[new_prio].append(el)

    def add_prio(self, prio):
        for i in range(len(self.min_ps)):
            cur_p = self.min_ps[i]
            if cur_p == prio:
                break
            if cur_p > prio:
                self.min_ps.insert(i, prio)
                break

    def remove_prio(self, prio):
        if prio == self.min_ps[0]:
            self.pop_prio()
        else:
            self.min_ps.remove(prio)

    def pop_prio(self):
        # print("pop prio", self.min_ps)
        self.min_ps.pop(0)

    def prio_len(self):
        return len(self.min_ps)
