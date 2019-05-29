# perfect number is a number whose digit sumup to 10.
# 19, 28, ..., 91, 109, 118, 190, 208, 217...

def gen_perfect_number(x, k, starting, record, result = []):
    if starting: record = []

    if k == 1:
        record.append(x)
        print(record)
        result.append(''.join([str(x) for x in record]))
        record.pop()
    else:
        if starting:
            for i in range(1, min(9,x)+1):
                record.append(i)
                gen_perfect_number(x-i, k-1, False, record, result)
                record.pop()
        else:
            for i in range(min(9,x)+1):
                record.append(i)
                gen_perfect_number(x-i, k-1, False, record, result)
                record.pop()
def main():
    N = 10
    k = 2

    count = 0
    while True:
        result = []
        reached = False
        gen_perfect_number(10, k, True, [], result)
        k = k + 1
        for x in result:
            print(x)
            count= count + 1
            if count == N:
                reached = True
                break
        if reached:
            break

# implementation with yield
# to recursively yield use 'yield from' (since pyton 3.3) no need to loop
# yield.
def gen_perfect_number_yield(x, k, starting, record):
    if starting: record = []

    if k == 1:
        record.append(x)
        print(record)
        yield ''.join([str(x) for x in record])
        record.pop()
    else:
        if starting:
            for i in range(1, min(9,x)+1):
                record.append(i)
                yield from gen_perfect_number_yield(x-i, k-1, False, record)

                record.pop()
        else:
            for i in range(min(9,x)+1):
                record.append(i)
                yield from gen_perfect_number_yield(x-i, k-1, False, record)
                record.pop()
def main_y():
    N = 10
    k = 2

    count = 0
    gen = gen_perfect_number_yield(10, k, True, record=[])
    while True:
        try:
            result = next(gen)
            print(result)
            count = count + 1

            if count  == N:
                print(result)
                break
        except StopIteration:
            k = k + 1
            gen = gen_perfect_number_yield(10, k, True, record=[])

if __name__ == '__main__':
    #main1()
    main_y()
