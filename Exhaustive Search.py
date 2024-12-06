import math
import numpy as np

class Problem:
    def __init__(self):
        infile = open("tsp299.txt", "r")
        data = infile.read().split()
        data = [eval(x) for x in data]
        self.city_count = data[0]  # 도시가 5개라면 도시 번호는 [0, 1, 2, 3, 4]
        data.pop(0)
        self.pos_x = []
        self.pos_y = []
        for i in range(0, self.city_count * 3, 3):
            self.pos_x.append(data[i + 1])
            self.pos_y.append(data[i + 2])

        # 도시 사이의 거리
        self.distance = [[0 for j in range(self.city_count)] for i in range(self.city_count)]
        # 도사 사이의 visibility (1 / 거리)
        self.eta = [[0 for j in range(self.city_count)] for i in range(self.city_count)]
        for i in range(self.city_count - 1):
            for j in range(i + 1, self.city_count):
                self.distance[i][j] = int(math.sqrt((self.pos_x[i] - self.pos_x[j]) ** 2 + (self.pos_y[i] - self.pos_y[j]) ** 2) + 0.5)
                self.distance[j][i] = self.distance[i][j]
                self.eta[i][j] = 1 / self.distance[i][j]
                self.eta[j][i] = self.eta[i][j]

    def GetTourLength(self, tour):
        global best

        sum_distance = 0
        for i in range(len(tour) - 1):
            sum_distance += self.distance[tour[i]][tour[i + 1]]
        sum_distance += self.distance[tour[len(tour) - 1]][tour[0]]

        if sum_distance < best[1]:
            best = [tour, sum_distance]
            print(sum_distance)

        return sum_distance

tsp = Problem()
best = [None, 10000000]     # solution, value

def GetNextCity(tabu, current_city, tau):
    alpha = 1
    beta = 5

    sum_tau_eta = 0
    for i in range(tsp.city_count):
        if i not in tabu:
            sum_tau_eta += (tau[current_city][i] ** alpha * tsp.eta[current_city][i] ** beta)

    p = [0 for i in range(tsp.city_count)]  # 선택 확률
    for i in range(tsp.city_count):
        if i not in tabu:
            tau_eta = (tau[current_city][i] ** alpha * tsp.eta[current_city][i] ** beta)
            p[i] = tau_eta / sum_tau_eta
        else:
            p[i] = 0

    cities = [i for i in range(tsp.city_count)]
    city = np.random.choice(cities, 1, p=p)

    return city[0]

def IsInTour(start, end, tour):
    for i in range(tsp.city_count - 1):
        if tour[i] == start and tour[i + 1] == end:
            return True

    if tour[-1] == start and tour[0] == 0:
        return True

    return False

def main():
    #Initialization
    t = 0
    # 모든 경로의 trail intensity 값을 1.0으로 초기화
    tau = [[0.1 for j in range(tsp.city_count)] for i in range(tsp.city_count)]
    m = 20     # ant 개수
    Q = 10
    rho = 0.7

    while True:
        print(f"iteration : {t}")
        # Initialize the starting city
        tabu = [[0] for k in range(m)]

        # Build a tour for each ant
        for i in range(1, tsp.city_count):
            for k in range(m):
                next_city = GetNextCity(tabu[k], tabu[k][-1], tau)
                tabu[k].append(next_city)

        # Update the trail intensity
        L = [0 for k in range(m)]
        for k in range(m):
            L[k] = tsp.GetTourLength(tabu[k])

        delta_tau = [[0 for j in range(tsp.city_count)] for i in range(tsp.city_count)]
        for i in range(tsp.city_count):
            for j in range(tsp.city_count):
                for k in range(m):
                    if IsInTour(i, j, tabu[k]):
                        delta_k = Q / L[k]
                    else:
                        delta_k = 0
                    delta_tau[i][j] += delta_k
                    #delta_tau[j][i] = delta_tau[i][j]

        for i in range(tsp.city_count):  # 모든 edge (i, j)에 대해 tau 업데이트
            for j in range(tsp.city_count):
                tau[i][j] = rho * tau[i][j] + delta_tau[i][j]

        t += 1

        if t == 50:
            break

    print("최단 경로 :", best[0])
    print("최단 거리 :", best[1])

#main()

# GUI