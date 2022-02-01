def check():
    try:
        ipt = int(input())
        assert 25 <= ipt <= 37
    except ValueError:
        print("Correct the error!")
    except AssertionError:
        print("Correct the error!")
    else:
        print(ipt)
