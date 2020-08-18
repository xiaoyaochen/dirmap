import pandas as pd
from urllib import parse
from lib.parse.cmdline import cmdLineParser

result = []

def tar_from_input(url):
    host = parse.urlparse(url.strip()).hostname
    port = parse.urlparse(url.strip()).port
    if port:
        return "./output/{}_{}.txt".format(host,port)
    else:
        return "./output/{}.txt".format(host)

def tar_from_file(file):
    path_list = set()
    with open(file,encoding='utf-8') as r:
        for tar in r.readlines():
            host = parse.urlparse(tar.strip()).hostname
            port = parse.urlparse(tar.strip()).port
            if port:
                path_list.add("./output/{}_{}.txt".format(host,port))
            else:
                path_list.add("./output/{}.txt".format(host))
    return path_list
            

def read_result(file):
    try:
        with open(file,encoding='utf-8') as r:
            for line in r.readlines():
                line = line.replace(']','[')
                l = line.split('[')
                result.append({'url':l[6].strip(),'status':l[1],'lenth':l[5],'type':l[3]})
    except Exception as e:
        print(e)
            

def to_xlsx():
    
    inp = cmdLineParser().target_input
    fil = cmdLineParser().target_file
    if inp:
        r_path = tar_from_input(inp)
        read_result(r_path)
        save_pd = pd.DataFrame.from_dict(result)
        x_file = r_path.replace('txt','xlsx')
        save_pd.to_excel(x_file,index=False)
        print('结果保存：{}'.format(x_file))
    else:
        r_path = tar_from_file(fil)
        for f in r_path:
            read_result(f)
        save_pd = pd.DataFrame.from_dict(result)
        x_file = './output/{}.xlsx'.format(fil.split('.')[-2])
        print(x_file)
        save_pd.to_excel(x_file,index=False)
        print('结果保存：{}'.format(x_file))