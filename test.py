list_dict = [{"A":15, "B":2}, {"A":16, "B":6}, {"A":19, "B":3}]
list_output = [list_dict[i]["A"] for i in range(len(list_dict))]
print(list_output)