def combine(final_final):
    """
    A function used to combine two sections of sentences if the difference of
    row numbers between them is 60
    """
    final_f = []
    final_f.append(final_final[0])

    previous_list = final_final[0]
    flag = previous_list[-1]

    if len(final_final) == 1:
        return final_final

    for i in range(1, len(final_final)):
        if final_final[i][0] < previous_list[-1] + 60:
            final_f[-1] = final_f[-1] + final_final[i]
            previous_list = final_f[-1]
            print(final_f)
        else:
            final_f.append(final_final[i])
            previous_list = final_f[-1]

    return final_f
