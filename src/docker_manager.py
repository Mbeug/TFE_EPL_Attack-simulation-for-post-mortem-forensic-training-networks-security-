import os
import tarfile
import tempfile
import docker

class DockerManager:

    def __init__(self):
        # Use the default socket
        self.client = docker.from_env()

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
        container = self.client.containers.get(cont_name)

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
        container.put_archive(os.path.dirname(dst), data)

    def exec_to_docker(self, cont_name, cmd):
        container = self.client.containers.get(cont_name)
        res = container.exec_run(cmd)
        return res

# # Example
# from docker_manager import DockerManager 
# dm = DockerManager()
# cont_name = dm.select_container()
# dm.copy_to_docker('./python_scripts/write_file.py',cont_name)
# res = dm.exec_to_docker(cont_name, 'python3 write_file.py new_file.txt')
# print(res.output)