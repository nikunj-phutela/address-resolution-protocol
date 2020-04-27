import subprocess as sp
import os


class netsError(Exception):
    # raised from nets if exception found
    pass


class nets():

    def __init__(self):
        self.system = os.name # Operating System type; nt - Windows; posix - UNIX
        self.privateAddress = '' #  System Private IP
        self.subnetMask = '' #  System Subnet Mask
        self.defaultGateway = '' #  System Default Gateway
        self.publicAddress = '' #   TO BE DONE - System Public Address
        self.broadcast = '' # Broadcast IP Address; TO BE DONE for nt
        self.NeighbourIp = '' # ip neigh show for UNIX; Windows(?)
        self.dontExit = 1 # Menu looper variable
        self.ARPMac = ''
        self.arpInput = ''
        start = self.privateAddress.split(".")
        start.pop(-1)
        start = '.'.join(start)
        start += "."
        for i in range(255):
            sp.Popen("ping -c 1 " + start + str(i), stdin=sp.PIPE, shell=True, stdout=sp.PIPE, stderr=sp.PIPE)

        self.getInformation()
        self.getNeighbourInfo()
        self.showMenu()

    def cleanNT(self, dPA, dSM, dDG):
        dPA = dPA.stdout.read().decode().splitlines()
        dSM = dSM.stdout.read().decode().splitlines()
        dDG = dDG.stdout.read().decode().splitlines()
        if(dPA):
            self.privateAddress = dPA[0].split(": ")[1]
        else:
            raise netsError("Empty Private Address")
        if(dSM):
            self.subnetMask = dSM[0].split(": ")[1]
        else:
            raise netsError("Empty Subnet Mask")
        if(dDG):
            self.defaultGateway = dDG[0].split(": ")[1]
        else:
            raise netsError("Empty Default Gateway")

    def cleanPOSIX(self, dI, dN):
        dI = dI.stdout.read().decode().splitlines()
        dISplit = dI[0].split()
        if(dI):
            self.privateAddress = dISplit[1].split(":")[1]
            self.subnetMask = dISplit[3].split(":")[1]
            self.broadcast = dISplit[2].split(":")[1]

        if(dN):
            self.defaultGateway = dN = dN.stdout.read().decode().split()[3]

    def getInformation(self):
        if self.system == "nt":
            dirtyPrivateAddress = sp.Popen(
                "ipconfig | findstr IPv4", stdin=sp.PIPE, shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
            dirtySubnetMask = sp.Popen(
                "ipconfig | findstr Subnet", stdin=sp.PIPE, shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
            dirtyDefaultGateway = sp.Popen(
                "ipconfig | findstr Default", stdin=sp.PIPE, shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
            self.cleanNT(dirtyPrivateAddress,
                         dirtySubnetMask, dirtyDefaultGateway)
        elif self.system == "posix":
            dirtyInformation = sp.Popen(
                "ifconfig | grep -w 'broadcast\|Bcast'", stdin=sp.PIPE, shell=True, stdout=sp.PIPE, stderr=sp.PIPE)

            dirtyDefaultGateway = sp.Popen(
                "ip route| grep default", stdin=sp.PIPE, shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
            self.cleanPOSIX(dirtyInformation, dirtyDefaultGateway)

        else:
            raise netsError("Program could not detect your OS Version.")

    def getNeighbourInfo(self):
        if(self.system) == "posix":
            dirtyNeighbourIp = sp.Popen(
                "ip neigh show", stdin=sp.PIPE, shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
            dirtyNeighbourIp = dirtyNeighbourIp.stdout.read().decode().splitlines()
            for lines in dirtyNeighbourIp:
                self.NeighbourIp = self.NeighbourIp + lines.split()[0] + " "

    def allInfo(self):
        print("Private IP Address: ", self.privateAddress)
        print("Subnet Mask: ", self.subnetMask)
        print("Default Gateway: ", self.defaultGateway)
        print("Broadcast IP: ", self.broadcast)
        print("Neighbouring IPs: ", self.NeighbourIp)
        return

    def priIP(self): # Prints System Private IP Address
        print("Private IP Address: ", self.privateAddress)
        return

    def subMask(self): # Prints Subnet Mask
        print("Subnet Mask: ", self.subnetMask)
        return

    def defGat(self): # Prints Default Gateway
        print("Default Gateway: ", self.defaultGateway)
        return

    def broadIP(self): # Prints Broadcast IP
        print("Broadcast IP: ", self.broadcast)
        return

    def neigh(self): # ip neigh show on UNIX
        print("Neighbouring IPs: ", self.NeighbourIp)
        return

    def exitMenu(self): # Terminate loop and program
        self.dontExit = 0
        print("Exiting program")
        return

    def runARP(self):
        self.arpInput = input("Enter IP Address to find MAC address for: ")
        out1 = sp.Popen("ping -c 1 " + self.arpInput, stdin=sp.PIPE, shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
        out2 = sp.Popen("arp -n | grep " + self.arpInput, stdin=sp.PIPE, shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
        self.ARPMac = out2.stdout.read().decode().split()[2]
        print("Ethernet address for " + self.arpInput + ": " + self.ARPMac)
        return

    def revARP(self):
        inp = input("Enter MAC Address to find IP for: ")
        out2 = sp.Popen("arp -n | grep " + inp, stdin=sp.PIPE, shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
        out2 = out2.stdout.read().decode().split()[0]
        print("MAC Address for: " + inp + ": " + out2)


    def printMenu(self): # Menu for user to choose key
        print("Choose an option from the below, and enter the key: ")
        print("1: Private IP Address")
        print("2: Subnet Mask")
        print("3: Default Gateway")
        print("4: Broadcast IP Address")
        print("5: Neighbor IPs")
        print("6: All Information")
        print("7: ARP")
        print("8: Reverse ARP")
        print("9: Exit")
        return "\n"

    def showMenu(self): # Function to map index to function
        dictMenu = {
            1: self.priIP,
            2: self.subMask,
            3: self.defGat,
            4: self.broadIP,
            5: self.neigh,
            6: self.allInfo,
            7: self.runARP,
            8: self.revARP,
            9: self.exitMenu
        }
        while(self.dontExit):
            self.printMenu()
            index = int(input("\nEnter the key: "))
            dictMenu.get(index, lambda: "Invalid index.")()
            print()
        return ("Program run successfully.")




