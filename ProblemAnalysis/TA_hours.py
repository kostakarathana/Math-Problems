
def days_to_hold_hours(availability: list) -> list:
    '''
    I ask students every week what day they can attend TA hours,
    like I might get:

    avail = [1, 5, 9, 10, 4, 1, 10] where avail[0] = Monday avail[1] = Tuesday etc.

    avail[i] in general is the number of students available for day i. BUT I can't
    book rooms for two consequetive days, so I need some way to maximise the number
    of students I can help. 
    '''

    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    n = len(availability)
    if n == 0:
        return []
    if n == 1:
        return [days[0]]

    # dp[i] = (max_people, list_of_days)
    dp = [(0, []) for _ in range(n)]
    dp[0] = (availability[0], [days[0]])
    dp[1] = max(
        (availability[0], [days[0]]),
        (availability[1], [days[1]])
    )

    for i in range(2, n):
        include_today = dp[i - 2][0] + availability[i]
        if include_today > dp[i - 1][0]:
            dp[i] = (include_today, dp[i - 2][1] + [days[i]])
        else:
            dp[i] = dp[i - 1]

    return dp[-1][1]

print(days_to_hold_hours([1, 5, 9, 10, 4, 1, 10]))
