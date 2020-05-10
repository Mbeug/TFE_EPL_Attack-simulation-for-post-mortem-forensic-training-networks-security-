from docker_manager import DockerManager
from network_manager import NetworkManager

class SimulationManager:
    """
    Class to manage the simulation of traffic for clients:
        
    """
    def __init__(self,networkmanager=None):
        if(networkmanager == None):
            self.nm = NetworkManager()
        else:
            self.nm = networkmanager
        self.dm = DockerManager(self.nm.selected_machine["compute_id"])
        pass

    def mail_activity(self, list_pc, t_min = 2, t_max = 5, sender = "bob", passwd = "alice", receiver = "bob"):
        """
        Start mail activity on machines with curl

        :param list_pc: list of targeted machines 
        :param t_min: min time between each request
        :param t_max: max time between each request
        :param sender: sender of mails
        :param passwd: password of the sender
        :param receiver: recipient of the mail
        :type list_pc: list
        :type t_min: int
        :type t_max: int
        :type sender: str
        :type passwd: str
        :type receiver: str
        """
        for pc in list_pc:
            container = pc["properties"]["container_id"]
            self.dm.copy_to_docker("./config_files/client/requests_mail.sh", container)
            self.dm.copy_to_docker("./config_files/client/kill_mail.sh", container)
            self.dm.copy_to_docker("./config_files/client/template_mail.txt", container)
            self.dm.exec_to_docker(container, "ash requests_mail.sh "+str(t_min)+" "+str(t_max)+" "+sender+" "+str(passwd)+" "+receiver,isdetach=True)
        pass

    def kill_mail_activity(self, list_pc):
        """
        Stop mail activity on machines

        :param list_pc: list of targeted machines
        :type list_pc: list
        """
        for pc in list_pc:
            container = pc["properties"]["container_id"]
            self.dm.exec_to_docker(container, "ash kill_mail.sh")
        pass

    def http_ftp_activity(self, list_pc, t_min = 2, t_max = 5, path_url = "./config_files/client/"):
        """
        Start http/ftp activity on machines with curl

        :param list_pc: list of targeted machines 
        :param t_min: min time between each request
        :param t_max: max time between each request
        :param path_url: path to the file containing urls
        :type list_pc: list
        :type t_min: int
        :type t_max: int
        :type path_url: str
        """
        for pc in list_pc:
            container = pc["properties"]["container_id"]
            self.dm.copy_to_docker("./config_files/client/requests_urls.sh", container)
            self.dm.copy_to_docker("./config_files/client/kill_urls.sh", container)
            self.dm.copy_to_docker(path_url+"url.txt", container)
            self.dm.exec_to_docker(container, "ash requests_urls.sh "+str(t_min)+" "+str(t_max)+" url.txt",isdetach=True)
        pass

    def kill_http_ftp_activity(self, list_pc):
        """
        Stop http/ftp activity on machines with curl

        :param list_pc: list of targeted machines
        :type list_pc: list
        """
        for pc in list_pc:
            container = pc["properties"]["container_id"]
            self.dm.exec_to_docker(container, "ash kill_urls.sh")
        pass