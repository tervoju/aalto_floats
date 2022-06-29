# testing temperature 
# 
def get_cpu_temp():
    tempFile = open( "/sys/class/thermal/thermal_zone0/temp" )
    cpu_temp = tempFile.read()
    tempFile.close()
    return float(float(cpu_temp)/1000.0)
    
if __name__ == "__main__":
    print(str(get_cpu_temp()))