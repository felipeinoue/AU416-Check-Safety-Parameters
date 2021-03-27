import xml.etree.ElementTree as ET

# parse xml file
root = ET.parse('k6spcl1.xml').getroot()

def GetParameter(DevType, ls_Port, ls_VarName):

# [ok]01_PSDI_NotHalt_Antriebe_Zustimmung_2k1_V01
# [ok]01_PSDI_NotHalt_Antriebe_Zustimmung_2k2_V01
# 02_PSDI_OSSD_E2_2k_V01
# 04_PSDI_Stopzylinder_FreigabeAntriebeEinRoboter_1k_V01
# 05_PSDI_InbetriebnahmeBruecke_2k1_V01
# 05_PSDI_InbetriebnahmeBruecke_2k2_V01
# 06_PSDI_Zweihand_2k1_V01
# 06_PSDI_Zweihand_2k2_V01
# 07_PSDI_GATEWAY_2k_V01
# [ok]08_PSDI_AlbanyTor_Reed_2k1_V01
# [ok]08_PSDI_AlbanyTor_Reed_2k2_V01
# 10_PSDO8_2k_V01
# 11_PSDO8_1k_V01
# 12_PSDO4_4_PLUS_MINUS_2k_V01
# 13_PSDO4_4_PLUS_1k_V01
# [ok]14_PSDOR_2k_V01
# 15_PSDOR_1k_V01
# 16_PSDOR_2k_EDM_IN1_V01
# 17_PSDOR_2k_EDM_IN2_V01
# 18_PSDOR_1k_EDM_IN1_V01
# 19_PSDOR_1k_EDM_IN2_V01
# 20_PSDO8_ELR_H3_H5_1k_V01

    # start variables
    ls = []
    DevicesConfig = [

        # 01_PSDI_NotHalt_Antriebe_Zustimmung_2k1_V01
        {
            "DevType": 'PSDI',
            "Port": 'Kanal 1',
            "Symbols": ['SN', 'FK16', 'FK36', 'SWE2'],
            "ParameterChannel1": '01_PSDI_NotHalt_Antriebe_Zustimmung_2k1_V01',
            "ParameterChannel2": '01_PSDI_NotHalt_Antriebe_Zustimmung_2k2_V01'
        },

        # 02_PSDI_OSSD_E2_2k_V01
        {
            "DevType": 'PSDI',
            "Port": 'Kanal 1',
            "Symbols": ['E_2PSDI', 'BG', 'A1BE'],
            "ParameterChannel1": '02_PSDI_OSSD_E2_2k_V01',
            "ParameterChannel2": '02_PSDI_OSSD_E2_2k_V01'
        },

        # 08_PSDI_AlbanyTor_Reed_2k1_V01
        {
            "DevType": 'PSDI',
            "Port": 'Kanal 1',
            "Symbols": ['SF1B7'],
            "ParameterChannel1": '08_PSDI_AlbanyTor_Reed_2k1_V01',
            "ParameterChannel2": '08_PSDI_AlbanyTor_Reed_2k2_V01'
        },

        # 14_PSDOR_2k_V01
        {
            "DevType": 'PSDOR',
            "Port": 'Kanal 1',
            "Symbols": ['K16','K36','K1SK1','K2SK1','K1NH','K2NH','SV','_STO'],
            "ParameterChannel1": '14_PSDOR_2k_V01',
            "ParameterChannel2": '14_PSDOR_2k_V01'
        }

    ]

    i = 0
    while i < len(ls_Port):

        # Look for Match case in DevicesConfig
        VarFound = False
        for DeviceConfig in DevicesConfig:

            if (
                DeviceConfig['DevType'] in DevType and
                DeviceConfig['Port'] in ls_Port[i] and (
                    any(s in ls_VarName[i] for s in DeviceConfig['Symbols'])
                )
            ):
                # Channel 1
                ls.append(DeviceConfig['ParameterChannel1'])

                # Channel 2
                try:
                    if DeviceConfig['ParameterChannel2']:
                        i += 1
                        ls.append(DeviceConfig['ParameterChannel2'])
                except:
                    pass

                VarFound = True
                break

        # Var Reserve or not found
        if not VarFound:

            #  Var Reserve
            if ls_VarName[i] == 'Reserve':
                ls.append('not used')

            # Var not found
            else:
                ls.append('Parameter not found')

        # increment
        i += 1

    # return list with parameters
    return ls


def GetDevTypeDict(root):
    # start variables
    ls_DevType = [
        "IB IL 24 PSDI 8 PAC PROFIsafe",
        "IB IL 24 PSDOR 4-PAC PROFIsafe"
    ]
    DevTypeDict = {}

    for DevType in ls_DevType:

        # get oid
        ls_dummy = root.findall(f".//*[@name='{DevType}']")
        oid = ls_dummy[0].get('id')

        # get rid
        ls_dummy = root.findall(f".//*[@oid='{oid}']")
        rid = ls_dummy[0].get('id')

        DevTypeDict[rid] = DevType

    return DevTypeDict


# start variables
ls_Devices = []

# get Device Type Dictonary
DevTypeDict = GetDevTypeDict(root)

# get all possible devices
ls_Device = root.findall(".//*[@name='Device']")

# iterate on devices
for device in ls_Device:

    # start variables
    ModuleEquipmentId = ''
    DevType = ''
    ls_Port = []
    ls_VarName = []
    ls_Parameter = []

    # get Module Equipment Id
    ls_ModuleEquipmentId = device.findall(".//*[@name='awxTop.devModuleEquipmentId']")
    try:
        ModuleEquipmentId = ls_ModuleEquipmentId[0].text
    except:
        ModuleEquipmentId = 'Module Equipment Id not found'

    # get Device Type
    ls_Devtype = device.findall(".//*[@name='awxTop.refDevType']")
    try:
        DevType = DevTypeDict[ls_Devtype[0].attrib["rid"]]
    except:
        DevType = 'Device not found'
        # skip not found devices, go to next iteration
        continue

    # get all Device Terminal
    ls_DeviceTerminal = device.findall(".//*[@type='awxTop.deviceTerminal']")

    # get Device Terminal
    for DeviceTerminal in ls_DeviceTerminal:

        # get devTerminalSignalName and devTerminalVarName
        ls_devTerminalSignalName = DeviceTerminal.findall(".//*[@name='awxTop.devTerminalSignalName']")
        ls_devTerminalVarName = DeviceTerminal.findall(".//*[@name='awxTop.devTerminalVarName']")
    
        # check if devTerminalSignalName is not empty append texts
        if ls_devTerminalSignalName[0].text:
            ls_Port.append(ls_devTerminalSignalName[0].text)
            ls_Parameter.append('')
            if ls_devTerminalVarName[0].text:
                ls_VarName.append(ls_devTerminalVarName[0].text)
            else:
                ls_VarName.append('Reserve')

    # get Parameters
    ls_Parameter = GetParameter(DevType, ls_Port, ls_VarName)

    # create dictonary
    elements_dict = {
        "ModuleEquipmentId": ModuleEquipmentId, #IEKA111
        "DevType": DevType, #24275, IB IL 24 PSDI 8 PAC PROFIsafe
        "ls_Port": ls_Port, #Eingang 0 Kanal 1 (und 2)
        "ls_VarName": ls_VarName, #IESN1
        "ls_Parameter": ls_Parameter #2k2estop
    }

    # append to Device list
    ls_Devices.append(elements_dict)

with open("file.txt", "w") as output:
    output.write(str(ls_Devices))

fim = 'fim'