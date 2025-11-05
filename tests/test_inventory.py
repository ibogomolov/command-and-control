from program.inventory import Inventory, InventoryException
from tests.fixtures import FileTestCase


class TestInventory(FileTestCase):
    def test_from_file_success(self):
        hosts = """
        [webservers]
        one.example.com
        bar.example.com
        
        [dbservers]
        one.example.com
        two.example.com
        three.example.com"""
        self.create_hosts_file_from_text(hosts)

        inv = Inventory.from_file(self.hosts_file)
        self.assertListEqual(list(inv._hosts.keys()), ["webservers", "dbservers"])
        self.assertListEqual(inv._hosts["webservers"], ["one.example.com", "bar.example.com"])
        self.assertListEqual(inv._hosts["dbservers"], ["one.example.com", "two.example.com", "three.example.com"])

    def test_from_file_duplicate_host(self):
        hosts = """
        [dbservers]
        one.example.com
        one.example.com
        three.example.com"""
        self.create_hosts_file_from_text(hosts)

        with self.assertRaises(InventoryException) as context:
            Inventory.from_file(self.hosts_file)

        self.assertEqual(str(context.exception), "Hosts file contains duplicate host in a group")

    def test_from_file_duplicate_group(self):
        hosts = """
        [dbservers]
        one.example.com
        
        [dbservers]
        two.example.com"""
        self.create_hosts_file_from_text(hosts)

        with self.assertRaises(InventoryException) as context:
            Inventory.from_file(self.hosts_file)

        self.assertEqual(str(context.exception), "Hosts file contains duplicate group")

    def test_from_file_host_outside_of_group(self):
        hosts = """
        one.example.com
        
        [dbservers]
        two.example.com"""
        self.create_hosts_file_from_text(hosts)

        with self.assertRaises(InventoryException) as context:
            Inventory.from_file(self.hosts_file)

        self.assertEqual(str(context.exception), "Hosts file contains hosts declared outside of a group")

    def test_get_hosts_by_group_success(self):
        hosts = """
        [dbservers]
        one.example.com
        two.example.com
        three.example.com"""
        self.create_hosts_file_from_text(hosts)
        inv = Inventory.from_file(self.hosts_file)

        self.assertListEqual(inv.get_hosts_by_group("dbservers"),
                             ["one.example.com", "two.example.com", "three.example.com"])

    def test_get_hosts_by_group_absent_group(self):
        hosts = """
        [dbservers]
        one.example.com
        two.example.com
        three.example.com"""
        self.create_hosts_file_from_text(hosts)
        inv = Inventory.from_file(self.hosts_file)

        with self.assertRaises(InventoryException) as context:
            inv.get_hosts_by_group("webservers")

        self.assertEqual(str(context.exception), "Group 'webservers' is absent from the hosts file")

    def test_get_hosts_by_group_no_hosts(self):
        hosts = """
        [dbservers]"""
        self.create_hosts_file_from_text(hosts)
        inv = Inventory.from_file(self.hosts_file)

        with self.assertRaises(InventoryException) as context:
            inv.get_hosts_by_group("dbservers")

        self.assertEqual(str(context.exception), "Group 'dbservers' has no hosts")
