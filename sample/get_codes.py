from token_pcl import codes

print(codes)

while True:
    try:
        code = input(">> ")
        print(codes.get(code, "Not found"))
    except KeyboardInterrupt:
        print()
        exit(0)