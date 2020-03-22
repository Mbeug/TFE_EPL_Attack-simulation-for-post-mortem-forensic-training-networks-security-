import sys
from time import sleep
from unittest import TestCase


from colorOutput import ColorOutput
from network_manager import NetworkManager


class TestNetworkManager(TestCase):
    nm  = NetworkManager(0,{
                "compute_id": "vm",
                "name": "GNS3 VM (GNS3 VM)"
            })

    def test_get_all_templates(self):
        # expected= [
        #     {
        #         "adapter_type": "e1000",
        #         "adapters": 1,
        #         "bios_image": "",
        #         "boot_priority": "c",
        #         "builtin": False,
        #         "category": "guest",
        #         "cdrom_image": "",
        #         "compute_id": "vm",
        #         "console_auto_start": False,
        #         "console_type": "vnc",
        #         "cpu_throttling": 0,
        #         "cpus": 1,
        #         "custom_adapters": [],
        #         "default_name_format": "{name}-{0}",
        #         "first_port_name": "",
        #         "hda_disk_image": "linux-tinycore-linux-6.4-firefox-33.1.1-2.img",
        #         "hda_disk_interface": "ide",
        #         "hdb_disk_image": "",
        #         "hdb_disk_interface": "ide",
        #         "hdc_disk_image": "",
        #         "hdc_disk_interface": "ide",
        #         "hdd_disk_image": "",
        #         "hdd_disk_interface": "ide",
        #         "initrd": "",
        #         "kernel_command_line": "",
        #         "kernel_image": "",
        #         "legacy_networking": False,
        #         "linked_clone": True,
        #         "mac_address": "",
        #         "name": "Firefox 31.1.1~2",
        #         "on_close": "power_off",
        #         "options": "-vga std -usbdevice tablet",
        #         "platform": "i386",
        #         "port_name_format": "Ethernet{0}",
        #         "port_segment_size": 0,
        #         "process_priority": "normal",
        #         "qemu_path": "/usr/bin/qemu-system-i386",
        #         "ram": 256,
        #         "symbol": "firefox.svg",
        #         "template_id": "3279fa58-eef8-48ea-a6b9-a20bf1240d12",
        #         "template_type": "qemu",
        #         "usage": ""
        #     },
        #     {
        #         "adapter_type": "Intel PRO/1000 MT Desktop (82540EM)",
        #         "adapters": 1,
        #         "builtin": False,
        #         "category": "guest",
        #         "compute_id": "local",
        #         "console_auto_start": False,
        #         "console_type": "none",
        #         "custom_adapters": [],
        #         "default_name_format": "{name}-{0}",
        #         "first_port_name": "",
        #         "headless": False,
        #         "linked_clone": False,
        #         "name": "GNS3 VM",
        #         "on_close": "power_off",
        #         "port_name_format": "Ethernet{0}",
        #         "port_segment_size": 0,
        #         "ram": 2048,
        #         "symbol": ":/symbols/vbox_guest.svg",
        #         "template_id": "9893f914-515f-4baf-bdf8-e5dd3ac4e208",
        #         "template_type": "virtualbox",
        #         "usage": "",
        #         "use_any_adapter": False,
        #         "vmname": "GNS3 VM"
        #     },
        #     {
        #         "adapters": 1,
        #         "builtin": False,
        #         "category": "guest",
        #         "compute_id": "vm",
        #         "console_auto_start": False,
        #         "console_http_path": "/",
        #         "console_http_port": 80,
        #         "console_resolution": "1024x768",
        #         "console_type": "telnet",
        #         "custom_adapters": [],
        #         "default_name_format": "{name}-{0}",
        #         "environment": "",
        #         "extra_hosts": "",
        #         "extra_volumes": [],
        #         "image": "gns3/ubuntu:xenial",
        #         "name": "Ubuntu Docker Guest",
        #         "start_command": "",
        #         "symbol": "linux_guest.svg",
        #         "template_id": "d15fb3d1-0ba1-43d9-a725-e286bb6c1e56",
        #         "template_type": "docker",
        #         "usage": ""
        #     },
        #     {
        #         "adapter_type": "e1000",
        #         "adapters": 4,
        #         "bios_image": "",
        #         "boot_priority": "c",
        #         "builtin": False,
        #         "category": "router",
        #         "cdrom_image": "",
        #         "compute_id": "vm",
        #         "console_auto_start": False,
        #         "console_type": "telnet",
        #         "cpu_throttling": 0,
        #         "cpus": 1,
        #         "custom_adapters": [],
        #         "default_name_format": "{name}-{0}",
        #         "first_port_name": "",
        #         "hda_disk_image": "bird-tinycore64-1.5.0.img",
        #         "hda_disk_interface": "ide",
        #         "hdb_disk_image": "",
        #         "hdb_disk_interface": "ide",
        #         "hdc_disk_image": "",
        #         "hdc_disk_interface": "ide",
        #         "hdd_disk_image": "",
        #         "hdd_disk_interface": "ide",
        #         "initrd": "",
        #         "kernel_command_line": "",
        #         "kernel_image": "",
        #         "legacy_networking": False,
        #         "linked_clone": True,
        #         "mac_address": "",
        #         "name": "BIRD 1.5.0",
        #         "on_close": "power_off",
        #         "options": "",
        #         "platform": "i386",
        #         "port_name_format": "Ethernet{0}",
        #         "port_segment_size": 0,
        #         "process_priority": "normal",
        #         "qemu_path": "/usr/bin/qemu-system-x86_64",
        #         "ram": 128,
        #         "symbol": ":/symbols/classic/router.svg",
        #         "template_id": "6f38fbb5-ae7d-43b6-bd8f-8af1a06dd3cd",
        #         "template_type": "qemu",
        #         "usage": "Configure interfaces in /opt/bootlocal.sh, BIRD configuration is done in /usr/local/etc/bird"
        #     },
        #     {
        #         "adapters": 1,
        #         "builtin": False,
        #         "category": "guest",
        #         "compute_id": "vm",
        #         "console_auto_start": False,
        #         "console_http_path": "/",
        #         "console_http_port": 80,
        #         "console_resolution": "1024x768",
        #         "console_type": "telnet",
        #         "custom_adapters": [],
        #         "default_name_format": "{name}-{0}",
        #         "environment": "",
        #         "extra_hosts": "",
        #         "extra_volumes": [],
        #         "image": "alpine",
        #         "name": "Alpine Linux",
        #         "start_command": "",
        #         "symbol": "linux_guest.svg",
        #         "template_id": "0cf3b8a5-8a9c-4ba7-a900-e44ec8b13695",
        #         "template_type": "docker",
        #         "usage": ""
        #     },
        #     {
        #         "adapters": 1,
        #         "builtin": False,
        #         "category": "guest",
        #         "compute_id": "vm",
        #         "console_auto_start": False,
        #         "console_http_path": "/",
        #         "console_http_port": 80,
        #         "console_resolution": "1024x768",
        #         "console_type": "telnet",
        #         "custom_adapters": [],
        #         "default_name_format": "{name}-{0}",
        #         "environment": "",
        #         "extra_hosts": "",
        #         "extra_volumes": [],
        #         "image": "thomasbeckers/alpine-python3",
        #         "name": "thomasbeckers-alpine-python3",
        #         "start_command": "",
        #         "symbol": ":/symbols/docker_guest.svg",
        #         "template_id": "0fcf4286-b924-440a-88bd-f973871e4b9b",
        #         "template_type": "docker",
        #         "usage": ""
        #     },
        #     {
        #         "builtin": True,
        #         "category": "guest",
        #         "compute_id": None,
        #         "default_name_format": "Cloud{0}",
        #         "name": "Cloud",
        #         "symbol": ":/symbols/cloud.svg",
        #         "template_id": "39e257dc-8412-3174-b6b3-0ee3ed6a43e9",
        #         "template_type": "cloud"
        #     },
        #     {
        #         "builtin": True,
        #         "category": "guest",
        #         "compute_id": None,
        #         "default_name_format": "NAT{0}",
        #         "name": "NAT",
        #         "symbol": ":/symbols/cloud.svg",
        #         "template_id": "df8f4ea9-33b7-3e96-86a2-c39bc9bb649c",
        #         "template_type": "nat"
        #     },
        #     {
        #         "builtin": True,
        #         "category": "guest",
        #         "compute_id": None,
        #         "default_name_format": "PC{0}",
        #         "name": "VPCS",
        #         "properties": {
        #             "base_script_file": "vpcs_base_config.txt"
        #         },
        #         "symbol": ":/symbols/vpcs_guest.svg",
        #         "template_id": "19021f99-e36f-394d-b4a1-8aaa902ab9cc",
        #         "template_type": "vpcs"
        #     },
        #     {
        #         "builtin": True,
        #         "category": "switch",
        #         "compute_id": None,
        #         "console_type": "none",
        #         "default_name_format": "Switch{0}",
        #         "name": "Ethernet switch",
        #         "symbol": ":/symbols/ethernet_switch.svg",
        #         "template_id": "1966b864-93e7-32d5-965f-001384eec461",
        #         "template_type": "ethernet_switch"
        #     },
        #     {
        #         "builtin": True,
        #         "category": "switch",
        #         "compute_id": None,
        #         "default_name_format": "Hub{0}",
        #         "name": "Ethernet hub",
        #         "symbol": ":/symbols/hub.svg",
        #         "template_id": "b4503ea9-d6b6-3695-9fe4-1db3b39290b0",
        #         "template_type": "ethernet_hub"
        #     },
        #     {
        #         "builtin": True,
        #         "category": "switch",
        #         "compute_id": None,
        #         "default_name_format": "FRSW{0}",
        #         "name": "Frame Relay switch",
        #         "symbol": ":/symbols/frame_relay_switch.svg",
        #         "template_id": "dd0f6f3a-ba58-3249-81cb-a1dd88407a47",
        #         "template_type": "frame_relay_switch"
        #     },
        #     {
        #         "builtin": True,
        #         "category": "switch",
        #         "compute_id": None,
        #         "default_name_format": "ATMSW{0}",
        #         "name": "ATM switch",
        #         "symbol": ":/symbols/atm_switch.svg",
        #         "template_id": "aaa764e2-b383-300f-8a0e-3493bbfdb7d2",
        #         "template_type": "atm_switch"
        #     }
        # ]
        self.assertTrue(self.nm.get_all_templates() is not [])


    def test_get_all_gns3vm(self):
        # expected =[
        #     {
        #         "compute_id": "vmware",
        #         "name": "VMware Fusion (recommended)"
        #     },
        #     {
        #
        #         "compute_id": "virtualbox",
        #         "name": "VirtualBox"
        #     },
        #     {
        #         "compute_id": "remote",
        #         "name": "Remote"
        #     }
        # ]
        self.assertTrue(self.nm.get_all_gns3vm() is not [])

    def test_get_all_machines(self):
        # expected = [
        #     {
        #         "compute_id": "local",
        #         "name": "MacBook-Pro-de-Maxime-9.local"
        #     },
        #     {
        #         "compute_id": "vm",
        #         "name": "GNS3 VM (GNS3 VM)"
        #     }
        # ]
        self.assertTrue(self.nm.get_all_machines() is not [])
    def test_get_all_drawings(self):
        # expected = [
        #     {
        #         "drawing_id": "63aa2322-577a-45b2-8e79-074da5184899",
        #         "locked": False,
        #         "project_id": "8cf37f7e-76a1-418c-9317-82e8586a1560",
        #         "rotation": 0,
        #         "svg": "<svg></svg>",
        #         "x": 0,
        #         "y": 0,
        #         "z": 2
        #     },
        #     {
        #         "drawing_id": "1f40e801-68e4-4ba0-87bd-458374ee8768",
        #         "locked": False,
        #         "project_id": "8cf37f7e-76a1-418c-9317-82e8586a1560",
        #         "rotation": 0,
        #         "svg": "<svg height=\"374\" width=\"528\"><rect fill=\"#ffffff\" fill-opacity=\"1.0\" height=\"374\" stroke=\"#000000\" stroke-width=\"2\" width=\"528\" /></svg>",
        #         "x": -465,
        #         "y": -360,
        #         "z": 1
        #     },
        #     {
        #         "drawing_id": "1a65ffb8-7283-466f-a8e1-8dc917eb8660",
        #         "locked": False,
        #         "project_id": "8cf37f7e-76a1-418c-9317-82e8586a1560",
        #         "rotation": 0,
        #         "svg": "<svg></svg>",
        #         "x": 0,
        #         "y": 0,
        #         "z": 2
        #     },
        #     {
        #         "drawing_id": "1d0bf1ff-5d16-406f-83ac-58a4603f5438",
        #         "locked": False,
        #         "project_id": "8cf37f7e-76a1-418c-9317-82e8586a1560",
        #         "rotation": 0,
        #         "svg": "<svg></svg>",
        #         "x": 0,
        #         "y": 0,
        #         "z": 2
        #     }
        # ]
        self.assertTrue(self.nm.get_all_drawings() is not [])
    def test_get_all_links(self):
        # expected = [
        #     {
        #         "capture_compute_id": None,
        #         "capture_file_name": None,
        #         "capture_file_path": None,
        #         "capturing": False,
        #         "filters": {},
        #         "link_id": "87321383-2e39-452f-b30a-dd71f46ca4c3",
        #         "link_type": "ethernet",
        #         "nodes": [],
        #         "project_id": "8cf37f7e-76a1-418c-9317-82e8586a1560",
        #         "suspend": False
        #     },
        #     {
        #         "capture_compute_id": None,
        #         "capture_file_name": None,
        #         "capture_file_path": None,
        #         "capturing": False,
        #         "filters": {},
        #         "link_id": "775aa0ed-911c-4e8e-9ff3-0e9bf55c37e1",
        #         "link_type": "ethernet",
        #         "nodes": [],
        #         "project_id": "8cf37f7e-76a1-418c-9317-82e8586a1560",
        #         "suspend": False
        #     },
        #     {
        #         "capture_compute_id": None,
        #         "capture_file_name": None,
        #         "capture_file_path": None,
        #         "capturing": False,
        #         "filters": {},
        #         "link_id": "2f9101dd-bdac-4ff2-bc90-e05ac07ced3b",
        #         "link_type": "ethernet",
        #         "nodes": [],
        #         "project_id": "8cf37f7e-76a1-418c-9317-82e8586a1560",
        #         "suspend": False
        #     },
        #     {
        #         "capture_compute_id": None,
        #         "capture_file_name": None,
        #         "capture_file_path": None,
        #         "capturing": False,
        #         "filters": {},
        #         "link_id": "b6bff2a2-1638-4384-a1e2-ffa9bf24ce72",
        #         "link_type": "ethernet",
        #         "nodes": [
        #             {
        #                 "adapter_number": 0,
        #                 "label": {
        #                     "rotation": 0,
        #                     "style": "font-family: TypeWriter;font-size: 10.0;font-weight: bold;fill: #000000;fill-opacity: 1.0;",
        #                     "text": "e1",
        #                     "x": 71,
        #                     "y": -1
        #                 },
        #                 "node_id": "27515250-dbac-422e-9e11-1eefaf7ae76b",
        #                 "port_number": 1
        #             },
        #             {
        #                 "adapter_number": 0,
        #                 "label": {
        #                     "rotation": 0,
        #                     "style": "font-family: TypeWriter;font-size: 10.0;font-weight: bold;fill: #000000;fill-opacity: 1.0;",
        #                     "text": "e0",
        #                     "x": -3,
        #                     "y": 46
        #                 },
        #                 "node_id": "72e118c6-6799-4291-8fed-41d8c75fc522",
        #                 "port_number": 0
        #             }
        #         ],
        #         "project_id": "8cf37f7e-76a1-418c-9317-82e8586a1560",
        #         "suspend": False
        #     },
        #     {
        #         "capture_compute_id": None,
        #         "capture_file_name": None,
        #         "capture_file_path": None,
        #         "capturing": False,
        #         "filters": {},
        #         "link_id": "14aa31f2-e44d-4b59-94f4-9215565d4b1b",
        #         "link_type": "ethernet",
        #         "nodes": [
        #             {
        #                 "adapter_number": 0,
        #                 "label": {
        #                     "rotation": 0,
        #                     "style": "font-family: TypeWriter;font-size: 10.0;font-weight: bold;fill: #000000;fill-opacity: 1.0;",
        #                     "text": "e0",
        #                     "x": 75,
        #                     "y": 21
        #                 },
        #                 "node_id": "27515250-dbac-422e-9e11-1eefaf7ae76b",
        #                 "port_number": 0
        #             },
        #             {
        #                 "adapter_number": 0,
        #                 "label": {
        #                     "rotation": 0,
        #                     "style": "font-family: TypeWriter;font-size: 10.0;font-weight: bold;fill: #000000;fill-opacity: 1.0;",
        #                     "text": "e0",
        #                     "x": -7,
        #                     "y": 23
        #                 },
        #                 "node_id": "97e285e3-f752-4052-8a5a-6f2b4e2fb72d",
        #                 "port_number": 0
        #             }
        #         ],
        #         "project_id": "8cf37f7e-76a1-418c-9317-82e8586a1560",
        #         "suspend": False
        #     },
        #     {
        #         "capture_compute_id": None,
        #         "capture_file_name": None,
        #         "capture_file_path": None,
        #         "capturing": False,
        #         "filters": {},
        #         "link_id": "8a95382f-653f-4777-9b41-520a610ddbaf",
        #         "link_type": "ethernet",
        #         "nodes": [
        #             {
        #                 "adapter_number": 0,
        #                 "label": {
        #                     "rotation": 0,
        #                     "style": "font-family: TypeWriter;font-size: 10.0;font-weight: bold;fill: #000000;fill-opacity: 1.0;",
        #                     "text": "e2",
        #                     "x": 28,
        #                     "y": -23
        #                 },
        #                 "node_id": "27515250-dbac-422e-9e11-1eefaf7ae76b",
        #                 "port_number": 2
        #             },
        #             {
        #                 "adapter_number": 0,
        #                 "label": {
        #                     "rotation": 0,
        #                     "style": "font-family: TypeWriter;font-size: 10.0;font-weight: bold;fill: #000000;fill-opacity: 1.0;",
        #                     "text": "eth0",
        #                     "x": 39,
        #                     "y": 68
        #                 },
        #                 "node_id": "914d1c91-f727-4c95-a767-cb831b4fd264",
        #                 "port_number": 0
        #             }
        #         ],
        #         "project_id": "8cf37f7e-76a1-418c-9317-82e8586a1560",
        #         "suspend": False
        #     },
        #     {
        #         "capture_compute_id": None,
        #         "capture_file_name": None,
        #         "capture_file_path": None,
        #         "capturing": False,
        #         "filters": {},
        #         "link_id": "7d88732d-4c7c-455b-9f1a-d9d7a5774149",
        #         "link_type": "ethernet",
        #         "nodes": [],
        #         "project_id": "8cf37f7e-76a1-418c-9317-82e8586a1560",
        #         "suspend": False
        #     },
        #     {
        #         "capture_compute_id": None,
        #         "capture_file_name": None,
        #         "capture_file_path": None,
        #         "capturing": False,
        #         "filters": {},
        #         "link_id": "67c8e9b7-a8e5-4bce-9291-8fe491cf3a39",
        #         "link_type": "ethernet",
        #         "nodes": [],
        #         "project_id": "8cf37f7e-76a1-418c-9317-82e8586a1560",
        #         "suspend": False
        #     }
        # ]
        self.assertTrue(self.nm.get_all_links() is not [])

    def test_get_all_nodes(self):
        # expected =[
        #     {
        #         "name": "AlpineLinux-1",
        #         "node_id": "914d1c91-f727-4c95-a767-cb831b4fd264"
        #     },
        #     {
        #         "name": "thomasbeckers-alpine-python3-1",
        #         "node_id": "fac28a86-2be5-4219-832c-a06837389ff7"
        #     },
        #     {
        #         "name": "PC1",
        #         "node_id": "72e118c6-6799-4291-8fed-41d8c75fc522"
        #     },
        #     {
        #         "name": "PC2",
        #         "node_id": "97e285e3-f752-4052-8a5a-6f2b4e2fb72d"
        #     },
        #     {
        #         "name": "Switch1",
        #         "node_id": "27515250-dbac-422e-9e11-1eefaf7ae76b"
        #     }
        # ]
        self.assertTrue(self.nm.get_all_nodes() is not [])

    def test_get_all_project(self):
        # expected =[
        #     {
        #         "auto_close": True,
        #         "auto_open": False,
        #         "auto_start": False,
        #         "drawing_grid_size": 25,
        #         "filename": "proto1.gns3",
        #         "grid_size": 75,
        #         "name": "proto1",
        #         "path": "/Users/maximebeugoms/GNS3/projects/proto1",
        #         "project_id": "8cf37f7e-76a1-418c-9317-82e8586a1560",
        #         "scene_height": 1000,
        #         "scene_width": 2000,
        #         "show_grid": False,
        #         "show_interface_labels": True,
        #         "show_layers": False,
        #         "snap_to_grid": True,
        #         "status": "opened",
        #         "supplier": None,
        #         "variables": None,
        #         "zoom": 35
        #     }
        # ]
        self.assertTrue(self.nm.get_all_project() is not [])

    def test_get_all_snapshots(self):
        # expected =[
        #     {
        #         "created_at": 1584656065,
        #         "name": "snapshot_testing_nm",
        #         "project_id": "8cf37f7e-76a1-418c-9317-82e8586a1560",
        #         "snapshot_id": "0ab187e5-2f4b-41d1-9b6d-8f7ecc57c988"
        #     }
        # ]
        self.assertTrue(self.nm.get_all_snapshots() is not [])

    def test_post_template(self):
        machine_template = {
                "adapters": 1,
                "builtin": False,
                "category": "guest",
                "compute_id": "vm",
                "console_auto_start": False,
                "console_http_path": "/",
                "console_http_port": 80,
                "console_resolution": "1024x768",
                "console_type": "telnet",
                "custom_adapters": [],
                "default_name_format": "{name}-{0}",
                "environment": "",
                "extra_hosts": "",
                "extra_volumes": [],
                "image": "gns3/ubuntu:xenial",
                "name": "Ubuntu Docker Guest",
                "start_command": "",
                "symbol": "linux_guest.svg",
                "template_id": "d15fb3d1-0ba1-43d9-a725-e286bb6c1e56",
                "template_type": "docker",
                "usage": ""
            }
        # result_expected = {
        #     "command_line": None,
        #     "compute_id": "vm",
        #     "console": 5009,
        #     "console_auto_start": False,
        #     "console_host": "192.168.56.104",
        #     "console_type": "telnet",
        #     "custom_adapters": [],
        #     "first_port_name": None,
        #     "height": 59,
        #     "label": {
        #         "rotation": 0,
        #         "style": None,
        #         "text": "UbuntuDockerGuest-1",
        #         "x": None,
        #         "y": -40
        #     },
        #     "locked": False,
        #     "name": "UbuntuDockerGuest-1",
        #     "node_directory": "/opt/gns3/projects/8cf37f7e-76a1-418c-9317-82e8586a1560/project-files/docker/49cfbb85-a553-48cb-9193-c66c411339e8",
        #     "node_id": "49cfbb85-a553-48cb-9193-c66c411339e8",
        #     "node_type": "docker",
        #     "port_name_format": "Ethernet{0}",
        #     "port_segment_size": 0,
        #     "ports": [
        #         {
        #             "adapter_number": 0,
        #             "data_link_types": {
        #                 "Ethernet": "DLT_EN10MB"
        #             },
        #             "link_type": "ethernet",
        #             "name": "eth0",
        #             "port_number": 0,
        #             "short_name": "eth0"
        #         }
        #     ],
        #     "project_id": "8cf37f7e-76a1-418c-9317-82e8586a1560",
        #     "properties": {
        #         "adapters": 1,
        #         "aux": 5010,
        #         "console_http_path": "/",
        #         "console_http_port": 80,
        #         "console_resolution": "1024x768",
        #         "container_id": "4aa379c99a5a8cc64dcd6155cf511b394019794c3852deec0977537cba63980c",
        #         "environment": None,
        #         "extra_hosts": None,
        #         "extra_volumes": [],
        #         "image": "gns3/ubuntu:xenial",
        #         "start_command": None,
        #         "usage": ""
        #     },
        #     "status": "stopped",
        #     "symbol": "linux_guest.svg",
        #     "template_id": "d15fb3d1-0ba1-43d9-a725-e286bb6c1e56",
        #     "width": 65,
        #     "x": 200,
        #     "y": 300,
        #     "z": 1
        # }
        self.assertTrue(self.nm.post_template(machine_template,300,100) is not {})


    def test_create_template_by_name(self):
        self.assertEqual('d15fb3d1-0ba1-43d9-a725-e286bb6c1e56', self.nm.create_template_by_name('Ubuntu Docker Guest',300,200)['template_id'])

    def test_create_template_by_id(self):
        self.assertEqual('d15fb3d1-0ba1-43d9-a725-e286bb6c1e56', self.nm.create_template_by_id('d15fb3d1-0ba1-43d9-a725-e286bb6c1e56',300,300)['template_id'])

    def test_get_one_machine_by_id(self):
        expected_machine = {
                "compute_id": "vm",
                "name": "GNS3 VM (GNS3 VM)"
            }
        self.assertEqual(expected_machine, self.nm.get_one_machine_by_id(expected_machine['compute_id']))

    def test_get_one_machine_by_name(self):
        expected_machine = {
            "compute_id": "vm",
            "name": "GNS3 VM (GNS3 VM)"
        }
        self.assertEqual(expected_machine, self.nm.get_one_machine_by_name(expected_machine['name']))

    def test_set_current_machine(self):
        expected_machine = {
            "compute_id": "vm",
            "name": "GNS3 VM (GNS3 VM)"
        }
        self.assertEqual(expected_machine, self.nm.selected_machine)

    # def test_post_drawing(self):
    #     self.fail()
    #
    # def test_get_drawing(self):
    #     self.fail()
    #
    # def test_put_drawing(self):
    #     self.fail()
    #
    # def test_delete_drawing(self):
    #     self.fail()
    #

    def test_link_method(self):
        # Test create link between 2 nodes
        self.nm.create_template_by_name('Firefox',200,200)
        self.nm.create_template_by_name('Alpine',200,300)
        node1 = self.nm.get_one_node_by_name('Firefox')
        node2 = self.nm.get_one_node_by_name('Alpine')

        result = self.nm.link_nodes(node1['node_id'], node2['node_id'])

        self.assertTrue(result is not {})

        list_link = self.nm.get_all_links()

        # Test to get one specific link
        result= self.nm.get_one_link(list_link[0]['link_id'])
        self.assertEqual(list_link[0],result)

        # Infos about link
        result = self.nm.get_link_node(node1['node_id'])
        self.assertTrue(result is not [])

        # Test the capture on a link
        # Starting
        # self.nm.start_node(node1['node_id'])
        # self.nm.start_node(node2['node_id'])
        # result = self.nm.start_capture_link(list_link[0]['link_id'])
        # self.assertEqual(201, result.status_code)
        # sleep(1)
        # # Stopping
        # result = self.nm.stop_capture_link(list_link[0]['link_id'])
        # self.assertEqual(201,result.status_code)
        # # Get the capturing file
        # result = self.nm.get_pcap_link(list_link[0]['link_id'])
        # self.assertEqual(200, result.status_code)
        #
        # self.nm.stop_node(node1['node_id'])
        # self.nm.stop_node(node2['node_id'])

        # Test to delete on specific link
        result = self.nm.delete_link(list_link[0]['link_id'])
        self.assertEqual(204, result.status_code)

        self.nm.delete_node(node1['node_id'])
        self.nm.delete_node(node2['node_id'])

    def test_node_method(self):
        list_nodes = self.nm.get_all_nodes()
        # Update node
        self.nm.put_node(list_nodes[0]['node_id'],{'x':300,'y':300})
        # Get specific node
        result = self.nm.get_one_node_by_id(list_nodes[0]['node_id'])
        result = self.nm.get_one_machine_by_name(list_nodes[0]['name'])

        # Duplicate node
        self.nm.duplicate_node(list_nodes[0]['node_id'], {'x': 400, 'y': 300})

        # Starting node
        self.nm.start_node(list_nodes[0]['node_id'])
        # Stopping node
        self.nm.stop_node(list_nodes[0]['node_id'])
        # General manage
        self.nm.start_all_nodes()
        self.nm.stop_all_node()
        self.nm.reload_all_node()
        self.nm.stop_all_node()
        # File manager
        result = self.nm.add_file_to_node(list_nodes[0]['node_id'], "/tmp/test.txt","Hello word!")
        self.assertEqual(201,result.status_code)

        # Delete specific node
        self.nm.delete_node(list_nodes[0]['node_id'])

    def test_method_snapshot(self):
        result = self.nm.post_snapshot({'name': 'snap_test'})

        self.assertEqual(201, result.status_code)
        result = result.json()
        list_snaps = self.nm.get_all_snapshots()
        snap_id=''
        for snap in list_snaps:
            if snap['name']=='snap_test':
                snap_id= snap['snapshot_id']
        # print(list_snaps)
        # res = self.nm.restore_snapshot(snap_id)
        # self.assertEqual(201, res.status_code)

        res = self.nm.delete_snapshot(snap_id)
        self.assertEqual(204, res.status_code)



