import os
import tarfile
import tempfile
from typing import Tuple

import docker

class DockerManager:
    """
    This class discuss with dockers

    Example::

        from docker_manager import DockerManager
        dm = DockerManager('vm')
        cont_name = dm.select_container()
        dm.copy_to_docker('./python_scripts/write_file.py',cont_name)
        res = dm.exec_to_docker(cont_name, 'python3 write_file.py new_file.txt')
        print(res.output)
    """

    def __init__(self, selected_machine):
        # Use the default socket
        if selected_machine == 'local':
            self.client = docker.from_env()
        elif selected_machine == 'vm':
            self.client = docker.DockerClient(base_url = 'tcp://192.168.56.110:2375')

    def select_container(self):
        """
        Prompt a selection of running container

        :return: short_id of the selected container
        """
        count = 0
        for container in self.client.containers.list():
            print("["+str(count)+"]", end = ' ')
            print('Id: '+container.short_id, end = ' ')
            print('Image: '+container.image.tags[0])
            count = count+1
        selected_container = int(input('Choose your container \n'))
        return self.client.containers.list()[selected_container].short_id

    def copy_to_docker(self, src, cont_name, dst='/'):
        """
        Copy a file or folder to a specific docker container

        :param src: path of the file to copy
        :param cont_name: name of the container (for example short_id)
        :param dst:  destination path in the container
        :type src: str
        :type dst: str
        :return: True if the copy was successful
        """
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

    def exec_to_docker(self, cont_name, cmd, isdetach=False)->Tuple[int,bytes]:
        """
        Execute a command inside a container

        :param cont_name: name of the container (for example short_id)
        :param cmd: command to execute
        :param isdetach: True if we want to detach
        :type cont_name: str
        :type src: str
        :type dst: bool
        :return: tuple with the exit code and the output of the command
        """
        container = self.client.containers.get(cont_name)
        res = container.exec_run(cmd,detach=isdetach)
        return res