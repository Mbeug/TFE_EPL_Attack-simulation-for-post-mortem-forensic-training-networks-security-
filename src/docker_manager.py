import os
import tarfile
import tempfile
import docker

class DockerManager:
    """
    This class discuss with dockers
    """
    def __init__(self, selected_machine):
        # Use the default socket
        if selected_machine == 'local':
            self.client = docker.from_env()
        elif selected_machine == 'vm':
            self.client = docker.DockerClient(base_url = 'tcp://192.168.56.104:2375')

    def select_container(self):
        count = 0
        for container in self.client.containers.list():
            print("["+str(count)+"]", end = ' ')
            print('Id: '+container.short_id, end = ' ')
            print('Image: '+container.image.tags[0])
            count = count+1
        selected_container = int(input('Choose your container \n'))
        return self.client.containers.list()[selected_container].short_id

    def copy_to_docker(self, src, cont_name, dst='/'):
        #TODO resolve not copying files to docker
        container = self.client.containers.get(cont_name)

        cur_dir = os.getcwd()
        os.chdir(os.path.dirname(src))
        srcname = os.path.basename(src)

        f = tempfile.NamedTemporaryFile()
        tar = tarfile.open(mode='w', fileobj=f)
        try:
            tar.add(srcname)
        finally:
            tar.close()

        f.seek(0)
        data = f.read()
        res = container.put_archive(os.path.dirname(dst), data)
        os.chdir(cur_dir)
        return res

    def exec_to_docker(self, cont_name, cmd, isdetach=False):
        container = self.client.containers.get(cont_name)
        res = container.exec_run(cmd,detach=isdetach)
        # print(res)
        return res

# Example
#from docker_manager import DockerManager
# dm = DockerManager('vm')
# cont_name = dm.select_container()
# dm.copy_to_docker('./python_scripts/write_file.py',cont_name)
# res = dm.exec_to_docker(cont_name, 'python3 write_file.py new_file.txt')
# print(res.output)

