# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'TextEditor.ui'
#
# Created: Tue Jan 20 18:04:35 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(503, 300)
        self.plainTextEdit = QtGui.QPlainTextEdit(Form)
        self.plainTextEdit.setGeometry(QtCore.QRect(0, 0, 501, 291))
        self.plainTextEdit.setObjectName("plainTextEdit")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.plainTextEdit.setPlainText(QtGui.QApplication.translate("Form", ";; Ontology of Communication Concepts used in the CIA World Fact Book 2002\n"
"\n"
";; Access to and use of these products is governed by the GNU General Public \n"
";; License <http://www.gnu.org/copyleft/gpl.html>. \n"
";; By using these products, you agree to be bound by the terms \n"
";; of the GPL.\n"
"\n"
";; Those who are interested in making use of this ontology are urged \n"
";; to contact Adam Pease (apease@articulatesoftware.com).\n"
";; We ask the people using or referencing this work cite our primary paper:\n"
"\n"
";; Niles, I., and Pease, A.  2001.  Towards a Standard Upper Ontology.  In \n"
";; Proceedings of the 2nd International Conference on Formal Ontology in \n"
";; Information Systems (FOIS-2001), Chris Welty and Barry Smith, eds, \n"
";; Ogunquit, Maine, October 17-19, 2001.  See also www.ontologyportal.org \n"
"\n"
";; \n"
";; ==========================================================================\n"
";; VI. Communications\n"
"\n"
"(subclass CommunicationRadio CommunicationDevice)\n"
"(documentation CommunicationRadio EnglishLanguage \"Relatively low power broadcasting\n"
"devices designed for voice communication among specialized groups\n"
"in which each receiver also has the power to transmit, unlike\n"
"broadcast radio where most components transmitting or receiving on\n"
"a given frequency or set of frequencies are receivers only.  This \n"
"includes unlicensed walkie-talkies, public safety radios, military\n"
"communication systems and CB radios.\")\n"
"\n"
";;     A. Telephones - main lines in use\n"
"\n"
"(subclass TelephoneSystem CommunicationSystem)\n"
"(documentation TelephoneSystem EnglishLanguage \"A &%TelephoneSystem consists of a complete\n"
"interconnection of &%Telephones, &%MainTelephoneLines, and other components\n"
"that work together to make telephonic communication possible from point to\n"
"point in a given area.\")\n"
"\n"
"(termFormat EnglishLanguage Telephone \"telephone\")\n"
"\n"
"(=>\n"
"    (instance ?SYSTEM TelephoneSystem)\n"
"    (exists (?PHONE)\n"
"        (and\n"
"            (instance ?PHONE Telephone)\n"
"            (engineeringSubcomponent ?PHONE ?SYSTEM))))\n"
"\n"
"(subclass MainTelephoneLine CommunicationDevice)\n"
"(synonymousExternalConcept \"main telephone line\" MainTelephoneLine EnglishLanguage)\n"
"(documentation MainTelephoneLine EnglishLanguage \"A &%MainTelephoneLine is one \n"
"&%engineeringSubcomponent of a &%TelephoneSystem used for voice communication \n"
"or computer data transfer.\")\n"
"(=>\n"
"    (instance ?SYSTEM TelephoneSystem)\n"
"    (exists (?LINE)\n"
"        (and\n"
"            (instance ?LINE MainTelephoneLine)\n"
"            (engineeringSubcomponent ?LINE ?SYSTEM))))\n"
"\n"
"(subclass TelephoneCradle Device)\n"
"(documentation TelephoneCradle EnglishLanguage \"&%TelephoneCradle is the part of the\n"
"&%Telephone that is connected to the &%TelephoneSystem through some wire.\")\n"
"(termFormat EnglishLanguage TelephoneCradle \"telephone cradle\")\n"
"\n"
"(=>\n"
"  (instance ?X TelephoneCradle)\n"
"  (hasPurpose ?X\n"
"    (exists (?SYS ?WIRE)\n"
"      (and\n"
"        (instance ?SYS TelephoneSystem)\n"
"        (instance ?WIRE WireLine)\n"
"        (connectsEngineeringComponents ?WIRE ?X ?SYS)))))      \n"
"\n"
"(subclass CordedTelephone FixedPhone)\n"
"(documentation CordedTelephone EnglishLanguage \"&%CordedTelephone is a type of &%FixedPhone \n"
"whose &%TelephoneHandset is connected to its &%TelephoneCradle by a &%WireLine\")\n"
"(termFormat EnglishLanguage CordedTelephone \"corded telephone\")\n"
"\n"
"(=>\n"
"  (instance ?X CordedTelephone)\n"
"  (exists (?HANDSET ?CRADLE ?WIRE)\n"
"    (and\n"
"      (instance ?HANDSET TelephoneHandset)\n"
"      (instance ?CRADLE TelephoneCradle)\n"
"      (part ?HANDSET ?X)\n"
"      (part ?CRADLE ?X)\n"
"      (instance ?WIRE WireLine)\n"
"      (connectsEngineeringComponents ?WIRE ?HANDSET ?CRADLE))))\n"
"        \n"
"(subclass CordlessTelephone FixedPhone)\n"
"(documentation CordlessTelephone EnglishLanguage \"&%CordlessTelephone is a type of \n"
"&%FixedPhone whose &%TelephoneHandset is not connected to its &%TelephoneCradle by a \n"
"&%WireLine\")\n"
"(termFormat EnglishLanguage CordlessTelephone \"cordless telephone\")\n"
"\n"
"(=>\n"
"  (instance ?X CordlessTelephone)\n"
"  (exists (?HANDSET ?CRADLE)\n"
"    (and\n"
"      (instance ?HANDSET TelephoneHandset)\n"
"      (instance ?CRADLE TelephoneCradle)\n"
"      (part ?HANDSET ?X)\n"
"      (part ?CRADLE ?X)\n"
"      (not \n"
"        (exists (?WIRE)\n"
"          (and\n"
"            (instance ?WIRE WireLine)\n"
"            (connectsEngineeringComponents ?WIRE ?HANDSET ?CRADLE)))))))\n"
"        \n"
";;    B. Telephones - mobile cellular\n"
"\n"
";;    C. Telephone system\n"
"(subclass ArtificialSatellite Satellite)\n"
"(subclass ArtificialSatellite EngineeringComponent)\n"
"(termFormat EnglishLanguage ArtificialSatellite \"satellite\")\n"
"(documentation ArtificialSatellite EnglishLanguage \"An &%ArtificialSatellite is a &%Device\n"
"that orbits the earth in space and performs various functions such as\n"
"aiding in communication, photographing the earth\'s surface, and others.\")\n"
"\n"
"(subclass CommunicationSatellite ArtificialSatellite)\n"
"(subclass CommunicationSatellite CommunicationDevice)\n"
"(termFormat EnglishLanguage CommunicationSatellite \"communications satellite\")\n"
"(documentation CommunicationSatellite EnglishLanguage \"A &%CommunicationSatellite is an\n"
"&%ArtificialSatellite that serves as one &%engineeringSubcomponent of a \n"
"&%CommunicationSystem.\")\n"
"(=>\n"
"    (instance ?SAT CommunicationSatellite)\n"
"    (exists (?SYSTEM)\n"
"        (and\n"
"            (instance ?SYSTEM CommunicationSystem)\n"
"            (engineeringSubcomponent ?SAT ?SYSTEM))))\n"
"\n"
"(instance communicationSatelliteForArea TernaryPredicate)\n"
"(domain communicationSatelliteForArea 1 GeopoliticalArea)\n"
"(domainSubclass communicationSatelliteForArea 2 Satellite)\n"
"(domain communicationSatelliteForArea 3 Integer)\n"
"(documentation communicationSatelliteForArea EnglishLanguage \"The expression\n"
"(communicationSatelliteForArea ?AREA ?SATELLITE ?INTEGER) means that \n"
"?INTEGER number of &%CommunicationSatellites of the type ?SATELLITE serve\n"
"as an &%engineeringSubcomponent of a &%TelephoneSystem of the GeopoliticalArea\n"
"?AREA.\")\n"
"\n"
"(=>\n"
"    (communicationSatelliteForArea ?AREA ?SATELLITETYPE ?INTEGER)\n"
"    (equal ?INTEGER\n"
"        (CardinalityFn\n"
"            (KappaFn ?SATELLITE\n"
"                (and\n"
"                    (instance ?SATELLITE ?SATELLITETYPE)\n"
"                    (instance ?SYSTEM CommunicationSystem)\n"
"                    (located ?SYSTEM ?AREA)\n"
"                    (engineeringSubcomponent ?SATELLITE ?SYSTEM))))))\n"
"\n"
"(subclass Eutelsat CommunicationSatellite)\n"
"(documentation Eutelsat EnglishLanguage \"An &%Eutelsat is one type of \n"
"&%CommunicationSatellite.\")\n"
"\n"
"(subclass Inmarsat CommunicationSatellite)\n"
"(documentation Inmarsat EnglishLanguage \"An &%Inmarsat is one type of \n"
"&%CommunicationSatellite.\")\n"
"\n"
"(subclass Intelsat CommunicationSatellite)\n"
"(documentation Intelsat EnglishLanguage \"An &%Intelsat is one type of \n"
"&%CommunicationSatellite.\")\n"
"\n"
"(subclass Intersputnik CommunicationSatellite)\n"
"(documentation Intersputnik EnglishLanguage \"An &%Intersputnik is one type of \n"
"&%CommunicationSatellite.\")\n"
"\n"
"(subclass Orbita CommunicationSatellite)\n"
"(documentation Orbita EnglishLanguage \"An &%Orbita is one type of \n"
"&%CommunicationSatellite.\")\n"
"\n"
"(subclass Telex CommunicationDevice)\n"
"(documentation Telex EnglishLanguage \"&%Telex is a &%Telegraph-like &%CommunicationDevice \n"
"that is used to send messages over a &%TelephoneSystem.\")\n"
"(termFormat EnglishLanguage Telex \"telex\")\n"
"\n"
"(=>\n"
"  (instance ?TELEX Telex)\n"
"  (exists (?PRINTER)\n"
"    (and\n"
"      (instance ?PRINTER Printer)\n"
"      (part ?PRINTER ?TELEX))))\n"
"      \n"
"(=>\n"
"  (instance ?TELEX Telex)\n"
"  (hasPurpose ?TELEX\n"
"    (exists (?SYS ?TELEX2 ?MSG)\n"
"      (and\n"
"        (instance ?SYS TelephoneSystem)\n"
"        (instance ?TELEX2 Telex)\n"
"        (instance ?MSG Messaging)\n"
"        (or\n"
"          (and\n"
"            (origin ?MSG ?TELEX)\n"
"            (destination ?MSG ?TELEX2))\n"
"          (and\n"
"            (origin ?MSG ?TELEX2)\n"
"            (destination ?MSG ?TELEX)))\n"
"        (path ?MSG ?SYS)))))\n"
"\n"
"(=>\n"
"  (and\n"
"    (destination ?MSG ?TELEX)\n"
"    (instance ?MSG Messaging)\n"
"    (patient ?MSG ?M)\n"
"    (instance ?TELEX Telex))\n"
"  (exists (?PROC ?TEXT)\n"
"    (and\n"
"      (instrument ?PROC ?TELEX)\n"
"      (result ?PROC ?TEXT)\n"
"      (represents ?TEXT ?M)\n"
"      (instance ?TEXT Text)\n"
"      (before (BeginFn (WhenFn ?MSG)) (BeginFn (WhenFn ?PROC))))))\n"
"\n"
"\n"
";;    D. Radio broadcast stations\n"
"(subclass BroadcastingStation StationaryArtifact)\n"
"(subclass BroadcastingStation CommunicationDevice)\n"
"(engineeringSubcomponent BroadcastingStation CommunicationSystem)\n"
"(documentation BroadcastingStation EnglishLanguage \"A &%BroadcastingStation is\n"
"an &%engineeringSubcomponent of either a &%TelevisionSystem or\n"
"a &%RadioStation.\")\n"
"\n"
"(=>\n"
"    (instance ?STATION BroadcastingStation)\n"
"    (or\n"
"        (instance ?STATION TelevisionStation)\n"
"        (instance ?STATION RadioStation)))\n"
"\n"
"(subclass RadioSystem CommunicationSystem)\n"
"(documentation RadioSystem EnglishLanguage \"A &%RadioSystem consists of &%Radios, \n"
"&%RadioStations, and other components that work together to make \n"
"radio broadcasting possible in a given area.\")\n"
"\n"
"(subclass AMRadioSystem RadioSystem)\n"
"(documentation AMRadioSystem EnglishLanguage \"An &%AMRadioSystem consists of &%Radios, \n"
"&%AMRadioStations, and other components that work together to make \n"
"AM radio broadcasting possible in a given area.\")\n"
"\n"
"(subclass FMRadioSystem RadioSystem)\n"
"(documentation FMRadioSystem EnglishLanguage \"A &%FMRadioSystem consists of &%Radios, \n"
"&%FMRadioStations, and other components that work together to make \n"
"FM radio broadcasting possible in a given area.\")\n"
"\n"
"(subclass ShortwaveRadioSystem RadioSystem)\n"
"(documentation ShortwaveRadioSystem EnglishLanguage \"A &%ShortwaveRadioSystem consists \n"
"of &%Radios, &%ShortwaveRadioStations, and other components that work \n"
"together to make shortwave radio broadcasting possible in a given area.\")\n"
"\n"
"(subclass BabyMonitoringSystem RadioSystem)\n"
"(documentation BabyMonitoringSystem EnglishLanguage \"&%BabyMonitoringSystem refers to\n"
"the radio system that &%Broadcasting at 49Mhz, consisting of a transmitter and receiver,\n"
"where the transmitter is kept where the baby is kept, and the receiver is kept with\n"
"the person looking after the baby to be able to hear sounds and monitor the baby\")\n"
"(termFormat EnglishLanguage BabyMonitoringSystem \"baby monitor\")\n"
"\n"
"(=>\n"
"  (instance ?X BabyMonitoringSystem)\n"
"  (exists (?TX ?RX)\n"
"    (and\n"
"      (instance ?RX RadioReceiver)\n"
"      (instance ?TX Device)\n"
"      (engineeringSubcomponent ?RX ?X)\n"
"      (engineeringSubcomponent ?TX ?X)\n"
"      (hasPurpose ?X\n"
"        (exists (?BABY ?CARER ?SOUND ?LOC1 ?LOC2 ?PROC ?RADIO)\n"
"          (and\n"
"            (instance ?BABY HumanBaby)\n"
"            (instance ?CARER Human)\n"
"            (located ?BABY ?LOC1)\n"
"            (located ?CARER ?LOC2)\n"
"            (not (equal ?LOC1 ?LOC2))\n"
"            (instance ?PROC Maintaining)\n"
"            (patient ?PROC ?BABY)\n"
"            (agent ?PROC ?CARER)\n"
"            (located ?TX ?LOC1)\n"
"            (located ?RX ?LOC2)\n"
"            (instance ?SOUND RadiatingSound)\n"
"            (eventLocated ?SOUND ?LOC1)\n"
"            (instance ?RADIO RadioEmission)\n"
"            (patient ?RADIO ?SOUND)\n"
"            (destination ?RADIO ?RX)\n"
"            (agent ?RADIO ?TX)))))))\n"
"            \n"
"\n"
"(subclass RadioStation BroadcastingStation)\n"
"(subclass BroadcastingStation EngineeringComponent)\n"
"(engineeringSubcomponent RadioStation RadioSystem)\n"
"(documentation RadioStation EnglishLanguage \"A &%RadioStation is an \n"
"&%engineeringSubcomponent of a &%RadioSystem.\")\n"
"\n"
"(subclass AMRadioStation RadioStation)\n"
"(engineeringSubcomponent AMRadioStation RadioSystem)\n"
"(documentation AMRadioStation EnglishLanguage \"An &%AMRadioStation is an \n"
"&%engineeringSubcomponent of an &%AMRadioSystem.\")\n"
"\n"
"(subclass FMRadioStation RadioStation)\n"
"(engineeringSubcomponent FMRadioStation RadioSystem)\n"
"(documentation FMRadioStation EnglishLanguage \"A &%FMRadioStation is an \n"
"&%engineeringSubcomponent of an &%FMRadioSystem.\")\n"
"\n"
"(subclass ShortwaveRadioStation RadioStation)\n"
"(engineeringSubcomponent ShortwaveRadioStation RadioSystem)\n"
"(documentation ShortwaveRadioStation EnglishLanguage \"A &%ShortwaveRadioStation \n"
"is an &%engineeringSubcomponent of a &%ShortwaveRadioSystem.\")\n"
"\n"
";;    E. Radios\n"
"\n"
"(=>\n"
"    (instance ?SYSTEM RadioSystem)\n"
"    (exists (?DEVICE)\n"
"        (and\n"
"            (instance ?DEVICE RadioReceiver)\n"
"            (engineeringSubcomponent ?DEVICE ?SYSTEM))))\n"
"\n"
";;    F. Television broadcast stations\n"
"(subclass TelevisionSystem CommunicationSystem)\n"
"(documentation TelevisionSystem EnglishLanguage \"A system for &%Broadcasting and \n"
"receiving television signals.\")\n"
"\n"
"(subclass TelevisionStation BroadcastingStation)\n"
"(engineeringSubcomponent TelevisionStation TelevisionSystem)\n"
"(documentation TelevisionStation EnglishLanguage \"A &%TelevisionStation is an \n"
"&%engineeringSubcomponent of a &%TelevisionSystem.\")\n"
"(=>\n"
"    (instance ?SYSTEM TelevisionSystem)\n"
"    (exists (?STATION)\n"
"        (and\n"
"            (instance ?STATION TelevisionStation)\n"
"            (engineeringSubcomponent ?STATION ?SYSTEM))))\n"
"\n"
"(subclass CableTelevisionSystem CommunicationSystem)\n"
"(documentation CableTelevisionSystem EnglishLanguage \"A &%CableTelevisionSystem\n"
"is a &%CommunicationSystem for cable television.\")\n"
"\n"
"(=>\n"
"  (instance ?SYSTEM CableTelevisionSystem)\n"
"  (exists (?DEVICE)\n"
"    (and\n"
"      (instance ?DEVICE TelevisionReceiver)\n"
"      (engineeringSubcomponent ?DEVICE ?SYSTEM))))\n"
"\n"
"(subclass SatelliteTelevisionSystem CommunicationSystem)\n"
"(documentation SatelliteTelevisionSystem EnglishLanguage \"&%SatelliteTelevisionSystem       \n"
"is a &%CommunicationSystem where &%ArtificialSatellite is used to transfer TV signals\")\n"
"(termFormat EnglishLanguage SatelliteTelevisionSystem \"satellite tv\")\n"
"\n"
"(=>\n"
"  (instance ?TV SatelliteTelevisionSystem)\n"
"  (exists (?SAT ?RECEIVE)\n"
"    (and\n"
"      (instance ?SAT ArtificialSatellite)\n"
"      (member ?SAT ?TV)\n"
"      (instance ?RECEIVE TelevisionReceiver)\n"
"      (member ?RECEIVE ?TV))))      \n"
"      \n"
"(subclass BroadcastNetwork CommunicationSystem)\n"
"(documentation BroadcastNetwork EnglishLanguage \"&%BroadcastNetwork is the subclass of \n"
"&%CommunicationSystems consisting of &%BroadcastingStations that are linked \n"
"electronically and managed or owned by one organization.\")\n"
"(=>\n"
"  (instance ?N BroadcastNetwork)\n"
"  (forall (?M)\n"
"    (=>\n"
"      (member ?M ?N)\n"
"      (instance ?M BroadcastingStation))))\n"
"\n"
"(=>\n"
"  (instance ?N BroadcastNetwork)\n"
"  (exists (?O)\n"
"    (and\n"
"      (instance ?O Organization)\n"
"      (forall (?M)\n"
"        (=>\n"
"          (member ?M ?N)\n"
"          (possesses ?O ?M))))))\n"
"\n"
";;    G. Televisions\n"
"(subclass TelevisionReceiver ReceiverDevice)\n"
"(subclass TelevisionReceiver EngineeringComponent)\n"
"(termFormat EnglishLanguage TelevisionReceiver \"television\")\n"
"(termFormat EnglishLanguage TelevisionReceiver \"TV\")\n"
"(documentation TelevisionReceiver EnglishLanguage \"A &%TelevisionReceiver is a &%Device for receiving \n"
"television broadcast signals from a &%TelevisionStation or signals\n"
"transmitted through a cable from a &%CableTelevisionSystem.\")\n"
"(=>\n"
"  (instance ?SYSTEM TelevisionSystem)\n"
"  (exists (?DEVICE)\n"
"    (and\n"
"      (instance ?DEVICE TelevisionReceiver)\n"
"      (engineeringSubcomponent ?DEVICE ?SYSTEM))))\n"
"\n"
"(=>\n"
"  (instance ?T TelevisionReceiver)\n"
"  (capability TelevisionBroadcasting patient ?T))\n"
"\n"
"(subclass TelevisionSet ElectricDevice)\n"
"(documentation TelevisionSet EnglishLanguage \"&%TelevisionSet is an &%ElectricDevice\n"
"comprised of a &%TelevisionReceiver and some form of &%VideoDisplay and is part of\n"
"a &%TelevisionSystem\")\n"
"(termFormat EnglishLanguage TelevisionSet \"television set\")\n"
"\n"
"(=>\n"
"  (instance ?TV TelevisionSet)\n"
"  (exists (?RECEIVER ?DISPLAY)\n"
"    (and\n"
"      (instance ?RECEIVER TelevisionReceiver)\n"
"      (instance ?DISPLAY VideoDisplay)\n"
"      (part ?RECEIVER ?TV)\n"
"      (part ?DISPLAY ?TV))))\n"
"\n"
"(subclass TVRemoteControl RemoteControl)\n"
"(documentation TVRemoteControl EnglishLanguage \"&%TVRemoteControl is a type of \n"
"&%RemoteControl that signals to a &%TelevisionReceiver\")\n"
"(termFormat EnglishLanguage TVRemoteControl \"tv remote\")\n"
"\n"
"(=>\n"
"  (instance ?X TVRemoteControl)\n"
"  (hasPurpose ?X\n"
"    (exists (?SIGNAL ?DEVICE)\n"
"      (and\n"
"        (instance ?SIGNAL ElectronicSignalling)\n"
"        (agent ?SIGNAL ?X)\n"
"        (destination ?SIGNAL ?DEVICE)\n"
"        (instance ?DEVICE TelevisionReceiver)))))\n"
"\n"
"  \n"
";;    H. Internet country code\n"
"(instance Internet CommunicationSystem)    \n"
"(documentation Internet EnglishLanguage \"The &%Internet is a &%CommunicationSystem\n"
"for the rapid delivery of information between computers.\")\n"
"\n"
"(instance internetCountryCode BinaryPredicate)\n"
"(domain internetCountryCode 1 GeopoliticalArea)\n"
"(domain internetCountryCode 2 SymbolicString)\n"
"(documentation internetCountryCode EnglishLanguage \"(internetCountryCode ?AREA ?CODE)\n"
"relates a &%GeopoliticalArea to the &%SymbolicString ?CODE used to\n"
"identify the ?AREA on internet websites.\")\n"
"\n"
";;    I. Internet Service Providers (ISPs)\n"
"(subclass InternetServiceProvider CommunicationSystem)\n"
"(engineeringSubcomponent InternetServiceProvider Internet)\n"
"(documentation InternetServiceProvider EnglishLanguage \"An &%InternetServiceProvider\n"
"serves as an &%engineeringSubcomponent of the &%Internet for a given\n"
"area.\")\n"
"(=>\n"
"    (instance ?PART InternetServiceProvider)\n"
"    (engineeringSubcomponent ?PART Internet))\n"
"\n"
";;    J. Internet users\n"
"(instance InternetUser SocialRole)\n"
"(documentation InternetUser EnglishLanguage \"An &%InternetUser is an individual who\n"
"uses the &%Internet.\")\n"
"\n"
"(=>\n"
"    (attribute ?INDIVIDUAL InternetUser)\n"
"    (exists (?PROCESS)\n"
"        (and\n"
"            (agent ?PROCESS ?INDIVIDUAL)\n"
"            (instrument ?PROCESS Internet))))\n"
"\n"
";;    K. Communications - note\n"
"\n"
";; ==========================================================================\n"
"", None, QtGui.QApplication.UnicodeUTF8))
