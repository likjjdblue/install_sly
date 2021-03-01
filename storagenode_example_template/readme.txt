storagenode_example_template 目录下存放的是工具配置模板，使用方式：
1、项目组按实际情况，拷贝其中一个模板至上一级文件目录(也就是install_sly 目录下)，并将文件重命名为"storagenode.py"
2、按照实际情况对storagenode.py中的配置项进行修改。


说明：
storagenode_nas.py  
    该模板对应 NAS 存储,使用该模板需提前保证外部NAS 可访问（建议项目组优先采用该方式）； 可以使用mount  命令进行测试

storagenode_nfs.py   
    该模板对应NFS 存储,使用该模板将由工具搭建NFS 服务;程序自建NFS 性能会有很大问题，一般不推荐用于正式环境，除非是小规模使用，或者用于测试环境!

