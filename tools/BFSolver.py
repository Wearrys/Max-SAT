import math


class bruteforceSolver:
    def knapsack_solve(self, data):
        n, m = map(int, data[1].split(' '))
        wei = list(map(int, data[2].split(' ')))
        val = list(map(int, data[3].split(' ')))

        f = [0 for i in range(m + 1)]

        for i in range(n):
            for j in range(m, wei[i] - 1, -1):
                f[j] = max(f[j], f[j - wei[i]] + val[i])

        return f[m]

    def TSP_solve(self, data):
        n = int(data[1])
        d, mx = [], 0
        for i in range(n):
            d.append(list(map(int, data[i + 2].split(' '))))
            mx = max(max(d[i]), mx)

        po = [int(math.pow(2, i)) for i in range(n + 1)]

        # f[i][j] denotes the minimum money needed to pay when passing through all city in j and finally arrive at city i
        f = [[mx * n + 1 for i in range(po[n])] for j in range(n)]
        f[0][1] = 0
        for j in range(po[n]):
            for i in range(n):
                if f[i][j] <= mx * n:
                    for k in range(n):
                        if (j & po[k]) == 0:
                            f[k][j + po[k]] = min(f[k][j + po[k]], f[i][j] + d[i][k])
        return min([(d[i][0] + f[i][po[n] - 1]) for i in range(n)])

    def independent_set_solve(self, data):

        def dfs(ls, sum, edge, vis):
            if ls >= n:
                return sum
            res = dfs(ls + 1, sum, edge, vis)
            flag = True
            for i in range(ls):
                if vis[i] and edge[i][ls]:
                    flag = False
                    break
            if flag:
                vis[ls] = 1
                res = max(res, dfs(ls + 1, sum + 1, edge, vis))
                vis[ls] = 0
            return res

        n, m = map(int, data[1].split(' '))
        edge = [[0 for j in range(n)] for i in range(n)]
        for i in range(m):
            u, v = map(int, data[i + 2].split(' '))
            edge[u][v] = edge[v][u] = 1
        vis = [0 for i in range(n)]
        return dfs(0, 0, edge, vis)

    def dominating_set_solve(self, data):

        def dfs(ls, sum, edge, vis):
            if ls >= n:
                for i in range(n):
                    if not vis[i]:
                        flag = False
                        for j in range(n):
                            if vis[j] and edge[i][j]:
                                flag = True
                                break
                        if not flag:
                            return n
                return sum

            res = dfs(ls + 1, sum, edge, vis)
            vis[ls] = 1
            res = min(res, dfs(ls + 1, sum + 1, edge, vis))
            vis[ls] = 0
            return res

        n, m = map(int, data[1].split(' '))
        edge = [[0 for j in range(n)] for i in range(n)]
        for i in range(m):
            u, v = map(int, data[i + 2].split(' '))
            edge[u][v] = edge[v][u] = 1
        vis = [0 for i in range(n)]
        return dfs(0, 0, edge, vis)

    def chromatic_number_solve(self, data):

        def dfs(ls, tot_col, col):
            if ls >= n:
                return 1
            app_col = set()
            for to in edge[ls]:
                if (to < ls):
                    app_col.add(col[to])
            ava_col = {i for i in range(tot_col)} - app_col
            for c in ava_col:
                col[ls] = c
                if (dfs(ls + 1, tot_col, col)):
                    return 1
            return 0

        n, m = map(int, data[1].split(' '))
        edge = [[] for i in range(n)]
        for i in range(m):
            u, v = map(int, data[i + 2].split(' '))
            edge[u].append(v)
            edge[v].append(u)
        col = [-1 for i in range(n)]
        for i in range(1, n):
            if dfs(0, i, col):
                return i
        return n

    def solve(self, input_file):
        data = [line.strip() for line in open(input_file, 'r')]
        if data[0] == "TSP":
            return self.TSP_solve(data)
        elif data[0] == "01-KNAPSACK":
            return self.knapsack_solve(data)
        elif data[0] == "INDEPENDENT-SET":
            return self.independent_set_solve(data)
        elif data[0] == "DOMINATING-SET":
            return self.dominating_set_solve(data)
        elif data[0] == "CHROMATIC-NUMBER":
            return self.chromatic_number_solve(data)


if __name__ == "__main__":
    b = bruteforceSolver()
    print(b.solve("input.txt"))
