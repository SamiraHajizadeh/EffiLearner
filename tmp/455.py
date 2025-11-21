
def check_monthnumb_number(n):
    if (n > 0 and n%4 == 0 and n< 10) or (n > 0 and n%4 == 0 and n<=100) or (n > 0 and n%4 == 0 and n<=500):
      return True
    else :
      return False
if __name__ == "__main__":
 for i in range(1, 13):
   print("The month {}: is {} days".format(i,check_monthnumb_number(i)))
assert check_monthnumb_number(5)==True
assert check_monthnumb_number(2)==False
assert check_monthnumb_number(6)==False