import os
tel = {'peron':True,'zajezdnia':False,'reka':False,'przeszkody':True,"czerwony":False,'twarz':False,'banan':False}
filmOrCam=1 #1== dla filmu ,obojetnie jaka inna liczba dla kamery
os.system("python skryptRozdzielajacy.py "+str(filmOrCam)+ " czysty.avi "+str(tel))


