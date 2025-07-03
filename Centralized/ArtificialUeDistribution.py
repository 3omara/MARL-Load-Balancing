import matplotlib.pyplot as plt
import random
import math
import time

boundaries = [402.09,1282.45,2708.33,2651.23]
enbs = [
    [796.8938352346304, 2118.770895089954, 30],
    [1371.877438257332, 2331.1886772192083, 30],
    [1354.4832434408017, 1791.0314224967733, 3],
    [1756.5697463185643, 1924.1612803018652, 3],
    [1857.1249418809894, 2368.2851388552226, 3],   
    [2291.7522011126857, 1929.4412568900734, 3],
]
ues = []
mytime = int(time.time())
random.seed(mytime)

def condense_ues(enb, num_ues, min_distance, max_distance):
    if (max_distance + enb[0] > boundaries[2]):
        max_distance = boundaries[2] - enb[0]
    if (max_distance + enb[1] > boundaries[3]):
        max_distance = boundaries[3] - enb[1]
    if (max_distance < min_distance):
        print("Max distance is less than min distance or exceeds boundaries.")
        return
    for _ in range(num_ues):
        magnitude = math.sqrt(random.uniform(0, 1) * (max_distance ** 2 - min_distance ** 2) + min_distance ** 2)
        angle = random.uniform(0, 2 * math.pi)
        x = enb[0] + magnitude * math.cos(angle)
        y = enb[1] + magnitude * math.sin(angle)
        ues.append([x, y])

def random_ues(num_ues):
    for _ in range(num_ues):
        x = random.uniform(boundaries[0], boundaries[2])
        y = random.uniform(boundaries[1], boundaries[3])
        ues.append([x, y])

def generate_ue_allocation_file():
    with open("ue_allocation{}.txt".format(mytime), "w") as file:
        for ue in ues:
            file.write(f"uePositionAlloc->Add(Vector({ue[0]}, {ue[1]}, 3));")
            file.write("\n")
    file.close()



if __name__ == "__main__":
    condense_ues(enbs[1], 15, 75, 150)
    condense_ues(enbs[3], 15, 50, 150)
    random_ues(10)
    generate_ue_allocation_file()
    plt.figure(figsize=(10, 10))
    plt.xlim(boundaries[0], boundaries[2])
    plt.ylim(boundaries[1], boundaries[3])
    plt.scatter([ue[0] for ue in ues], [ue[1] for ue in ues], c='blue', label='UEs')
    for i in range(len(enbs)):
        plt.scatter(enbs[i][0], enbs[i][1], c='green', marker='o', s=100)
        plt.text(enbs[i][0], enbs[i][1], f'ENB {i}', fontsize=9, ha='right', va='bottom', color='black')
    plt.legend()
    plt.title('User Equipment (UE) Distribution')
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.savefig('ue_exp_distribution_{}.png'.format(mytime))
