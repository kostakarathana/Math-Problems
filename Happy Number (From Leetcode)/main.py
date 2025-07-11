def get_happy_number_record(num: int) -> list[int]:
    record: list[int] = []
    seen: set[int] = set()
    temp_num: int = num

    while True:
        temp_num = sum([int(n)**2 for n in list(str(temp_num))])
        if temp_num in seen:
            record.append(temp_num)
            break
        elif temp_num == 1:
            record.append(temp_num)
            break
        else:
            record.append(temp_num)
            seen.add(temp_num)
    return record

if __name__ == "__main__":
    print(get_happy_number_record(15))
    
    

        

